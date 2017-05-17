import json

from flask import Flask
from flask import request
from flask import make_response
from flask import render_template
from functools import wraps

from app.login import Login
from app.juicer import Juicer
from app.parser import Parser
from app.render import Render

app		= Flask(__name__)
login	= Login()


def as_json(func):
	@wraps(func)
	def core(*args, **kwargs):
		content, status = func(*args, **kwargs)
		json_encoded	= json.dumps(content)
		headers			= {"Content-Type": "application/json"}
		response		= make_response(json_encoded, status, headers)

		return response
	return core


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
def index():
	return render_template('index.html')


@app.route("/search", methods=["POST"])
@as_json
def search():
	query = request.form.get("query")
	force = request.form.get("force") or False
	if query:
		juicer 	= Juicer(query=query, force=force)
		success = juicer.find()
		if success:
			parser	= Parser(juicer)
			success	= parser.generate()
			if success:
				return {"success": True, "result": juicer.torender()}, 200
			else:
				return {"success": False, "message": "Sorry... We could not find your request."}, 404
		else:
			if juicer.opts:
				return {"success": False, "options": juicer.opts}, 200
			else:
				return {"success": False, "message": "Sorry... We could not find your request."}, 404
	return {"success": False, "message": "No query provided"}, 400


@app.route('/download', methods=["POST"])
@as_json
def download():
	formats	= ["infographic"]
	data	= request.get_json()

	format_req	= data.get('format') or False
	character	= data.get('character') or False

	if character and format_req:
		if format_req in formats:
			character["fmt"] = format_req
			render 	= Render(**character)
			url 	= render.save()

			if url:
				return {"success": True, "result": url}, 200

			return {"success": False, "message": "Something was wrong creating output."}, 500
		return {"success": False, "message": "This format is not ready yet. But we're working on it!"}, 418
	return {"success": False, "message": "Bad request. More data required."}, 400


@app.route('/output/<string:query>')
def output(query):
	if query:
		template = "output/{}.html".format(query)
		return render_template(template)
	return render_template('error.html')


if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
