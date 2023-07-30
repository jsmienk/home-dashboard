from inky.auto import auto
from PIL import Image

display = auto()

print(display.colour)
print(display.resolution)

image = Image.open("./screens/art.png")
display.set_image(image)
display.show()
