#!/usr/bin/python

import re
import shutil

temp = open('temp', 'w')
with open('tunnelworks/settings.py', 'r+') as f:

  for line in f:
    if line.startswith('import'):
      line = line + 'import django_heroku'+'\n' + 'import dj_database_url'+'\n'

    if line.startswith("    'django.middleware.security.SecurityMiddleware',"):
      line = line + "    'whitenoise.middleware.WhiteNoiseMiddleware'," + '\n'

    if line.startswith("INSTALLED_APPS = ["):
      line = line + "    'whitenoise.runserver_nostatic'," + '\n'
    
    re.sub('DEBUG = False', 'DEBUG = True', line)
    re.sub('ALLOWED_HOSTS = \[]', "ALLOWED_HOSTS = \['127\.0\.0\.1', 'engtools\.herokuapp\.com'\]", line)
    re.sub('django\.db\.backends\.mysql', 'django\.db\.backends\.postgresql_psycopg2', line)
      
    temp.write(line)
  f.close()

whitenoise_finders = "WHITENOISE_USE_FINDERS = True"+'\n'
temp.write(whitenoise_finders)

storage = "STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'" + '\n'
temp.write(storage)

database_sett = "DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)"+'\n'
temp.write(database_sett)

django_heroku = "django_heroku.settings(locals())"+'\n'
temp.write(django_heroku)

temp.close()
shutil.move('temp', 'tunnelworks/settings.py')


with open('requirements,txt', 'a') as f:
  f.write('psycopg2-binary==2.9.1'+'\n')
  f.write('gunicorn==20.1.0'+'\n')
  f.write('dj-database-url==0.5.0'+'\n')
  f.write('django-heroku==0.3.1'+'\n')
  f.write('whitenoise==5.3.0'+'\n')
  f.write('psycopg2==2.9.1'+'\n')
  f.close()
