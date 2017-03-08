# -*- coding: utf-8 -*-

import os
import re
import json
import requests

from random import randint
from datetime import datetime

from functools import wraps

from flask import Flask
from flask import request
from flask import url_for
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
			userid		= request.form['userid']
			accesstoken = request.form['accesstoken']
			name		= request.form['name'].encode('utf-8')
			email		= request.form['email']

			try:
				current_path	= os.path.dirname(os.path.abspath(__file__))
				access_log		= "%s/access.log" % current_path
				with open(access_log, "a") as fd:
					date	= datetime.now().strftime("%Y-%m-%d %H:%M:%S")
					record	= "[%s] ID: %s - Email: %s\n" % (date, userid, email)

					fd.write(record)
			except:
				pass

			resp = make_response(redirect('/'))
			resp.set_cookie('name', name)
			resp.set_cookie('accesstoken', accesstoken)
			resp.set_cookie('userid', userid)
			return resp
		except:
			return make_response(redirect("/login"))
	else:
		accesstoken = request.cookies.get('accesstoken')
		userid		= request.cookies.get('userid')
		
		if accesstoken and userid:
			return make_response(redirect("/"))

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

@app.route("/", methods=["GET"])
@tokenrequired
def index():
	return render_template('index.html')

@app.route("/preview", methods=["POST"])
@tokenrequired
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
@tokenrequired
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
			return target_facebook(content)
		elif method == "twitter":
			return target_twitter(content)
	
	return redirect('/') 

def target_facebook(content):
	current_path	= os.path.dirname(os.path.abspath(__file__))
	raw_sentences	= content["raw_sentences"]
	sentences		= []
	for sentence in raw_sentences:
		sentences.append({
			"submitable":	True,
			"bot":			True,
			"content":		sentence
		})
	
	sentences_json		= "%s/bot_sentences.json" % current_path
	middle_sentences	= []
	with open(sentences_json, 'r', encoding='utf-8') as raw_content:
		middle_sentences	= json.load(raw_content)
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
		"content":		"Check out original content here: %s" % content["url"]
	})
	return render_template('facebook.html', sentences=sentences)

def target_twitter(content):
	current_path	= os.path.dirname(os.path.abspath(__file__))
	raw_sentences	= content["raw_sentences"]
	keywords		= content["keywords"]
	sentences		= []
	hour			= 2
	for sentence in raw_sentences:
		words	= sentence.split(" ")
		tags	= []
		for word in words:
			if word in keywords:
				tags.append(word)

		sentences.append({
			"image":	False,
			"content":	sentence.lstrip(),
			"tags":		tags,
			"link":		False,
			"hour":		hour		
		})
		hour = hour + 6

	sentences.append({
		"image":	False,
		"content":	"Check out original content here",
		"tags":		[],
		"link":		content["url"],	
		"hour":		hour - 6	
	})

	contacts_json = "%s/my_contacts.json" % current_path
	with open(contacts_json, 'r', encoding='utf-8') as raw_contacts:
		contacts = json.load(raw_contacts)
		return render_template('twitter.html', tweets=sentences, contacts=contacts)

	return redirect("/")


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
		content = "Hi! This is takethejuice Bot, what can I help you to learn today?"

	status_code, response = bot_send_message(user_id, content)
	print(response)
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
	return resp.status_code, resp.text if resp.status_code == 200 else "Ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
