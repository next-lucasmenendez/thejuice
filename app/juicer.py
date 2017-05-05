import re
import requests
import wikipedia
import xmltodict

from random import randint

DBPEDIA="http://lookup.dbpedia.org/api/search.asmx/PrefixSearch?QueryClass=&MaxHits=5&QueryString={query}"


class Juicer:
	def __init__(self, query=None, lang="en", force=False):
		self.query 	= query
		self.lang 	= lang
		self.force	= force
		self.opts	= []

		self.title 	= ""
		self.text 	= ""
		self.images = []
		self.image	= None

		if not query:
			return

		""" Set lang of searchs """
		if self.lang in wikipedia.languages():
			wikipedia.set_lang(self.lang)

	def check(self):
		if self.images:
			images = []
			needle = self.title.replace(" ", "_")

			for img in self.images:
				if re.search(needle, img, re.IGNORECASE):
					images.append(img)

			lenimages = len(images)
			if lenimages:
				picture = randint(0, lenimages - 1)
				self.images	= images
				self.image 	= images[picture]

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
							title = result["Label"]
							if result["Classes"]:
								classes = result["Classes"]["Class"]
								for c in classes:
									if c["Label"] == "person" and title not in suggested:
										suggested.append(title)
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
			self.opts = wikipedia.search(self.query)
		else:
			w = wikipedia.page(self.query, auto_suggest=True)

			self.title	= w.title
			self.text	= w.content
			self.images	= w.images
			return True

		return False
