import json
from pathlib import Path


def update_tokens():
	with open('bots.json', 'r', encoding = 'utf-8') as file:
		bots = json.load(file)
	return bots

def upload_tokens(name, link):
    file_path = 'bots.json'
    
    try:
        if Path(file_path).exists():
            with open(file_path, 'r', encoding='utf-8') as file:
                bots = json.load(file)
        else:
            bots = {}
    except json.JSONDecodeError:
        bots = {}  # Если файл поврежден, начинаем с чистого листа
    
    name = " ".join(name)
    bots[name] = link
    
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(bots, file, ensure_ascii=False, indent=4)