from crontab import CronTab


PWD = '/home/pi/home-dashboard'
DASHBOARDS = ['art', 'film_screenings']

def dashboards(name, command):
  if name not in DASHBOARDS:
    raise ValueError('Invalid dashboard name!')
  return f"python3 {PWD}/dashboards/{name}/{command}.py >> {PWD}/dashboards/{name}/{command}.log 2>&1"

def renderers(name):
  if name not in DASHBOARDS:
    raise ValueError('Invalid dashboard name!')
  return f"python3 {PWD}/renderers/render_{name}.py >> {PWD}/dashboards/{name}/render.log 2>&1"


with CronTab(user='pi') as cron:
  cron.remove_all()

  # Art dashboard
  job = cron.new(
    command=renderers('art'),
    comment='Render art dashboard'
  )
  job.setall('*/2 * * * *')

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
