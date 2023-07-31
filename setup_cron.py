from crontab import CronTab


DASHBOARDS = ['art', 'film_screenings']

def dashboards(name, command):
  if name not in DASHBOARDS:
    raise ValueError('Invalid dashboard name!')
  return f"~/home_dashboard/dashboards/{name}/{command}.py"

def renderers(name):
  if name not in DASHBOARDS:
    raise ValueError('Invalid dashboard name!')
  return f"~/home_dashboard/renderers/render_{name}.py"


with CronTab(user='pi') as cron:
  # Art dashboard
  job = cron.new(command=renderers('art'), comment='Render art dashboard')
  job.minute.every(2)

  # Film screenings dashboard
  job = cron.new(command=dashboards('film_screenings', 'update_films'), comment='Update film screenings database')
  job.hour.every(2)
  job = cron.new(command=renderers('film_screenings'), comment='Render film screenings dashboard')
  job.hour.every(2).minute.on(5)
