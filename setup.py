"""
Create folders and variables required to operate.

/art
/html
  /renders
    /tmp
/screens
"""

import os

folders = [
  "art",
  "html/renders/tmp",
  "screens"
]

for folder in folders:
  os.makedirs(folder, exist_ok=True)


import configparser

config = configparser.ConfigParser()

SRC = '~/home-dashboard'
DASHBOARDS = [
  'art',
  'film_screenings',
  'n/a',
  'n/a'
]

config['PATHS']['src'] = SRC
config['PATHS']['db'] = f'{SRC}/home_dashboard.db'
config['PATHS']['chromium'] = '/usr/lib/chromium-browser/chromedriver'

config['DASHBOARDS']['names'] = DASHBOARDS
config['DASHBOARDS']['active'] = DASHBOARDS[0]

config['ART']['url'] = 'https://api.artic.edu/api/v1/artworks'

config['FILM_SCREENINGS']['url'] = 'https://www.vuecinemas.nl/movies.json'
config['FILM_SCREENINGS']['cinema_id'] = 24

with open(f'{SRC}/config.ini', 'w') as f:
  config.write(f)
