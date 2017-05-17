import re
import requests
import wikipedia
import xmltodict

from random import randint
from datetime import datetime

DBPEDIA="http://lookup.dbpedia.org/api/search.asmx/PrefixSearch?QueryClass=&MaxHits=5&QueryString={query}"
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
		suggested = []

		if not self.force:
			query = self.query.replace(" ", "+")
			endpoint = DBPEDIA.format(query=query)
			res = requests.get(endpoint)
			if res.status_code is 200:
				content = xmltodict.parse(res.text.encode('utf-8'))

				if "Result" in content["ArrayOfResult"].keys():
					results = content["ArrayOfResult"]["Result"]

					if results:
						for result in results:
							try:
								title = result["Label"]
								if result["Classes"]:
									classes = result["Classes"]["Class"]
									for c in classes:
										if c["Label"] == "person" and title not in suggested:
											suggested.append(title)
							except:
								pass
					if suggested:
						for suggestion in suggested:
							try:
								w = wikipedia.page(suggestion, auto_suggest=True)

								self.title 	= suggestion
								self.text 	= w.content
								self.images	= w.images
								return True
							except Exception as e:
								suggested.remove(suggestion)
								continue

			"""
			TODO: if suggested options is empty, try to search 
			first on wikipedia and them clean results checking if each
			one is person with dbpedia.
			"""
			self.opts = wikipedia.search(self.query, results=6)
		else:
			try:
				w = wikipedia.page(self.query, auto_suggest=True)
			except Exception as e:
				if hasattr(e, 'options') and e.options:
					self.opts = e.options
				return False

			self.title	= w.title
			self.text	= w.content
			self.images	= w.images
			return True

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

		for img in images:
			res	= re.search("([12]\d{3})", img, re.IGNORECASE)
			if res and "svg" not in img:
				date		= res.group(0)
				if self.limits["start"] < date < self.limits["end"]:
					self.hits.append({
						'date': date,
						'datetime': datetime.strptime(date, "%Y"),
						'content': '',
						'image': img
					})


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
					except:
						pass
		except:
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