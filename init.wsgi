#!/usr/bin/python3
import sys
import logging
from run import app

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/theJuice/")

app.run(host="0.0.0.0", debug=True)
