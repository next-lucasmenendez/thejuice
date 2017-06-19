import os
import sys
import json

from polyglot.text import Text

from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

EMOJISINDEX="{base}/static/assets/emojis_english.json"
ICONSINDEX="{base}/static/assets/icons_english.json"
ICONFILE="/static/icons/{file}"


class Extractor:
	def __init__(self, lang='english'):
		self.lang 		= lang
		self.stemmer	= Stemmer(self.lang)
		self.summarizer	= Summarizer(self.stemmer)

		self.summarizer.stop_words = get_stop_words(self.lang)

	def __getkeywords(self, sentences):
		results = []
		for content in sentences:
			lang = 'en' if self.lang != 'spanish' else 'es'
			blob = Text(content, hint_language_code=lang)

			keywords = []
			for word, pos in blob.pos_tags:
				if pos == "VERB" or pos == "NOUN" or pos == "PROPN":
					keywords.append(word.lower())

			results.append({
				"content": content,
				"keywords": keywords
			})

		return results

	def __getemojis(self, sentences):
		main_path	= os.path.realpath(sys.argv[0])
		base		= os.path.dirname(main_path)
		index		= EMOJISINDEX.format(base=base)

		with open(index) as fd:
			emojis = json.loads(fd.read())

			results = []
			for sentence in sentences:
				if 'emojis' not in sentence.keys():
					sentence['emojis'] = []

				for keyword in sentence.get('keywords'):
					for alias in emojis:
						emoji = emojis.get(alias)

						if keyword in emoji.get('keywords'):
							sentence['emojis'].append(emoji.get('char'))
				results.append(sentence)
		return sentences

	def __geticons(self, sentences):
		main_path	= os.path.realpath(sys.argv[0])
		base		= os.path.dirname(main_path)
		index		= ICONSINDEX.format(base=base)

		with open(index) as fd:
			icons = json.loads(fd.read())

			results = []
			for sentence in sentences:
				if 'icons' not in sentence.keys():
					sentence['icons'] = []

				for keyword in sentence.get('keywords'):
					for icon in icons:
						if keyword in icon.get('tags'):
							file = ICONFILE.format(file=icon.get('icon'))
							sentence['icons'].append(file)
				results.append(sentence)
		return sentences

	def getsentences(self, html, number=10):
		sentences = []
		parser = HtmlParser.from_string(html, "", Tokenizer(self.lang))

		for sentence in self.summarizer(parser.document, number):
			sentences.append(str(sentence))

		sentences = self.__getkeywords(sentences)
		sentences = self.__getemojis(sentences)
		sentences = self.__geticons(sentences)
		return sentences