# -*- coding: utf-8 -*-

import os
import re

from flask import Flask
from flask import request
from flask import redirect
from flask import render_template

from newspaper import Article

from app.clients.twitter import Twitter
from app.clients.facebook import Facebook
from app.auth.login import Login

app			= Flask(__name__)

login		= Login()
twitter		= Twitter()
facebook	= Facebook()

@app.route("/login", methods=["GET", "POST"])
def route_for_login(): 
	return login.login()

@app.route("/logout", methods=["GET"])
@login.tokenrequired
def route_for_logout():
	return login.logout()

@app.route("/logout/expired", methods=["GET"])
@login.tokenrequired
def route_for_expired():
	return login.expired()

@app.route("/", methods=["GET"])
@login.tokenrequired
def index():
	return render_template('index.html')

@app.route("/preview", methods=["POST"])
@login.tokenrequired
def preview():
	if request.form["url"]:
		url		= request.form["url"]
		article = Article(url=url, language='es')
		content = {}

		try:
			article.download()
			article.parse()

			content["title"]	= article.title
			content["url"]		= url 
			content["content"]	= article.text.strip(article.title)
			content["topimage"]	= article.top_image
			content["images"]	= article.images
			content["videos"]	= article.movies

			article.nlp()
			content["keywords"]		= article.keywords
			content["raw_keywords"]	= ",".join(article.keywords)

			valid_starters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z", "1","2","3","4","5","6","7","8","9","0", "¿", "¡"]
			summary = article.summary.strip(article.title)
			for char in summary:
				if char in valid_starters:
					break
				else:
					summary = summary[1:]

			content["summary"] = summary

			return render_template('preview.html', content=content)
		except Exception as e:
			print(e)
			return redirect('/')
		return redirect('/')
	else:
		return redirect('/')

@app.route("/targets", methods=["POST"])
@login.tokenrequired
def targets():
	title		= request.form["title"]
	summary		= request.form["summary"]
	url			= request.form["url"]
	keywords	= request.form["raw_keywords"].split(",")
	method		= request.form["method"]

	current_path	= os.path.dirname(os.path.abspath(__file__))
	template_file	= "{}.html".format(method)
	template_path	= "{}/templates/{}".format(current_path, template_file)
	if method and os.path.exists(template_path) and title and summary:
		raw_sentences = re.split("\r\n", summary)

		content = {
			"title":			title,
			"raw_sentences":	raw_sentences,
			"keywords":			keywords,
			"url":				url
		}

		if method == "facebook":
			return facebook.target(content)
		elif method == "twitter":
			return twitter.target(content)
	
	return redirect('/') 

@app.route("/send", methods=["POST"])
def send():
	errors = False
	platform = request.form.get('platform')
	if platform == "twitter":
		errors = twitter.send()

	if errors:
		return render_template('errors.html', errors=errors)
	else:
		return render_template('success.html')

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)
