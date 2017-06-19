from urllib.request import urlopen
from app.tagger import Tagger


class Parser:
	def __init__(self):
		self.tagger = Tagger()

	def parse(self, url):
		html = urlopen(url).read().decode('utf8')
		self.tagger.feed(html)

		return self.tagger.title, html