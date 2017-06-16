import os
import sys
import smtplib
from configparser import ConfigParser

class Notice:
	def __init__(self):
		main_path = os.path.realpath(sys.argv[0])
		path, runfile = os.path.split(main_path)

		config	= ConfigParser()
		file	= '%s/config.ini' % path

		config.read(file)
		self.host 		= config.get('mail', 'host')
		self.port 		= config.get('mail', 'port')
		self.username	= config.get('mail', 'username')
		self.password	= config.get('mail', 'password')
		self.admin		= config.get('mail', 'admin')

	def notify(self, content):
		template = "From: History [theJuice] <{frm}>\nTo: Admin <{to}>\nSubject: Something was wrong.\n\n{message}"
		try:
			server = smtplib.SMTP(host=self.host, port=self.port)

			server.ehlo()
			server.starttls()

			server.ehlo()
			server.login(self.username, self.password)

			message = template.format(frm=self.username, to=self.admin, message=content)
			server.sendmail(self.username, self.admin, message)

			server.quit()
		except smtplib.SMTPException as err:
			raise err