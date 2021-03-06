#!/usr/bin/python

import re
import shutil

temp = open('temp', 'w')
with open('../engtools_root/settings.py', 'r+') as f:

  for line in f:
    if line.startswith('import'):
      line = line + 'import django_heroku'+'\n' + 'import dj_database_url'+'\n'

    # if line.startswith("    'django.middleware.security.SecurityMiddleware',"):
      # line = line + "    'whitenoise.middleware.WhiteNoiseMiddleware'," + '\n'
    
    line = re.sub('DEBUG = True', 'DEBUG = False', line)
    line = re.sub(r'ALLOWED_HOSTS = \[]', r"ALLOWED_HOSTS = ['127.0.0.1', 'engtools.herokuapp.com']", line)
    line = re.sub(r'django\.db\.backends\.mysql', r'django.db.backends.postgresql_psycopg2', line)
      
    temp.write(line)
  f.close()

whitenoise_finders = "WHITENOISE_USE_FINDERS = True"+'\n'
# temp.write(whitenoise_finders)

storage = "STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'" + '\n'
# temp.write(storage)
temp.write('\n')

database_sett = "DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)"+'\n'
temp.write(database_sett)
temp.write('\n')

django_heroku = "django_heroku.settings(locals(), logging=False)"+'\n'
temp.write(django_heroku)
temp.write('\n')

temp.close()
shutil.move('temp', '../engtools_root/settings.py')


with open('../requirements.txt', 'a') as f:
  f.write('psycopg2-binary==2.9.1'+'\n')
  f.write('gunicorn==20.1.0'+'\n')
  f.write('dj-database-url==0.5.0'+'\n')
  f.write('django-heroku==0.3.1'+'\n')
  f.write('whitenoise==5.3.0'+'\n')
  f.write('psycopg2==2.9.1'+'\n')
  f.write(''+'\n')
  f.close()
