# -*- coding: utf-8 -*-

import re

from functools import wraps

from flask import Flask
from flask import request
from flask import redirect
from flask import make_response
from flask import render_template

from newspaper import Article

app = Flask(__name__)

def tokenrequired(func):
	@wraps(func)
	def core(*args, **kwargs):
		authtoken	= request.cookies.get('accesstoken')
		userid		= request.cookies.get('userid')
		if not authtoken or not userid:
			return render_template('login.html', error="Login required")
		
		return func(*args, **kwargs)

	return core


@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		try:
			accesstoken = request.form['accesstoken']
			userid		= request.form['userid']

			resp = make_response(redirect('/'))
			resp.set_cookie('accesstoken', accesstoken)
			resp.set_cookie('userid', userid)
			return resp
		except:
			return make_response("/login")
	else:
		accesstoken = request.cookies.get('accesstoken')
		userid		= request.cookies.get('userid')
		
		if accesstoken and userid:
			return make_response("/")

		return render_template("login.html")

@app.route("/logout", methods=["GET"])
@tokenrequired
def logout():
	resp = make_response(redirect("/login"))
	resp.set_cookie('accesstoken', '', expires=0)
	resp.set_cookie('userid', '', expires=0)
	
	return resp

@app.route("/", methods=["GET", "POST"])
@tokenrequired
def index():
	if request.method == "GET":
	    return render_template('index.html')
	elif request.method == "POST":
		if request.form["url"]:
			article = Article(url=request.form["url"], language='es')
			content = {}

			try:
				article.download()
				article.parse()

				content["title"]	= article.title
				content["content"]	= article.text.strip(article.title)
				content["topimage"]	= article.top_image
				content["images"]	= article.images
				content["videos"]	= article.movies

				article.nlp()
				content["keywords"]	= article.keywords

				valid_starters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z", "1","2","3","4","5","6","7","8","9","0", "¿", "¡"]
				summary = article.summary.strip(article.title)
				for char in summary:
					if char in valid_starters:
						break
					else:
						summary = summary[1:]

				content["summary"] = summary

				return render_template('result.html', content=content)
			except:
				return render_template('error.html', error="Invalid content.")

			return render_template('index.html')
		else:
			return render_template('error.html', error="Introduce a valid url.")

@app.route("/parse", methods=["POST"])
@tokenrequired
def parse():
	title	= request.form["title"]
	summary	= request.form["summary"]
	method	= request.form["method"]

	if request.form["title"] and request.form["summary"] and request.form["method"]:
		sentences = re.split("\r\n", summary)

		return render_template('parse.html', sentences=sentences)
	
	return render_template('error.html', error="Ops... We have a problem. Try again later!") 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
