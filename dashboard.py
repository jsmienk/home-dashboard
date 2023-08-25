import configparser
import os

CONFIG_PATH = f'{os.getcwd()}/config.ini'
config = configparser.ConfigParser()
config.read(CONFIG_PATH)


import RPi.GPIO as GPIO
import signal
import subprocess

print('Dashboards running. Quit using Ctrl+C!')

BUTTONS = [ 5,   6,   16,  24]
LABELS  = ['A', 'B', 'C', 'D']
NAMES = config['DASHBOARDS']['names'].split()


def load_dashboard(button_pin):
  name = NAMES[BUTTONS.index(button_pin)]
  if name == 'n/a': return

  config.read(CONFIG_PATH)

  print(f"Loading dashboard '{name.upper()}' ...")
  try:
    if config['DASHBOARDS']['active'] != name:
      subprocess.check_call(['python3', f"{config['PATHS']['src']}/dashboards/set_screen.py", name])
      
      # save name of current active screen
      with open(CONFIG_PATH, 'w') as f:
        config['DASHBOARDS']['active'] = name
        config.write(f)
  except subprocess.CalledProcessError:
    print(f"Could not set screen to dashboard '{name.upper()}'!")


# listen to button presses
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
for pin in BUTTONS:
  GPIO.add_event_detect(pin, GPIO.FALLING, load_dashboard, bouncetime=250)

load_dashboard(BUTTONS[0])  # start on first screen

signal.pause()
