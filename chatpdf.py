import requests 
import re

class ChatBot:

	def __init__(self, source_id, url, api_key, upload_url):
		self.source_id = source_id
		self.url = url
		self.upload_url = upload_url
		self.api_key = api_key
		self.headers = headers = {
								    "x-api-key": api_key,
								    "Content-Type": "application/json",
								}

	def send_message(self, message):
		data = {
				  "sourceId": self.source_id,
				  "messages": [
				    {
				      "role": "user",
				      "content": message
				    }
				  ]
				}
		if self.url == 'url':
			return "Пожалуйста выберете экзамен"
		answer = requests.post(self.url, headers = self.headers, json = data)
		content = answer.json()['content']
		# chars_to_escape = r'_*[]()~`>#+-=|{}.!'
		# for char in chars_to_escape:
		# 	content = content.replace(char, f'\\{char}')
		return content
	def upload_file(self, file):
		if self.url_upload == 'url_upload':
			return "Пожалуйста выберете экзамен"
		files = [('file', ('file', open(file, 'rb'), 'application/octet-stream'))]
		answer = requests.post(self.upload_url, headers = headers, files = files)

		return answer.json()['sourceId']