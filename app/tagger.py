from html.parser import HTMLParser


class Tagger(HTMLParser):
    def __init__(self):
        super(Tagger, self).__init__()
        self._has_title = False

    def handle_starttag(self, tag, attrs):
        if tag == 'h1':
            self._has_title = True

    def handle_data(self, data):
        if self._has_title:
            self.title = data
            self._has_title = False