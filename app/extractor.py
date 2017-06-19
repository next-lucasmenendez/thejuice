from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


class Extractor:
	def __init__(self, lang='english'):
		self.lang 		= lang
		self.stemmer	= Stemmer(self.lang)
		self.summarizer	= Summarizer(self.stemmer)

		self.summarizer.stop_words = get_stop_words(self.lang)

	def getsentences(self, html, number=10):
		sentences = []
		parser = HtmlParser.from_string(html, "", Tokenizer(self.lang))

		for sentence in self.summarizer(parser.document, number):
			sentences.append(str(sentence))

		return sentences