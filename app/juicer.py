import re
import os
import sys
import json

from random import randint
from textblob import TextBlob
from datetime import datetime

from app.datasource import DataSource
from app.parser import Parser

ICONSINDEX="{base}/static/icons/icons.json"
ICON="/static/icons/{file}"


class Juicer:
	def __init__(self, name=None, text=None, images=None, birth=None, death=None, lang="en"):
		self.name 	= name
		self.text 	= text
		self.images = images
		self.lang	= lang
		self.pic	= None
		self.hits	= None
		self.limits = {
			"start": birth,
			"end": death
		}

	def __parse(self):
		start, end = self.__parselimits()
		parser = Parser(text=self.text, start=start, end=end, lang=self.lang)
		self.hits = parser.parse()

	def __clean(self):
		hits = sorted(self.hits, key=lambda hit: hit["datetime"])
		normalized = []

		for hit in hits:
			item = hit.copy()
			del (item["datetime"])
			normalized.append(item)

		self.hits = normalized

	def __fill(self):
		images = self.images.copy()
		for hit in self.hits:
			year = datetime.strftime(hit["datetime"], "%Y")
			for image in images:
				if year in image:
					hit["image"] = image
					images.remove(image)

		start, end		= self.__parselimits()
		currentdates	= [hit["date"] for hit in self.hits]
		if images:
			for image in images:
				res	= re.search("([12]\d{3})", image, re.IGNORECASE)
				if res:
					date	= res.group(0)
					dt 		= datetime.strptime(date, "%Y")
					if date not in currentdates and start < dt < end:
						currentdates.append(date)
						self.hits.append({
							'date': date,
							'datetime': dt,
							'content': '',
							'image': image
						})

		self.__getkeywords()
		self.__geticons()
		return

	def __getpicture(self):
		if self.images:
			images = []
			needle = self.name.replace(" ", "_")
			for img in self.images:
				if re.search(needle, img, re.IGNORECASE):
					images.append(img)
			if len(images):
				index = randint(0, len(images) - 1)
				self.pic = images[index]

	def __getkeywords(self):
		for hit in self.hits:
			content = hit['content']
			blob 	= TextBlob(content)

			keywords = []
			for word, pos in blob.tags:
				if str(pos).startswith("VB") or pos == "NN":
					keywords.append(word.lower())

			hit['keywords'] = keywords

		return True

	def __geticons(self):
		main_path	= os.path.realpath(sys.argv[0])
		base		= os.path.dirname(main_path)
		index		= ICONSINDEX.format(base=base)

		with open(index) as fd:
			icons = json.loads(fd.read())

			for hit in self.hits:
				if 'icons' not in hit.keys():
					hit['icons'] = []

				for keyword in hit['keywords']:
					for item in icons:
						file = item['icon']
						tags = item['tags']

						icon = ICON.format(file=file)
						if keyword in tags and icon not in hit['icons']:
							hit['icons'].append(icon)
			return True
		return False

	def __parselimits(self):
		start	= None
		end		= datetime.today() if not self.limits["end"] else None
		formats	= ["%Y-%m-%d", "%Y-%m", "%Y"]

		for fmt in formats:
			try:
				if not start:
					start = datetime.strptime(self.limits["start"], fmt)

				if not end:
					end	= datetime.strptime(self.limits["end"], fmt).replace(month=12, day=31)
			except:
				pass

		return start, end

	def search(self, query):
		if query:
			datasource = DataSource(lang=self.lang)
			return datasource.search(query=query)
		return False

	def get(self, pageid):
		if pageid:
			datasource	= DataSource(lang=self.lang)
			entity		= datasource.get(pageid=pageid)

			if entity:
				self.name	= entity.get("name")
				self.text	= entity.get("text")
				self.images	= entity.get("images")
				self.limits	= {
					"start": entity.get("birth"),
					"end": entity.get("death")
				}
				return True
		return False

	def torender(self):
		self.__parse()
		self.__getpicture()
		self.__fill()
		self.__clean()

		return {
			"name": self.name,
			"hits": self.hits,
			"pic": self.pic,
			"limits": self.limits
		}