# -*- coding: utf-8 -*-

import os
import re
import json
import requests

from random import randint

from functools import wraps

from flask import Flask
from flask import request
from flask import redirect
from flask import make_response
from flask import render_template

from newspaper import Article

ACCESS_TOKEN = "EAACziQjfRpIBAKKSUMKapzKzA0eLY6i0ALm3XRPKGMHLut54WX0Ng9J0eMDuZAZAVZBE980QDyvTQXplcXvfyODZCJBO75sLjp85TfhidfcZBeyWg1EZAPtYYtPWoIQlZBdoVaBJZBreLmCFAaQv1sWcMOtW7HgTYgQQoNAAwR5VnwZDZD"  
app = Flask(__name__)

def tokenrequired(func):
	@wraps(func)
	def core(*args, **kwargs):
		authtoken	= request.cookies.get('accesstoken')
		userid		= request.cookies.get('userid')
		if not authtoken or not userid:
			return render_template('login.html')
		
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
			return make_response(redirect("/login", error="Session expired. Please relogin."))
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

@app.route("/logout/expired", methods=["GET"])
@tokenrequired
def expired():
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
			except Exception as e:
				return render_template('index.html', error="Invalid content.")

			return render_template('index.html')
		else:
			return render_template('index.html', error="Introduce valid url.")

@app.route("/parse", methods=["POST"])
@tokenrequired
def parse():
	title	= request.form["title"]
	summary	= request.form["summary"]
	url		= request.form["url"]
	method	= request.form["method"]

	if request.form["title"] and request.form["summary"] and request.form["method"]:
		sentences		= []
		raw_sentences	= re.split("\r\n", summary)
		for sentence in raw_sentences:
			sentences.append({
				"submitable":	True,
				"bot":			True,
				"content":		sentence
			})
		
		current_path		= os.path.dirname(os.path.abspath(__file__))
		sentences_json		= "%s/bot_sentences.json" % current_path
		middle_sentences	= []
		with open(sentences_json, 'r') as raw_content: #as fd:
#			raw_content			= fd.read()
			middle_sentences        = json.load(raw_content)
			final_sentences		= []
			for sentence in sentences:
				final_sentences.append(sentence)	
				if len(middle_sentences):
					sentence_index	= randint(0, len(middle_sentences) - 1)
					middle_sentence	= middle_sentences.pop(sentence_index)
					if middle_sentence["question"]:
						final_sentences.append({
							"submitable":	False,
							"bot":			True,
							"content":		middle_sentence["question"]
						})

					final_sentences.append({
						"submitable":	False,
						"bot":			False,
						"content":		middle_sentence["answer"]
					})
				

		if len(final_sentences):
			sentences = final_sentences
		
		sentences.append({
			"submitable":	True,
			"bot":			True,
			"content":		"Check out original content here: %s" % url
		})
		return render_template('parse.html', sentences=sentences)
	
	return render_template('index.html', error="Ops... We have a problem. Try again later!") 

@app.route("/send", methods=["POST"])
def send():
	return render_template('success.html')

@app.route("/bot", methods=["GET"])
def bot_verification():
	return request.args['hub.challenge']

@app.route("/bot", methods=["POST"])
def bot_handle_msg():
	data	= request.json
	user_id	= data['entry'][0]['messaging'][0]['sender']['id']
	content	= data['entry'][0]['messaging'][0]['message']['text']

	
	if content == "start":
		bot_send_message(user_id, "Hi! This is takethejuice Bot, what can I help you to learn today?")
	else:
		bot_send_message(user_id, content)

	return "Ok"

def bot_send_message(user_id, content):
	data = {
		"recipient":	{
			"id": user_id
		},
		"message":		{
			"text": content
		}
	}
	resp = requests.post("https://graph.facebook.com/v2.8/me/messages?access_token=" + ACCESS_TOKEN, json=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
