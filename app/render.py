import requests

from io import StringIO
from xhtml2pdf import pisa
from datetime import datetime
from flask import render_template


class Render():
	def __init__(self, title, images, hits):
		self.title	= title
		self.images	= images
		self.hits	= hits

		self.page		= ""
		self.template 	= "templates/formats/infographic.html"
		self.fill()

	def fill(self):
		uri			= "https://en.wikipedia.org/w/api.php?action=query&prop=images&format=json&titles={query}"
		query 		= self.title.replace(" ", "+")
		endpoint 	= uri.format(query=query)

		try:
			req = requests.get(endpoint)
			print(req.status_code)
			if req.status_code is 200:
				res = req.json()
				pages 	= res["query"]["pages"]
				page 	= pages[list(pages.keys())[0]]
				images 	= [image["title"] for image in pages["images"]]

		except Exception as e:
			if self.images:
				images = self.images.copy()
				for hit in self.hits:
					year = datetime.strftime(hit["datetime"], "%Y")
					for image in images:
						if year in image:
							hit["image"] = image
							images.remove(image)
			else:
				pass

		print(self.hits)

	def render(self):
		data = {
			"title": self.title,
			"hits": self.hits
		}
		self.page = render_template(self.template, data=data)

	def output(self):
		pdf = StringIO()
		pisa.CreatePDF(StringIO(self.page), pdf)
		return pdf
