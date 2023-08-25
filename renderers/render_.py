import configparser
import os

config = configparser.ConfigParser()
config.read(f'{os.getcwd()}/home-dashboard/config.ini')
SRC = config['PATHS']['src']

NAME = '<name>'

#region Class definitions



#endregion Class definitions

#region Retrieve data from SQLite
import sqlite3

with sqlite3.connect(config['PATHS']['db']) as conn:
  cursor = conn.cursor()
  result = cursor.execute("""
    ...
  """).fetchall()

  # Parse into objects
  pass

#endregion Retrieve data from SQLite

#region Generate HTML
from jinja2 import Environment, FileSystemLoader, select_autoescape

TEMPLATES_PATH = f'{SRC}/html/templates'
RENDER = f'{SRC}/html/renders/{NAME}.html'

template = Environment(
  loader=FileSystemLoader(TEMPLATES_PATH),
  autoescape=select_autoescape()
).get_template(f'{NAME}.html')

with open(RENDER, 'w') as file:
  html = template.render()
  file.write(html)

#endregion Generate HTML

#region Save as image

import subprocess

try:
    subprocess.check_call(['python3', f'{SRC}/renderers/render.py', NAME])
except subprocess.CalledProcessError:
    print('HTML was generated, but failed to save the image...')

#endregion Save as image
