import os
import sys

from jinja2 import Environment
from jinja2 import FileSystemLoader

URL="/output/{name}"
OUTPUT="{base}/templates/output/{name}.html"
TEMPLATES="{base}/templates/formats"

class Render():
	def __init__(self, title, images, hits, fmt, pic, limits):
		self.title	= title
		self.images	= images
		self.hits	= hits
		self.fmt	= fmt
		self.pic	= pic
		self.limits = limits

	def save(self):
		base		= os.path.abspath(os.path.dirname(sys.argv[0]))
		templates	= TEMPLATES.format(base=base)
		loader		= FileSystemLoader(templates)
		environment = Environment(loader=loader)

		filename	= "{format}.html".format(format=self.fmt)
		template 	= environment.get_template(filename)

		name 	= self.title.replace(" ", "_")
		data	= {
			"title": self.title,
			"items": self.hits,
			"limits": self.limits,
			"picture": self.pic
		}
		result 	= template.render(data).encode('utf-8')
		output	= OUTPUT.format(base=base, name=name)

		try:
			with open(output, "wb") as fd:
				fd.write(result)
		except Exception as e:
			print(e)
			return False

		print(name)
		return URL.format(name=name)
