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
	def __init__(self, juicer=None):
		self.juicer = juicer
		self.text	= self.juicer.text
		if not self.juicer:
			return

		self.clean_text()

	def clean_text(self):
		if not self.text:
			return False

		lines = []
		chars = 0
		for line in self.text.splitlines():
			if line.startswith("=") or not line:
				continue
			lines.append(line)
			chars += len(line)

		content = ""
		for line in lines:
			content += line

		self.text = content

	def generate(self, min_length=MIN_LENGTH, max_length=MAX_LENGTH):
		if not self.text:
			return False

		datefinder	= Datefinder(self.text)
		dates 		= datefinder.results()
		limits		= sorted(dates[0:2], key=lambda l: l["datetime"])

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
			if limits[0]["datetime"] <= date <= limits[1]["datetime"]:
				hit = self.text[initial:final].strip()
				if max_length > len(hit) > min_length and hit not in hits and hit[0].isupper():
					hits.append(hit)
					results.append({
						'datetime': date,
						'date': datetime.strftime(date, format),
						'content': hit
					})

		hits = sorted(results, key=lambda date: date["datetime"])

		if hits[0]["datetime"] > dates[0]["datetime"]:
			fulldate	= dates[0]["datetime"]
			format 		= dates[0]["format"]
			date		= datetime.strftime(fulldate, format)
			hits.append({
				'datetime': fulldate,
				'date': date,
				'content': HITS_TEXT[self.juicer.lang]["start"].format(name=self.juicer.title, date=date)
			})

		if hits[len(hits) - 1]["datetime"] < dates[1]["datetime"]:
			fulldate	= dates[1]["datetime"]
			format		= dates[1]["format"]
			date		= datetime.strftime(fulldate, format)
			hits.append({
				'datetime': fulldate,
				'date': date,
				'content': HITS_TEXT[self.juicer.lang]["end"].format(name=self.juicer.title, date=date)
			})

		self.juicer.hits = sorted(hits, key=lambda hit: hit["datetime"])
		return True
