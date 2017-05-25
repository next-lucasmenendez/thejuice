import re
import requests
import wikipedia

from random import randint
from datetime import datetime
from app.database import DB

IMAGES="https://en.wikipedia.org/w/api.php?action=query&prop=images&format=json&titles={query}"
IMAGEINFO="https://en.wikipedia.org/w/api.php?action=query&format=json&prop=imageinfo&iiprop=url&titles={query}"
ICONS="/static/icons/{name}.png"


class Juicer:
	def __init__(self, query=None, lang="en", force=False):
		self.query 	= query
		self.lang 	= lang
		self.force	= force
		self.opts	= []

		self.title 	= ""
		self.text 	= ""
		self.images = []
		self.pic	= None
		self.hits	= None
		self.limits = None

		if not query:
			return

		""" Set lang of searchs """
		if self.lang in wikipedia.languages():
			wikipedia.set_lang(self.lang)

	def find(self):
		base_table = "figures_{lang}"
		table = base_table.format(lang=self.lang)

		db = DB()
		return db.search(table, "name", self.query)

	def get(self):
		try:
			w = wikipedia.page(self.query, auto_suggest=True)
			self.title = w.title
			self.text = w.content
			self.images = w.images
			return True
		except Exception as e:
			print(e)
		return False


	def clean(self):
		hits = sorted(self.hits, key=lambda hit: hit["datetime"])
		normalized = []

		for hit in hits:
			item = hit.copy()
			del (item["datetime"])
			normalized.append(item)

		self.hits 	= normalized

	def fill(self):
		images = self.getimages()
		self.images = images
		self.pic	= self.getpicture()
		self.limits = self.getlimits()

		for hit in self.hits:
			year = datetime.strftime(hit["datetime"], "%Y")
			for image in images:
				if year in image:
					hit["image"] = image
					images.remove(image)

		start, end = 0, len(self.hits) - 1
		self.hits[start]["icon"] 	= ICONS.format(name="born")
		self.hits[end]["icon"] 		= ICONS.format(name="dead")

		currentdates = [hit["date"] for hit in self.hits]
		print(currentdates)
		for img in images:
			res	= re.search("([12]\d{3})", img, re.IGNORECASE)
			if res and "svg" not in img:
				date = res.group(0)
				if date not in currentdates and self.limits["start"] < date < self.limits["end"]:
					currentdates.append(date)
					self.hits.append({
						'date': date,
						'datetime': datetime.strptime(date, "%Y"),
						'content': '',
						'image': img
					})

		print(currentdates)

	def getpicture(self):
		if self.images:
			needle = self.title.replace(" ", "_")
			images = []
			for img in self.images:
				if re.search(needle, img, re.IGNORECASE) and "svg" not in img:
					images.append(img)

			if len(images):
				picture = randint(0, len(images) - 1)
				return images[picture]

		return None

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
					except Exception as e:
						print(e)
						pass
		except Exception as e:
			print(e)
			pass

		return self.images

	def getlimits(self):
		limits = {
			"start": self.hits[0]["date"],
			"end": self.hits[len(self.hits) - 1]["date"]
		}

		return limits

	def torender(self):
		self.fill()
		self.clean()

		return {
			"title": self.title,
			"images": self.images,
			"hits": self.hits,
			"pic": self.pic,
			"limits": self.limits
		}