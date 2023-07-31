import os
import RPi.GPIO as GPIO
import signal
import subprocess

print('Dashboards running. Quit using Ctrl+C!')

BUTTONS = [ 5,   6,   16,  24]
LABELS  = ['A', 'B', 'C', 'D']
DASHBOARDS = [
  'art',
  'films_screenings',
  'n/a',
  'n/a'
]


def load_dashboard(dashboard):
  if dashboard == 'n/a': return

  print('Loading dashboard \'{}\' ...'.format(dashboard.upper()))
  try:
    if os.getenv('ACTIVE_DASHBOARD') != dashboard:
      os.putenv('ACTIVE_DASHBOARD', dashboard)
      subprocess.check_call(['python3', '/home/pi/home-dashboard/dashboards/set_screen.py', dashboard])
  except subprocess.CalledProcessError:
    print('Dashboard \'{}\' failed to run!'.format(dashboard.upper()))


def handle_button(pin):
  dashboard = DASHBOARDS[BUTTONS.index(pin)]
  load_dashboard(dashboard)


GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
for pin in BUTTONS:
  GPIO.add_event_detect(pin, GPIO.FALLING, handle_button, bouncetime=250)

load_dashboard(DASHBOARDS[0])

signal.pause()
