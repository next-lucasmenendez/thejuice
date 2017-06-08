import json
import os
import datetime

from functools import wraps

from flask import Flask
from flask import request
from flask import make_response
from flask import render_template
from flask import redirect

from app.article import Article
from app.render import Render

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
				record = "[{date}] Name: {name} - Email: {email}\n".format(
					date=date, name=name, email=email)

				fd.write(record)
		except:
			pass
		return {
					"success": True,
					"result": "Welcome {name}!".format(name=name)
				}, 200
	return {"success": False, "result": "No name and/or email provided."}, 400


@app.route('/question', methods=["POST"])
@as_json
def search():
	query = request.form.get('query') or False
	lang = request.form.get('lang') or "en"

	if query:

		# Retrieve the trivia sentences
		article = Article(title=query, lang=lang)
		trivia_sentences = article.generate_trivia_sentences(lang=lang)

		questions = {
			'title': trivia_sentences[0]['title'],
			'url': trivia_sentences[0]['url'],
			'questions': []
		}
		for sentence in trivia_sentences:
			question = {
				'question': sentence['question'],
				'answers': [
					{
						'name': a,
						'correct': False
					} for a in sentence['similar_words'][0:3]
				]
			}
			question['answers'].append({'name': sentence['answer'], 'correct': True})
			question['answers'] = sorted(question['answers'], key=lambda answer: answer['name'])
			questions['questions'].append(question)

		return {"success": True, "result": questions}, 200

	return {"success": False, "result": "No query provided."}, 400


@app.route('/download', methods=["POST"])
@as_json
def download():
	data = request.get_json()
	result = data.get('result') or False
	email = data.get('email') or False

	if result and email:
		result['email'] = email
		render = Render(**result)
		url = render.save()
		if url:
			return {"success": True, "result": url}, 200

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
