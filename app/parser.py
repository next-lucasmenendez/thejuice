# -*- coding: utf-8 -*-

from datetime import datetime
from app.datefinder import Datefinder

MIN_LENGTH	= 60
MAX_LENGTH	= 300
HITS_TEXT	= {
	"en": {
		"start": "{name} was born in {date}",
		"end": "{name} died in {date}"
	},
	"es": {
		"start": "{name} nació en {date}",
		"end": "{name} murió en {date}"
	}
}


class Parser:
	def __init__(self, text=None, start=None, end=None, lang="en"):
		self.text	= text
		self.start	= start
		self.end	= end
		self.lang 	= lang
		if not text or not start or not end:
			return

	def parse(self, min_length=MIN_LENGTH, max_length=MAX_LENGTH):
		if not self.text:
			return False

		datefinder	= Datefinder(self.text)
		dates 		= datefinder.results()

		hits 	= []
		results = []
		for d in dates:
			initial, final = d["start"], d["end"]
			while 1:
				char = self.text[initial]
				if char == ".":
					initial += 1
					break
				else:
					initial -= 1

			while 1:
				if final < len(self.text):
					char = self.text[final]
					final += 1
					if char == ".":
						break
				else:
					break

			date 	= d["datetime"]
			format	= d["format"]
			if self.start <= date <= self.end:
				hit = self.text[initial:final].strip()
				if max_length > len(hit) > min_length and hit not in hits and hit[0].isupper():
					hits.append(hit)
					results.append({
						'datetime': date,
						'date': datetime.strftime(date, format["rgx"]),
						'format': format,
						'content': hit
					})

		return sorted(results, key=lambda hit: hit["datetime"])