from flask import request
from flask import redirect
from flask import render_template

from clients.client import Client

FB_ACCESSTOKEN = "EAACziQjfRpIBAKKSUMKapzKzA0eLY6i0ALm3XRPKGMHLut54WX0Ng9J0eMDuZAZAVZBE980QDyvTQXplcXvfyODZCJBO75sLjp85TfhidfcZBeyWg1EZAPtYYtPWoIQlZBdoVaBJZBreLmCFAaQv1sWcMOtW7HgTYgQQoNAAwR5VnwZDZD"  

class Facebook:
	def target(self, content):
		current_path	= os.path.dirname(os.path.abspath(__file__))
		raw_sentences	= content["raw_sentences"]
		sentences		= []
		for sentence in raw_sentences:
			sentences.append({
				"submitable":	True,
				"bot":			True,
				"content":		sentence
			})
		
		sentences_json		= "%s/bot_sentences.json" % current_path
		middle_sentences	= []
		with open(sentences_json, 'r', encoding='utf-8') as raw_content:
			middle_sentences	= json.load(raw_content)
			final_sentences		= []
			for sentence in sentences:
				final_sentences.append(sentence)	
				if len(middle_sentences):
					sentence_index	= randint(0, len(middle_sentences) - 1)
					middle_sentence	= middle_sentences.pop(sentence_index)
					if middle_sentence["question"]:
						final_sentences.append({
							"submitable":	False,
							"bot":			True,
							"content":		middle_sentence["question"]
						})

					final_sentences.append({
						"submitable":	False,
						"bot":			False,
						"content":		middle_sentence["answer"]
					})
				
		if len(final_sentences):
			sentences = final_sentences
		
		sentences.append({
			"submitable":	True,
			"bot":			True,
			"content":		"Check out original content here: %s" % content["url"]
		})

		contacts = super().contacts()
		if contacts:
			return render_template('facebook.html', sentences=sentences, contacts=contacts)

		return redirect("/")

'''
@app.route("/bot", methods=["GET"])
def bot_verification():
	return request.args['hub.challenge']

@app.route("/bot", methods=["POST"])
def bot_handle_msg():
	data	= request.json
	user_id	= data['entry'][0]['messaging'][0]['sender']['id']
	content	= data['entry'][0]['messaging'][0]['message']['text']

	if content == "start":
		content = "Hi! This is takethejuice Bot, what can I help you to learn today?"

	status_code, response = bot_send_message(user_id, content)
	print(response)
	return "Ok"

def bot_send_message(user_id, content):
	data = {
		"recipient":	{
			"id": user_id
		},
		"message":		{
			"text": content
		}
	}

	resp = requests.post("https://graph.facebook.com/v2.8/me/messages?access_token=" + FB_ACCESSTOKEN, json=data)
	return resp.status_code, resp.text if resp.status_code == 200 else "Ok"
'''
