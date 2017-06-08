import re
import wikipedia
from SPARQLWrapper import SPARQLWrapper, JSON

DBPEDIA="http://dbpedia.org/sparql"

class DataSource:
	def __init__(self, lang="en"):
		self.lang = lang

	def search(self, query):
		q = '''
		SELECT DISTINCT ?name ?id WHERE {{
			?person rdf:type dbo:Person . 
			?person foaf:name ?name . 
			?person dbo:wikiPageID ?id . 
			FILTER contains(lcase(?name), "{query}").
		}} GROUP BY ?name
		'''
		sparql = SPARQLWrapper(DBPEDIA)
		sparql.setQuery(q.format(query=query))
		sparql.setReturnFormat(JSON)

		suggestions	= []
		response	= sparql.query().convert()
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

	def get(self, pageid):
		q = '''
			SELECT DISTINCT ?name ?birth ?death ?description ?id WHERE {{
				?person rdf:type dbo:Person . 
				?person dbo:wikiPageID {pageid} . 
				?person foaf:name ?name . 
				?person dbo:birthDate ?birth . 
				OPTIONAL{{?person dbo:deathDate ?death}} . 
			}} GROUP BY ?name
		'''
		sparql = SPARQLWrapper(DBPEDIA)
		sparql.setQuery(q.format(pageid=pageid))
		sparql.setReturnFormat(JSON)

		response = sparql.query().convert()
		results = response['results']['bindings']
		if results:
			item	= {}
			result	= results[0]

			for key in result.keys():
				item[key] = result[key]['value']

			try:
				wikipedia.set_lang(self.lang)
				page = wikipedia.page(pageid=pageid)
				raw, images = page.content, page.images

				item["images"]	= self.__getimages(images)
				item["text"]	= self.__cleantext(raw)
			except Exception as e:
				print(e)
				return False
			return item

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