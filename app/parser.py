import re

from urllib.request import Request
from urllib.request import urlopen
from polyglot.detect import Detector

from app.tagger import Tagger


class Parser:
	def __init__(self):
		self.tagger = Tagger()

	def __cleanhtml(self, html):
		regex	= re.compile('<.*?>')
		raw		= re.sub(regex, '', html)

		return raw

	def __detectlang(self, html):
		try:
			raw = self.__cleanhtml(html)
			detector = Detector(raw)

			return detector.language.name.lower()
		except:
			return 'english'

	def parse(self, url):
		req		= Request(url=url, headers={'User-Agent': 'Mozilla/5.0'})
		html	= urlopen(req).read().decode('utf8')
		self.tagger.feed(html)

		lang = self.__detectlang(html)
		return self.tagger.title, html, lang