import os
import sys
import base64
from datetime import datetime

from jinja2 import Environment
from jinja2 import FileSystemLoader

URL="/output/{name}"
OUTPUT="{base}/templates/output/{name}.html"
TEMPLATES="{base}/templates/designs"


class Template:
	def __init__(self, design='nude'):
		self.base	= os.path.abspath(os.path.dirname(sys.argv[0]))
		templates	= TEMPLATES.format(base=self.base)
		loader		= FileSystemLoader(templates)

		self.design = design
		self.env	= Environment(loader=loader)

	def __getfilename(self, title):
		dt		= datetime.today().strftime("%s")
		mark	= ("{date}-{name}".format(date=dt, name=title)).encode()

		return base64.b64encode(mark).decode('utf-8')

	def __gettemplate(self, data):
		design_file = "{design}.html".format(design=self.design)
		template	= self.env.get_template(design_file)

		filename = self.__getfilename(data.get('title'))

		result = template.render(data).encode('utf-8')
		output = OUTPUT.format(base=self.base, name=filename)

		with open(output, "wb+") as fd:
			success = fd.write(result)
			if success:
				return URL.format(name=filename)

		return False

	def render(self, title=None, sentences=None):
		if title and sentences:
			data = {
				"title": title,
				"sentences": sentences
			}

			url = self.__gettemplate(data)
			if url:
				return url
		return False