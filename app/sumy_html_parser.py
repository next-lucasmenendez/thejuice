from html.parser import HTMLParser


class SumyHtmlParser(HTMLParser):
    def __init__(self):
        super(SumyHtmlParser, self).__init__()
        self._has_title = False

    def handle_starttag(self, tag, attrs):
        if tag == 'h1':
            self._has_title = True

    def handle_data(self, data):
        if self._has_title:
            self.title = data
            self._has_title = False
