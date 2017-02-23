import os
import sys
import site

base_path	= '/var/www/juice-mvp'
packages	= '%s/venv/lib/python3.5/site-packages' % base_path
execution	= '%s/app' % base_path
venv_start	= '%s/venv/bin/activate_this.py' % base_path

# Add virtualenv site packages
site.addsitedir(packages)

# Path of execution
sys.path.append(execution)

# Fired up virtualenv before include application
execfile(activate_env, dict(__file__=venv_start))

# import my_flask_app as application
from server import app as application
