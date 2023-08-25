import configparser
import os

config = configparser.ConfigParser()
config.read(f'{os.getcwd()}/home-dashboard/config.ini')
SRC = config['PATHS']['src']

NAME = 'art'

#region Class definitions

class Artwork:
  def __init__(self, db_row) -> None:
    self.id = db_row[0]
    self.image_path = db_row[1]
    self.title = db_row[2]
    self.date_display = db_row[3]
    self.artist = db_row[4]

#endregion Class definitions

#region Retrieve data from SQLite
import random
import sqlite3

artwork = None

with sqlite3.connect(config['PATHS']['db']) as conn:
  cursor = conn.cursor()
  result = cursor.execute("""
    SELECT id, image_path, title, date_display, artist
    FROM artworks
  """).fetchall()

  if len(result) == 0:
    raise LookupError('No artwork found to select!')

  # Parse into object
  artwork = Artwork(random.choice(result))

#endregion Retrieve data from SQLite

#region Generate QR code

import qrcode

img = qrcode.make(f'https://www.artic.edu/artworks/{artwork.id}')
img.save(f'{SRC}/html/renders/tmp/qr.png')

#endregion Generate QR code

#region Generate HTML
from jinja2 import Environment, FileSystemLoader, select_autoescape

TEMPLATES_PATH = f'{SRC}/html/templates'
RENDER = f'{SRC}/html/renders/{NAME}.html'

template = Environment(
  loader=FileSystemLoader(TEMPLATES_PATH),
  autoescape=select_autoescape()
).get_template(f'{NAME}.html')

with open(RENDER, 'w') as file:
  html = template.render(artwork=artwork)
  file.write(html)

#endregion Generate HTML

#region Save as image

import subprocess

try:
    subprocess.check_call(['python3', f'{SRC}/renderers/render.py', NAME])
except subprocess.CalledProcessError:
    print('HTML was generated, but failed to save the image...')

#endregion Save as image
