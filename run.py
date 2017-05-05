from flask import Flask
from flask import request
from flask import redirect
from flask import render_template

from app.juicer import Juicer
from app.parser import Parser
from app.render import Render

app = Flask(__name__)

@app.route("/test/<string:query>", methods=["GET"])
def test(query):
	juicer = Juicer(query=query, lang="es")
	success = juicer.find()
	if success:
		parser 	= Parser(juicer)
		hits 	= parser.generate()

	return "HEY"

@app.route("/", methods=["GET"])
def search():
	return render_template('search.html')


@app.route("/pills", methods=["GET"])
def timeline():
	query	= request.args.get('query')
	force	= bool(request.args.get('force'))
	if query:
		juicer = Juicer(query=query, lang="es", force=force)
		success = juicer.find()
		if success:
			parser	= Parser(juicer)
			hits	= parser.generate()
			return render_template('timeline.html', title=juicer.title, picture=juicer.image, hits=hits)
		else:
			opts = juicer.opts
			return render_template('search.html', query=query, results=opts or None)

	return redirect('/')


@app.route("/download", methods=["GET"])
def formats():
	formats = ["infographic"]

	query	= request.args.get('query')
	format	= request.args.get('format')
	if query and format:
		if format in formats:
			juicer	= Juicer(query=query, lang="es", force=True)
			success	= juicer.find()

			if success:
				parser	= Parser(juicer)
				hits	= parser.generate()

				render = Render(
					title=juicer.title,
					images=juicer.images,
					hits=hits
				)
				render.fill()
				return render_template('download.html', query=query)
			else:
				return render_template('error.html', query=query)
		else:
			return render_template('soon.html', query=query, format=format)
	elif query:
		return redirect("/pills?query={}&format=True".format(query))

	return redirect('/')


if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
