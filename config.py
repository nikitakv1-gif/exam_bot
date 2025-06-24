import json
def update_tokens():
	with open('bots.json', 'r', encoding = 'utf-8') as file:
		bots = json.load(file)
	return bots

def upload_tokens(name, link):
	with open('bots.json', 'a+', encoding = 'utf-8') as file:
		bots = json.load(file)
		bots[name] = link
		json.dump(bots)