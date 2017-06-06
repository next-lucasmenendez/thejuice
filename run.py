import json
import os
import datetime

from functools import wraps

from flask import Flask
from flask import request
from flask import make_response
from flask import render_template

from app.article import Article

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
	data 	= request.get_json()
	name 	= data.get('name')
	email	= data.get('email')

	if name and email:
		try:
			current_path = os.path.dirname(os.path.abspath(__file__))
			access_log = "%s/access.log" % current_path
			with open(access_log, "a") as fd:
				date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				record = "[{date}] Name: {name} - Email: {email}\n".format(date=date, name=name, email=email)

				fd.write(record)
		except:
			pass
		return {"success": True, "result": "Welcome {name}!".format(name=name)}, 200
	return {"success": False, "result": "No name and/or email provided."}, 400


@app.route('/question', methods=["POST"])
@as_json
def search():
	query = request.form.get('query') or False
	lang = request.form.get('lang') or "en"

	if query:

		# Retrieve the trivia sentences
		questions = []
		article = Article(title=query, lang=lang)
		questions = questions + article.generate_trivia_sentences(lang=lang)

		return {"success": True, "results": questions}, 200

	return {"success": False, "result": "No query provided."}, 400


@app.route('/verify', methods=["POST"])
@as_json
def verify():
	pass


if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
