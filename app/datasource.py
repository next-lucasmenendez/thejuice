import re
import wikipedia
from app.database import DB
from SPARQLWrapper import SPARQLWrapper, JSON

DBPEDIA="http://dbpedia.org/sparql"
DBTABLE="figures_en"

class DataSource:
	def __init__(self, lang="en"):
		self.lang = lang

	def __sparql(self, query):
		sparql = SPARQLWrapper(DBPEDIA)
		sparql.setQuery(query)
		sparql.setReturnFormat(JSON)

		return sparql.query().convert()

	def __getdbpedia(self, pageid):
		q = '''
			SELECT DISTINCT ?name ?birth ?death ?description ?id WHERE {{
				?person rdf:type dbo:Person . 
				?person dbo:wikiPageID {pageid} . 
				?person foaf:name ?name . 
				?person dbo:birthDate ?birth . 
				OPTIONAL{{?person dbo:deathDate ?death}} . 
			}} GROUP BY ?name
		'''.format(pageid=pageid)

		response	= self.__sparql(q)
		results		= response.get('results')
		if results:
			bindings = results.get('bindings')

			if bindings:
				item = {}
				result = bindings[0]

				for key in result.keys():
					item[key] = result[key]['value']

				return item
		return None

	def search(self, query):
		q = '''
		SELECT DISTINCT ?name ?id ?birth ?death WHERE {{
			?person rdf:type dbo:Person . 
			?person foaf:name ?name . 
			?person dbo:wikiPageID ?id . 
			?person dbo:birthDate ?birth . 
			OPTIONAL{{?person dbo:deathDate ?death}} . 
			FILTER contains(lcase(?name), "{query}").
		}} GROUP BY ?name
		'''.format(query=query)

		suggestions	= []
		response	= self.__sparql(q)
		results		= response['results']['bindings']

		ids = []
		for result in results:
			if result['id'] not in ids:
				ids.append(result['id'])

				item = {}
				for key in result.keys():
					item[key] = result[key]['value']

				suggestions.append(item)
		return suggestions

	def autosuggest(self, query):
		db = DB()
		return db.search(DBTABLE, "name", query)

	def get(self, pageid):
		db 		= DB()
		results = db.search(DBTABLE, "id", pageid)

		if results:
			item = results[0]
		else:
			item = self.__getdbpedia(pageid=pageid)

		if item:
			try:
				wikipedia.set_lang(self.lang)
				page = wikipedia.page(pageid=pageid)
				raw, images = page.content, page.images

				item["images"] = self.__getimages(images)
				item["text"] = self.__cleantext(raw)

				return item
			except Exception as e:
				print(e)
				return False

		return False

	def __cleantext(self, raw):
		#Delete all html tags from raw text
		text = re.sub('<[^<]+>', "", raw)
		text = re.sub('(\[(\d+|edit)\])', "", text)

		lines = []
		chars = 0
		for line in text.splitlines():
			if line.startswith("=") or not line:
				continue
			lines.append(line)
			chars += len(line)

		content = ""
		for line in lines:
			content += line
		return content

	def __getimages(self, images):
		# Filter images by extension
		results = []
		for img in images:
			found = re.search("(\.gif|\.png|\.jpg|\.jpeg)", img, re.IGNORECASE)
			if found:
				results.append(img)

		return results