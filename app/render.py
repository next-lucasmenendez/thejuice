import os
import sys
import requests

from io import StringIO
from xhtml2pdf import pisa
from datetime import datetime
from flask import render_template

OUTPUT="{base}/output/{name}.pdf"
IMAGES="https://en.wikipedia.org/w/api.php?action=query&prop=images&format=json&titles={query}"
IMAGEINFO="https://en.wikipedia.org/w/api.php?action=query&format=json&prop=imageinfo&iiprop=url&titles={query}"
TEMPLATES={
	"infografic": "templates/formats/infographic.html"
}

class Render():
	def __init__(self, title, images, hits, format):
		self.title	= title
		self.images	= images
		self.hits	= hits
		self.format	= format

		self.fill()

	def fill(self):
		images = self.getimages()
		for hit in self.hits:
			year = datetime.strftime(hit["datetime"], "%Y")
			for image in images:
				if year in image:
					hit["image"] = image
					images.remove(image)

	def getimages(self):
		query = self.title.replace(" ", "+")
		endpoint = IMAGES.format(query=query)
		try:
			req = requests.get(endpoint)
			if req.status_code is 200:
				res = req.json()
				pages = res["query"]["pages"]
				page = pages[list(pages.keys())[0]]

				images_titles = [image["title"] for image in page["images"]]
				for image in images_titles:
					endpoint = IMAGEINFO.format(query=image)
					try:
						req = requests.get(endpoint)
						if req.status_code is 200:
							res = req.json()

							image = res["query"]["pages"]["-1"]["imageinfo"][0]["url"]
							self.images.append(image)
					except:
						pass
		except:
			pass

		return self.images


	def save(self):
		title	= self.title.replace(" ", "_")
		page	= render_template(TEMPLATES[self.format], title=self.title, hits=self.hits)
		path	= os.path.abspath(os.path.dirname(sys.argv[0]))

		pdf		= StringIO()
		pisa.CreatePDF(StringIO(page), pdf)

		file = OUTPUT.format(base=path, name=title)
		try:
			with open(file, "wr") as fd:
				fd.write(pdf)
		except:
			return False
		return True
