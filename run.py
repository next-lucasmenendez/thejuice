import os
import json
import datetime

from functools import wraps

from flask import Flask
from flask import request
from flask import make_response
from flask import render_template
from flask import redirect

from app.parser import Parser
from app.extractor import Extractor
from app.template import Template


app	= Flask(__name__)


def as_json(func):
	@wraps(func)
	def core(*args, **kwargs):
		content, status = func(*args, **kwargs)
		json_encoded	= json.dumps(content)
		headers			= {"Content-Type": "application/json"}
		response		= make_response(json_encoded, status, headers)

		return response
	return core


@app.route("/", methods=["GET"])
def index():
	return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
@as_json
def login():
	data = request.get_json()
	name = data.get('name')
	email = data.get('email')

	if name and email:
		try:
			current_path = os.path.dirname(os.path.abspath(__file__))
			access_log = "%s/access.log" % current_path
			with open(access_log, "a") as fd:
				date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				record = "[{date}] Name: {name} - Email: {email}\n".format(
					date=date, name=name, email=email)

				fd.write(record)
		except:
			pass
		return {"success": True, "result": "Welcome {name}!".format(name=name)}, 200
	return {"success": False, "result": "No name and/or email provided."}, 400


@app.route('/link', methods=["POST"])
@as_json
def link():
	url		= request.form.get('url') or False
	lang	= request.form.get('lang') or 'english'
	number	= request.form.get('number') or 10
	if url:
		parser		= Parser()
		extractor	= Extractor(lang)

		title, html	= parser.parse(url)
		sentences	= extractor.getsentences(html, number)

		article = {
			"title": title,
			"sentences": sentences
		}

		return {"success": True, "result": article}, 200

	return {"success": False, "result": "No query provided."}, 400


@app.route('/download', methods=["POST"])
@as_json
def download():
	data		= request.get_json()
	title		= data.get('title') or False
	sentences	= data.get('sentences') or False
	design		= data.get('design') or 'nude'

	if title and sentences:
		template	= Template(design)
		url			= template.render(title, sentences)

		if url:
			return {"success": True, "result": url}, 200
		return {"success": False, "message": "Something was wrong creating output."}, 500

	return {"success": False, "message": "Bad request. More data required."}, 400


@app.route('/output/<string:query>')
def output(query):
	if query:
		try:
			template = "output/{}.html".format(query)
			return render_template(template)
		except Exception as e:
			print("Template not found")
			pass
	return redirect('/')

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
