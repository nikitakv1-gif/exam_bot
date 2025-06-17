from PIL import Image
from gradio_client import Client, handle_file
import os
import pytesseract

# tesseract_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'OCR', 'tesseract.exe'))
# pytesseract.pytesseract.tesseract_cmd = tesseract_path

async def picture_response(update, img_path):
	text = None
	for i in range(3):
		try:
			text = pytesseract.image_to_string(Image.open(img_path).convert('L'), lang="rus")
			break
		except Exception as e:
			await update.message.reply_text(f"Ошибка распознавания попытка {i+1}/3. Ошибка: {e}")
			text = None

	try:
		os.remove(img_path)
	except OSError:
		pass
	try:
		os.remove('output.jpg')
	except OSError:
		pass

	print(text)
	return text




# from gradio_client import Client, handle_file

# client = Client("prithivMLmods/Multimodal-OCR")
# result = client.predict(
# 		model_name="Nanonets-OCR-s",
# 		text="Вопросы экзаменационные",
# 		image=handle_file('https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png'),
# 		max_new_tokens=1024,
# 		temperature=0.6,
# 		top_p=0.9,
# 		top_k=50,
# 		repetition_penalty=1.2,
# 		api_name="/generate_image"
# )
# print(result)