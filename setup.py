"""
Create the folders stuff will be created in.

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
