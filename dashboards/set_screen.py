import sys

from inky.auto import auto
from PIL import Image


if len(sys.argv) != 2:
  raise ValueError("Name was not provided!")

PWD = '/home/pi/home-dashboard'

image = Image.open(f'{PWD}/screens/{sys.argv[1]}.png')
display = auto()
display.set_image(image)
display.show()
