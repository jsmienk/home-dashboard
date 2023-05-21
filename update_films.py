"""
Run a couple times a day using a cronjob to update the data in the database.
"""

import os
import requests
import sqlite3

from datetime import datetime, date, timedelta


URL = "https://www.vuecinemas.nl/movies.json"
CINEMA_ID = 24
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

class Screening:
  def __init__(self, data):
    self.id = data.get('id')
    self.has_3d = bool(data.get('has_3d'))
    self.has_atmos = bool(data.get('has_atmos'))
    self.has_ov = bool(data.get('has_ov'))  # original version
    self.has_nl = bool(data.get('has_nl'))  # dutch version (includes all Dutch movies...)
    self.has_break = bool(data.get('has_break'))
    self.start = datetime.strptime(data.get('start'), DATETIME_FORMAT)
    self.end = datetime.strptime(data.get('end'), DATETIME_FORMAT)
    self.visible = bool(data.get('visible'))
    self.disabled = bool(data.get('disabled'))
    self.occupied_seats = data.get('occupied_seats')
    self.total_seats = data.get('total_seats')

class Film:
  def __init__(self, data):
    self.id = data.get('id')
    self.title = data.get('title')
    self.slug = data.get('slug')
    self.description = data.get('description')
    self.genres = data.get('genres')
    self.cast = data.get('cast')
    self.image_url = data.get('image')
    self.release_date = datetime.strptime(data.get('release_date'), DATETIME_FORMAT).date
    self.rating_average = data.get('rating_average')
    self.rating_count = data.get('rating_count')
    self.screenings = [Screening(s) for s in data.get('performances', [])]


# Create a SQLite database connection
with sqlite3.connect(os.environ.get("HOME_DASHBOARD_DB")) as conn:
  cursor = conn.cursor()

  # Query the API for today and the next 6 days
  today = date.today()
  for i in range(7):
    query_date = today + timedelta(days=i)
    query_params = {
      "type": "NOW_PLAYING_WITH_PERFORMANCES",
      "filters[cinema_id]": CINEMA_ID,
      "dateOffset": str(query_date)
    }

    response = requests.get(URL, params=query_params)
    if response.status_code == 200:
      for film_data in response.json():
        f = Film(film_data)
        cursor.execute("INSERT OR IGNORE INTO films (id, title, slug, description, genres, cast, image_url, release_date, rating_average, rating_count) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (f.id, f.title, f.slug, f.description, f.genres, f.cast, f.image_url, f.release_date, f.rating_average, f.rating_count))
        for s in f.screenings:
          cursor.execute("INSERT OR REPLACE INTO screenings (id, film_id, has_3d, has_atmos, has_ov, has_nl, has_break, start, end, visible, disabled, occupied_seats, total_seats) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (s.id, f.id, s.has_3d, s.has_atmos, s.has_ov, s.has_nl, s.has_break, s.start, s.end, s.visible, s.disabled, s.occupied_seats, s.total_seats))
  conn.commit()
