import re
import requests
from SPARQLWrapper import SPARQLWrapper, JSON

DBPEDIA="http://dbpedia.org/sparql"
WIKIPEDIA="http://{lang}.wikipedia.org/w/api.php"

class DataSource:
	def __init__(self, lang="en"):
		self.lang = lang

	def search(self, query):
		q = '''
		SELECT DISTINCT ?name ?birth ?death ?description ?id WHERE {{
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

			endpoint	= WIKIPEDIA.format(lang=self.lang)
			data		= {
				"action": "parse",
				"format": "json",
				"prop": "text|images",
				"pageid": pageid
			}

			res = requests.get(endpoint, params=data)
			if res.status_code == requests.codes.ok:
				parse	= res.json()['parse']
				raw		= parse['text']['*']

				item["images"]	= self.__getimages(parse['images']),
				item["text"]	= self.__cleantext(raw)
				return item

		return False

	def __cleantext(self, raw):
		#Delete all html tags from raw text
		text = re.sub('<[^<]+>', "", raw)
		text = re.sub('(\[(\d+|edit)\])', "", text)

		return text

	def __getimages(self, images):
		# Filter images by extension
		queries = []
		for img in images:
			found = re.search("(\.gif|\.png|\.jpg|\.jpeg)", img, re.IGNORECASE)
			if found:
				filename = "File:{img}".format(img=img)
				queries.append(filename)

		#Setting Wikipedia Api Request
		endpoint	= WIKIPEDIA.format(lang=self.lang)
		query		= "|".join(queries)
		data		= {
			"action": "query",
			"format": "json",
			"prop": "imageinfo",
			"titles": query,
			"iiprop": "url"
		}

		images = []
		try:
			req = requests.get(endpoint, params=data)
			if req.status_code is requests.codes.ok:
				res		= req.json()
				pages	= res["query"]["pages"]

				for page in pages.values():
					image = page["imageinfo"][0]["url"]
					images.append(image)
		except Exception as e:
			print(e)
			pass

		return images