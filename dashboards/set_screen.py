import sys

from inky.auto import auto
from PIL import Image


if len(sys.argv) != 2:
  raise ValueError("Name was not provided!")

image = Image.open("./screens/{}.png".format(sys.argv[1]))
display = auto()
display.set_image(image)
display.show()
