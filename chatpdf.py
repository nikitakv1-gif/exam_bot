import requests 

class ChatBot:

	def __init__(self, source_id, url, api_key):
		self.source_id = 'cha_' + source_id
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
		print(data)
		answer = requests.post(self.url, headers = self.headers, json = data)
		if answer.status_code == 200:
		    print('Result:', answer.json()['content'])
		else:
		    print('Status:', answer.status_code)
		    print('Error:', answer.text)
		return answer.json()['content']
