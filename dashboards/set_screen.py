import configparser
import sys

from inky.auto import auto
from PIL import Image


if len(sys.argv) != 2:
  raise ValueError('Name was not provided!')

config = configparser.ConfigParser()
config.read('~/home-dashboard/config.ini')

image = Image.open(f"{config['PATHS']['src']}/screens/{sys.argv[1]}.png")
display = auto()
display.set_image(image)
display.show()
