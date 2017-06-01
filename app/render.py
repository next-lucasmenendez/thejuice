# -*- coding: utf-8 -*-

import os
import sys
import base64

from datetime import datetime
from jinja2 import Environment
from jinja2 import FileSystemLoader

URL="/output/{name}"
OUTPUT="{base}/templates/output/{name}.html"
TEMPLATES="{base}/templates/designs"


class Render:
	def __init__(self, title, images, hits, design, pic, limits):
		self.title	= title
		self.images	= images
		self.hits	= hits
		self.design	= design
		self.pic	= pic
		self.limits = limits

	def save(self):
		base		= os.path.abspath(os.path.dirname(sys.argv[0]))
		templates	= TEMPLATES.format(base=base)
		loader		= FileSystemLoader(templates)
		environment = Environment(loader=loader)

		filename	= "{design}.html".format(design=self.design)
		template 	= environment.get_template(filename)

		dt		= datetime.today().strftime("%s")
		mark	= ("{date}-{name}".format(date=dt, name=self.title)).encode()
		name 	= base64.b64encode(mark).decode('utf-8')
		data	= {
			"title": self.title,
			"items": self.hits,
			"limits": self.limits,
			"picture": self.pic
		}

		result 	= template.render(data).encode('utf-8')
		output = OUTPUT.format(base=base, name=name)

		with open(output, "wb+") as fd:
			success = fd.write(result)

			if not success:
				return False

		return URL.format(name=name)
