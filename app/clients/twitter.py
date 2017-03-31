import twitter
from flask import request
from flask import redirect
from flask import render_template

from app.clients.client import Client

TW_CONSUMER_KEY			= "r5SBP7Q05lDbGSzKQl4TYdtso"
TW_CONSUMER_SECRET		= "z2jbLfmRRgdO6TjdJQAktYJ9p5tmu9nxBPRilUvEGaAZ6QfJuX"
TW_ACCESS_TOKEN_KEY		= "838718301782044672-siqwtCUpTdf20ZP4tAecZC1fraCEiYa"
TW_ACCESS_TOKEN_SECRET	= "BVGCpaWDQEvFjx1INe3wpxlSqAREgFHc1l2lOei0Banhl"

class Twitter(Client):
	api = None

	def __init__(self):
		self.api = twitter.Api(
			consumer_key=TW_CONSUMER_KEY,
			consumer_secret=TW_CONSUMER_SECRET,
			access_token_key=TW_ACCESS_TOKEN_KEY,
			access_token_secret=TW_ACCESS_TOKEN_SECRET
		)


	def target(self, content):
		raw_sentences	= content["raw_sentences"]
		keywords		= content["keywords"]
		sentences		= []
		hour			= 2

		#from related.related import Related

		count	= 0
		for sentence in raw_sentences:
			words	= sentence.split(" ")
			tags	= []
			for word in words:
				if word in keywords:
					tags.append(word)

			tweet	= sentence.lstrip()
			tagsraw	= "#{}".format(" #".join(tags)) if tags else ""
			full	= "{} {}".format(tweet, tagsraw)

			#rel_img		= Related(tweet, "tweet%s.png" % count, "+".join(tags))	
			#rel_pagh	= rel_img.get()
			#count += 1

			sentences.append({
				"image":	False,
				"content":	tweet,
				"tags":		tags,
				"link":		False,
				"hour":		hour,
				"full":		full
			})
			hour = hour + 6

		sentences.append({
			"image":	False,
			"content":	"Check out original content here",
			"tags":		[],
			"link":		content["url"],	
			"hour":		hour - 6,
			"full":		"Check out original content here {}".format(content['url'])
		})

		contacts = super().contacts()
		if contacts:
			return render_template('twitter.html', tweets=sentences, contacts=contacts)

		return redirect("/")

	def send(self):
		contacts	= request.form.getlist('contacts')
		tweets		= request.form.getlist('tweets')

		errors = []
		for content in tweets:
			for contact in contacts:
				try:
					self.api.PostDirectMessage(text=content, screen_name=contact)
				except twitter.error.TwitterError as err:
					message = err.message[0]['message']
					error = {
						"user":			contact,
						"exception":	message
					}

					if error not in errors:
						errors.append(error)

		return errors
