import os
import sys
import json

class Client:
	def contacts(self):
		current_path	= os.path.dirname(os.path.abspath(sys.argv[0]))
		contacts_json	= "%s/my_contacts.json" % current_path
		with open(contacts_json, 'r', encoding='utf-8') as raw_contacts:
			return json.load(raw_contacts)

		return False
