import json

from flask import Flask
from flask import request
from flask import redirect
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


'''
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
'''

@app.route("/", methods=["GET"])
def index():
	return render_template('index.html')

@app.route("/search", methods=["POST"])
@as_json
def search():
	query = request.form.get("query")
	force = request.form.get("force") or False
	if query:
		juicer 	= Juicer(query=query, lang="es", force=force)
		success = juicer.find()
		if success:
			parser	= Parser(juicer)
			success	= parser.generate()
			if success:
				return {"success": True, "result": juicer.torender()}, 200
			else:
				return {"success": False, "message": "Not found"}, 404
		else:
			return {"success": False, "options": juicer.opts}, 200
	return {"success": False, "message": "No query provided"}, 400

'''
@app.route("/api/pills", methods=["GET"])
def timeline():
	query	= request.args.get('query')
	force	= bool(request.args.get('force'))
	if query:
		juicer = Juicer(query=query, lang="es", force=force)
		success = juicer.find()
		if success:
			parser	= Parser(juicer)
			success	= parser.generate()
			if success:
				#return render_template('preview.html', title=juicer.title, picture=juicer.pic, hits=juicer.hits)
				return juicer.torender()
			return render_template('error.html', query=query)
		else:
			opts = juicer.opts
			return render_template('search.html', query=query, results=opts or None)

	return redirect('/')


@app.route("/api/output", methods=["GET"])
def formats():
	fmts = ["infographic"]

	query	= request.args.get('query')
	fmt		= request.args.get('format')
	if query and format:
		if fmt in fmts:
			juicer	= Juicer(query=query, lang="es", force=True)
			success	= juicer.find()

			if success:
				parser	= Parser(juicer)
				success = parser.generate()
				if success:
					data = juicer.torender()
					data["fmt"] = fmt

					render	= Render(**data)
					url		= render.save()

					if url:
						return redirect(url)

			return render_template('error.html', query=query)
		else:
			return render_template('soon.html', query=query, format=fmt)
	elif query:
		return redirect("/pills?query={}&format=True".format(query))

	return redirect('/')

@app.route('/output/<string:query>')
def output(query):
	if query:
		template = "output/{}.html".format(query)
		return render_template(template)
	return render_template('error.html')
'''

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
