import io
import os
import sys
import base64
import textwrap
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

class Related():
	content = ""
	output	= "image.png"
	topic	= None
	
	def __init__(self, content, output="image.png", topic=None):
		self.content	= content
		self.output		= output
		self.topic		= topic

	def get(self):
		try:
			return self.create()
		except Exception as err:
			raise err

	def create(self):
		try:
			margin, line_height, = 20, 40
			font_size, chars_per_line = 30, 37
			lines = textwrap.wrap(self.content, chars_per_line)

			width, height = 600, (margin * 2) + (line_height * len(lines))

			current_path	= os.path.dirname(os.path.abspath(sys.argv[0]))
			font_path		= "{}/font.ttf".format(current_path) 
			result_path		= "{}/{}".format(current_path, self.output)
	
			img		= Image.new("RGB", (width, height), (255, 255, 255))	
			font	= ImageFont.truetype(font_path, font_size)
			drawer	= ImageDraw.Draw(img)

			current = margin
			for line in lines:
				drawer.text((margin, current), line, font=font, fill=(0,0,0))
				current += line_height

			if self.topic:
				encoded_img = self.related()
				img_path	= io.BytesIO(encoded_img)
				rel_img		= Image.open(img_path)

				rel_img.thumbnail((width, width))
				rel_w, rel_h	= rel_img.size
				rel_x			= 0 if rel_w == width else int((width - rel_w)/2)
				size			= (width, rel_h + height)

				result = Image.new("RGB", size, (255,255,255))
				result.paste(rel_img, (rel_x, 0))
				result.paste(img, (0, rel_h))

				result.save(result_path, "PNG")
				return result_path

			img.save(result_path, "PNG")
		except Exception as err:
			print(err)

		return False

	def related(self):
		related_image = False

		bing_key1	= "970e8c5404c1475cb3ae0b21a710b76f"
		bing_key2	= "374ee3b915ab4cc3a4199c8d2149892c"

		query	= self.topic.lower().replace(" ", "+")
		url		= "https://api.cognitive.microsoft.com/bing/v5.0/images/search?q={}&count=5".format(query)
		try:
			results	= requests.get(url, headers={"Ocp-Apim-Subscription-Key": bing_key1})
			images	= results.json()['value']
			for image in images:
				src	= image['contentUrl']
				res	= requests.get(src)
				
				content_type = res.headers['Content-Type']
				if content_type.startswith("image/"):
					related_image = res.content
					break

		except Exception as err:
			print(err)

		return related_image
