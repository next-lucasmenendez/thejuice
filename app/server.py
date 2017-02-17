import re
import newspaper

from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "GET":
	    return render_template('index.html')
	elif request.method == "POST":
		if request.form["url"]:
			url		= request.form["url"]
			website	= newspaper.build(url, memoize_articles=False)
		
			if website.articles:
				article = website.articles[0]
				content = {}
				try:
					article.download()
					article.parse()

					content["title"]	= article.title
					content["content"]	= article.text

					article.nlp()
					content["summary"]	= article.summary
					content["keywords"]	= article.keywords

					return render_template('result.html', content=content)
				except:
					return render_template('error.html', error="Invalid content.")

			return render_template('index.html')
		else:
			return render_template('error.html', error="Introduce a valid url.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
