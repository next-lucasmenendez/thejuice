import os
import sys
import base64
import re

from datetime import datetime
from jinja2 import Environment
from jinja2 import FileSystemLoader

URL="/output/{name}"
OUTPUT="{base}/templates/output/{name}.html"
TEMPLATES="{base}/templates/designs"


class Render:
	def __init__(self, url, title, questions, email, image, design=None):
		self.title = title
		self.url = url
		self.questions = questions
		self.email = email
		self.image = image
		self.design = design or 'default'

	def save(self):
		base = os.path.abspath(os.path.dirname(sys.argv[0]))
		templates = TEMPLATES.format(base=base)
		loader = FileSystemLoader(templates)
		environment = Environment(loader=loader)

		filename = "{design}.html".format(design=self.design)
		template = environment.get_template(filename)

		dt = datetime.today().strftime("%s")
		file_title = re.sub(r'\s+', '_', self.title.lower())
		mark = ("{date}-{name}".format(date=dt, name=file_title)).encode()
		name = base64.b64encode(mark).decode('utf-8')
		data = {
			"title": self.title,
			"teacher_email": self.email,
			"questions": self.questions,
			"url": self.url,
			"image": self.image
		}

		result = template.render(data).encode('utf-8')
		output = OUTPUT.format(base=base, name=name)

		with open(output, "wb+") as fd:
			success = fd.write(result)

			if not success:
				return False

		return URL.format(name=name)
