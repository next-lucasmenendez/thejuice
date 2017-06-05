import json

from functools import wraps

from flask import Flask
from flask import request
from flask import make_response

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


@app.route('/question', methods=["GET"])
@as_json
def question():
	query = request.form.get('query')
	lang = request.form.get('lang') or "en"




if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
