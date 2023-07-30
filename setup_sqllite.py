"""
Run once to setup the database for the home dashboard project.

Films and Screenings tables for Vue movies
"""

import os
import sqlite3


with sqlite3.connect(os.environ.get("HOME_DASHBOARD_DB")) as conn:
  cursor = conn.cursor()

  # ARTWORKS
  # cursor.execute("DROP TABLE artworks")
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS artworks (
      id INTEGER PRIMARY KEY,
      resource_id TEXT,
      image_path TEXT,
      title TEXT,
      date_display TEXT,
      artist TEXT
  )""")
  conn.commit()

  # FILMS AND SCREENINGS
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS films (
      id INTEGER PRIMARY KEY,
      title TEXT,
      slug TEXT,
      description TEXT,
      genres TEXT,
      cast TEXT,
      image_url TEXT,
      release_date DATE,
      rating_average REAL,
      rating_count INTEGER
  )""")
  conn.commit()
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS screenings (
      id INTEGER PRIMARY KEY,
      film_id INTEGER,
      has_3d INTEGER,
      has_atmos INTEGER,
      has_ov INTEGER,
      has_nl INTEGER,
      has_break INTEGER,
      start DATETIME,
      end DATETIME,
      visible INTEGER,
      disabled INTEGER,
      occupied_seats INTEGER,
      total_seats INTEGER,
      FOREIGN KEY (film_id) REFERENCES films(id)
  )""")
  conn.commit()
