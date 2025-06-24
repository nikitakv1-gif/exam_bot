import requests 
import re
import os

class ChatBot:

	def __init__(self, source_id, url, api_key):
		self.source_id = source_id
		self.url = url
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
	def upload_file(self, file_path, upload_url):
	    print(self, upload_url)

	    file_name = os.path.basename(file_path)
	    with open(file_path, "rb") as f:
	        files = [('file', ('file', f, 'application/octet-stream'))]
	        response = requests.post(upload_url, headers=self.headers, files=files)

	    print("Status:", response.status_code)
	    print("Text:", response.text)
	    if response.status_code == 200:
	        return response.json()['sourceId']
	    return None

	def upload_by_link(self, link):
		upload_url = 'https://api.chatpdf.com/v1/sources/add-url'

		data = {'url': upload_url}

		print(self.headers)
		response = requests.post(
		    upload_url, headers= self.headers, json=data)

		if response.status_code == 200:
		    return(response.json()['sourceId'])
		else:
		    print('Status:', response.status_code)
		    print('Error:', response.text)
		    return None