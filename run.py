import json
import os

from functools import wraps
from datetime import datetime

from flask import Flask
from flask import request
from flask import redirect
from flask import make_response
from flask import render_template

from app.juicer import Juicer
from app.parser import Parser
from app.render import Render
from app.datasource import DataSource

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


@app.route("/search/<string:query>", methods=["GET"])
@as_json
def search(query):

	lang = request.args.get('lang') or "en"
	try:
		#juicer 	= Juicer(query=query, lang=lang)
		#results	= juicer.find()

		datasource	= DataSource(lang=lang)
		results		= datasource.search(query=query)
		status 		= 200 if results else 404

		return {"success": True, "results": results}, status
	except:
		pass

	return {"success": False, "message": "Something was wrong..."}, 500

@app.route("/get/<int:pageid>", methods=["GET"])
@as_json
def get(pageid):
	datasource = DataSource()
	entity = datasource.get(pageid=pageid)

	return {"success": True, "content": entity}, 420


@app.route("/review", methods=["POST"])
@as_json
def review():
	query	= request.form.get("query")
	lang 	= request.form.get("lang") or "en"

	if query:
		juicer = Juicer(query=query, lang=lang, force=True)
		try:
			success = juicer.get()
			if not success:
				raise

			parser	= Parser(juicer)
			success	= parser.generate()
			if success:
				return {"success": True, "result": juicer.torender()}, 200
			else:
				return {"success": False, "message": "Sorry... We could not find your request."}, 404
		except Exception as e:
			print(e)
			return {"success": False, "message": "Sorry... We could not find your request."}, 404
	return {"success": False, "message": "No query provided"}, 400


@app.route('/download', methods=["POST"])
@as_json
def download():
	data	= request.get_json()

	design		= data.get('design') or False
	character	= data.get('character') or False

	if character and design:
		character["design"] = design
		render 	= Render(**character)
		url 	= render.save()
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
