import json
import os
import datetime
import smtplib
import threading

from functools import wraps

from flask import Flask
from flask import request
from flask import make_response
from flask import render_template
from flask import redirect

from app.article import Article
from app.render import Render

app	= Flask(__name__)
app.config.from_pyfile('config.py')


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


@app.route('/validate', methods=['POST'])
@as_json
def validate():
	data = request.get_json()
	student_email = data.get('studentEmail')
	teacher_email = data.get('teacherEmail')
	title = data.get('title')
	questions = data.get('questions')

	if student_email and teacher_email and title:
		correct_answers = 0
		questions_text = ''
		for question in questions:
			if question['select'] == question['correct']:
				correct_answers += 1
			questions_text += """{0}
Student answer: {1}
Correct answer: {2}

""".format(question['question'], question['select'], question['correct'])

		summary = correct_answers*100/len(questions)
		body = """Hi!

{0} has just completed the test about {1} created with theJuice.

Here you have the results:

Success rate: {2}%
Correct answers: {3}
Failed answers: {4}

Questions / Answers:

{5}""".format(student_email, title, summary, correct_answers, len(questions)-correct_answers, questions_text)

		try:
			thread_email_teacher = threading.Thread(target=send_mail, kwargs={
				'email_from': teacher_email,
				'email_to': student_email,
				'subject': 'One student has answered a Trivia',
				'content': body
			})
			thread_email_student = threading.Thread(target=send_mail, kwargs={
				'email_from': student_email,
				'email_to': teacher_email,
				'subject': 'You have answered a Trivia!',
				'content': body
			})
			thread_email_teacher.start()
			thread_email_student.start()

			return {"success": True, "message": "Emails sent.", "score": summary}, 200
		except Exception:
			return {"success": False, "message": "Server error. Error when send email."}, 500

	return {"success": False, "message": "Bad request. More data required."}, 400


def send_mail(email_from, email_to, subject, content):
	template = "From: Noa <{frm}>\nTo: {to}\nSubject: {subject}\n\n{message}"
	try:
		host, port = app.config.get('SMTP_ADDRESS'), app.config.get("SMTP_PORT")
		server = smtplib.SMTP(host=host, port=port)

		server.ehlo()
		server.starttls()

		username, password = app.config.get('SMTP_USERNAME'), app.config.get('SMTP_PASSWORD')
		server.ehlo()
		server.login(username, password)

		message = template.format(frm=email_from, to=email_to, message=content, subject=subject)
		server.sendmail(email_from, email_to, message)

		server.quit()
	except smtplib.SMTPException as err:
		print(err)
		raise err


if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
