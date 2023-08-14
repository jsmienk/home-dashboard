"""
Run once to populate the database with artwork information and store the image files
"""

import os
import requests
import sqlite3
import time


URL = "https://api.artic.edu/api/v1/artworks"
IMAGE_FOLDER_NAME = "art"
ART_TYPES = ["Painting"]


class Artwork:
  def __init__(self, data) -> None:
    self.id = data.get('id')
    self.resource_id = data.get('image_id')
    self.title = data.get('title')
    self.date_display = data.get('date_display')
    self.artist = data.get('artist_title')
    self.artwork_type = data.get('artwork_type_title')
    dimensions = data.get('dimensions_detail')
    dimensions = { "width_cm": 1, "height_cm": 1 } if len(dimensions) == 0 else dimensions[0]
    self.width = dimensions['width_cm']
    self.height = dimensions['height_cm']

  @property
  def image_url(self):
    return f"https://www.artic.edu/iiif/2/{self.resource_id}/full/843,/0/default.jpg"

  @property
  def image_file_path(self):
    return os.path.join(os.getcwd(), IMAGE_FOLDER_NAME, f"{self.id}.jpg")

  @property
  def is_landscape(self) -> bool:
    if self.height == 0: return False
    ratio = self.width / self.height
    return ratio > 1.5 and ratio < 1.9

  @property
  def is_suitable(self) -> bool:
    return self.is_landscape and self.resource_id is not None and self.artwork_type in ART_TYPES


params = {
  "fields": "id,image_id,title,date_display,artist_title,dimensions_detail,artwork_type_title",
  "limit": 30,
  "page": 590
}

count = 0
while count < 100:
  params["page"] += 1
  print("Page", params["page"])

  response = requests.get(URL, params=params)
  if response.status_code == 200:
    # Create a SQLite database connection
    with sqlite3.connect(os.getenv('HOME_DASHBOARD_DB')) as conn:
      cursor = conn.cursor()
      for artwork_data in response.json()["data"]:
        a = Artwork(artwork_data)
        if not a.is_suitable:
          continue

        count += 1
        print(f"Artwork {a.id} is suitable ({count}).")

        time.sleep(1)  # do not stress the API

        # Download the image
        response2 = requests.get(a.image_url)
        if response2.status_code == 200:
          with open(a.image_file_path, "wb") as f:
            f.write(response2.content)

          # Store the information
          cursor.execute("INSERT OR IGNORE INTO artworks (id, resource_id, image_path, title, date_display, artist) VALUES (?, ?, ?, ?, ?, ?)",
                        (a.id, a.resource_id, a.image_file_path, a.title, a.date_display, a.artist))
          conn.commit()
        else:
          print("Error retrieving art image!", a.id, response2.status_code)
  else:
    print("Error retrieving art info!", params["page"], response.status_code)
