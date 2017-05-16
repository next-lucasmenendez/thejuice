import os
from datetime import datetime
from unidecode import unidecode
from functools import wraps

from flask import request
from flask import redirect
from flask import make_response
from flask import render_template


class Login:
	def tokenrequired(self, func):
		@wraps(func)
		def core(*args, **kwargs):
			authtoken = request.cookies.get('accesstoken')
			userid = request.cookies.get('userid')
			if not authtoken or not userid:
				return render_template('login.html')

			return func(*args, **kwargs)

		return core

	def login(self):
		if request.method == "POST":
			try:
				userid		= request.form['userid']
				accesstoken = request.form['accesstoken']
				name		= unidecode(request.form["name"]).split(" ")[0]
				email		= request.form['email']

				try:
					current_path = os.path.dirname(os.path.abspath(__file__))
					access_log = "%s/access.log" % current_path
					with open(access_log, "a") as fd:
						date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
						record = "[%s] ID: %s - Email: %s\n" % (date, userid, email)

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
			userid = request.cookies.get('userid')

			if accesstoken and userid:
				return make_response(redirect("/"))

			return render_template("login.html")

	def logout(self):
		resp = make_response(redirect("/login"))
		resp.set_cookie('accesstoken', '', expires=0)
		resp.set_cookie('userid', '', expires=0)

		return resp

	def expired(self):
		resp = make_response(redirect("/login"))
		resp.set_cookie('accesstoken', '', expires=0)
		resp.set_cookie('userid', '', expires=0)

		return resp