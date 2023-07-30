NAME = "film_screenings"
films = dict()

#region Class definitions
import re

from datetime import datetime, date, timedelta

class Screening:
  def __init__(self, db_row) -> None:
    self.id = db_row[0]
    # db_row[1] is the film_id
    self.has_3d = bool(db_row[2])
    self.has_atmos = bool(db_row[3])
    self.has_ov = bool(db_row[4])  # original version
    self.has_nl = bool(db_row[5])  # dutch version (includes all Dutch movies...)
    self.has_break = bool(db_row[6])
    self.start = datetime.strptime(db_row[7][:19], "%Y-%m-%d %H:%M:%S")
    self.end = datetime.strptime(db_row[8][:19], "%Y-%m-%d %H:%M:%S")
    self.visible = bool(db_row[9])
    self.disabled = bool(db_row[10])
    self.occupied_seats = db_row[11]
    self.total_seats = db_row[12]

class Film:
  def __init__(self, db_row) -> None:
    self.id = db_row[0]
    self.title = db_row[1]
    self.slug = db_row[2]
    self.description = db_row[3]
    self.genres = db_row[4]
    self.cast = db_row[5]
    self.image_url = db_row[6]
    self.release_date = datetime.strptime(db_row[7][:10], "%Y-%m-%d").date()
    self.rating_average = db_row[8]
    self.rating_count = db_row[9]
    self.screenings = list()
  
  def add_screening(self, screening):
    self.screenings.append(screening)
  
#endregion Class definitions

#region Retrieve data from SQLite
import os
import sqlite3

with sqlite3.connect(os.environ.get("HOME_DASHBOARD_DB")) as conn:
  cursor = conn.cursor()
  # Get available 2D screenings that start between 17:00 and 22:00 in the coming days
  result = cursor.execute("""
    SELECT f.*, s.*
    FROM films AS F
    JOIN screenings AS s ON f.id = s.film_id
    WHERE s.start BETWEEN date('now') AND date('now', '+6 days')
      AND s.occupied_seats < s.total_seats
      AND s.has_3d = 0 AND s.visible = 1 AND s.disabled = 0
      AND time(s.start) BETWEEN time('17:00') AND time('22:00')
      AND f.title NOT LIKE '%Nederlandse Versie%'
    ORDER BY date(s.start) ASC, f.release_date DESC
  """).fetchall()

  # Parse into Film and Screening objects
  for data in result:
    film_id = data[0]
    if film_id not in films:
      films[film_id] = Film(data[:10])
    films[film_id].add_screening(Screening(data[10:]))
  
  if len(films) == 0:
    raise ValueError("No films found to render!")

#endregion Retrieve data from SQLite

#region Generate HTML
import random

from jinja2 import Environment, FileSystemLoader, select_autoescape

TEMPLATES_PATH = "./html/templates"
RENDER = f"./html/renders/{NAME}.html"
WEEKDAYS = ['ma', 'di', 'wo', 'do', 'vr', 'za', 'zo']

class FilmDecorator:
  def __init__(self, film: Film) -> None:
    self.film = film

  @property
  def title(self):
    return re.sub(" \(originele versie\)", '', self.film.title.strip(), flags=re.IGNORECASE)

  @property
  def release(self):
    return self.film.release_date.strftime("%d/%m")

  @property
  def genres(self):
    return ', '.join(self.film.genres.split(' / '))

  def weekdays(self):
    coming_weekdays = [(date.today() + timedelta(days=i)).weekday() for i in range(7)]
    screening_weekdays = {s.start.weekday() for s in self.film.screenings}
    return [WEEKDAYS[weekday] if weekday in screening_weekdays else None for weekday in coming_weekdays]


film_decorators = [FilmDecorator(film) for film in films.values()]

template = Environment(
  loader=FileSystemLoader(TEMPLATES_PATH),
  autoescape=select_autoescape()
).get_template(f"{NAME}.html")

with open(RENDER, 'w') as file:
  html = template.render(
    films=film_decorators,
    background=random.choice(list(films.values())).image_url
  )
  file.write(html)

#endregion Generate HTML

#region Save as image

import subprocess

try:
    subprocess.check_call(["python3", "./renderers/render.py", NAME])
except subprocess.CalledProcessError:
    print("HTML was generated, but failed to save the image...")

#endregion Save as image
