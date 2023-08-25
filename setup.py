"""
Create folders and variables required to operate.

/art
/html
  /renders
    /tmp
/screens
"""
import configparser
import os


folders = [
  'art',
  'html/renders/tmp',
  'screens',
  'logs'
]

for folder in folders:
  os.makedirs(folder, exist_ok=True)


SRC = os.getcwd()

with open(f'{SRC}/config.ini', 'w') as f:
  config = configparser.ConfigParser()

  config['PATHS'] = {
    'src': SRC,
    'db': f'{SRC}/home_dashboard.db',
    'chromium': '/usr/lib/chromium-browser/chromedriver'
  }
  config['DASHBOARDS'] = {
    'names': 'art film_screenings n/a n/a',
    'active': 'art'
  }
  config['ART'] = {
    'url': 'https://api.artic.edu/api/v1/artworks'
  }
  config['FILM_SCREENINGS'] = {
    'url': 'https://www.vuecinemas.nl/movies.json',
    'cinema_id': 24
  }

  config.write(f)
