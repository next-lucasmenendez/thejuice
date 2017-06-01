import re
from datetime import datetime


class Datefinder:
	dmy_rgx	= "((\d{1}|\d{2})\ (%s)\ [12]\d{3})"
	my_rgx	= "((%s)\ [12]\d{3})"
	y_rgx	= "([12]\d{3})"

	default = "en"
	langs	= {
		"es": "Enero|Febrero|Marzo|Abril|Mayo|Junio|Julio|Agosto|Septiembre|Octubre|Noviembre|Diciembre",
		"en": "January|February|March|April|May|June|July|August|September|October|November|December"
	}

	def __init__(self, text, lang=None):
		self.text	= text
		self.lang	= lang if lang and lang in langs.keys() else self.default
		self.months	= self.langs[self.lang]
		
		self.dmy_rgx	= self.dmy_rgx % self.months
		self.my_rgx		= self.my_rgx % self.months

		self.matches = []
		self.match()

	def match(self):
		full_rgx	= "|".join([self.dmy_rgx, self.my_rgx, self.y_rgx])
		rgx			= re.compile(full_rgx, re.IGNORECASE)

		parsed_dates = []
		for match in rgx.finditer(self.text, re.IGNORECASE):
			start, end	= match.start(), match.end()
			raw_text	= self.text[start:end]

			date, format = self.parse_date(raw_text)

			if raw_text not in parsed_dates:
				parsed_dates.append(raw_text)
				self.matches.append({
					"start": start,
					"end": end,
					"raw": raw_text,
					"datetime": date,
					"format": format
				})

	def parse_date(self, raw_date):
		date	= None
		format	= ""
		formats	= [
			{
				"rgx": "%d de %B de %Y",
				"flag": 111
			},
			{
				"rgx": "%d %B %Y",
				"flag": 111,
			},
			{
				"rgx": "%B de %Y",
				"flag": 11
			},
			{
				"rgx": "%B %Y",
				"flag": 11
			},
			{
				"rgx": "%Y",
				"flag": 1
			}
		]
		for f in formats:
			try:
				date = datetime.strptime(raw_date, f["rgx"])
				format = f
				break
			except:
				pass

		return date, format

	def results(self):
		return self.matches
