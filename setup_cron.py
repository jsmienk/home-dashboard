import configparser
import os

config = configparser.ConfigParser()
config.read(f'{os.getcwd()}/config.ini')
SRC        = config['PATHS']['src']
DASHBOARDS = config['DASHBOARDS']['names']


def dashboards(name, command):
  if name not in DASHBOARDS:
    raise ValueError('Invalid dashboard name!')
  return f"python3 {SRC}/dashboards/{name}/{command}.py >> {SRC}/logs/{name}-{command}.log 2>&1"

def renderers(name):
  if name not in DASHBOARDS:
    raise ValueError('Invalid dashboard name!')
  return f"python3 {SRC}/renderers/render_{name}.py >> {SRC}/logs/{name}-render.log 2>&1"


from crontab import CronTab

with CronTab(user='pi') as cron:
  cron.remove_all()

  # Art dashboard
  job = cron.new(
    command=renderers('art'),
    comment='Render art dashboard'
  )
  job.setall('*/5 * * * *')

  # Film screenings dashboard
  job = cron.new(
    command=dashboards('film_screenings', 'update_films'),
    comment='Update film screenings database'
  )
  job.setall('0 */4 * * *')
  job = cron.new(
    command=renderers('film_screenings'),
    comment='Render film screenings dashboard'
  )
  job.setall('5 */4 * * *')
