import json
def update_tokens():
	with open('bots.json', 'r', encoding = 'utf-8') as file:
		bots = json.load(file)
	return bots