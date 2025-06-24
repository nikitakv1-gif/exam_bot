import logging
import json
from chatpdf import ChatBot
import json 
from config import update_tokens, upload_tokens
import os
from dotenv import load_dotenv
from picture_work import picture_response

from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)


url = 'https://api.chatpdf.com/v1/chats/message'

url_upload = 'https://api.chatpdf.com/v1/sources/add-file'

load_dotenv()

api_key = os.getenv('CHATPDF_API_KEY')  
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

chat = ChatBot('sourse_id', 'url', api_key)


def exam_keyboard():
	
	keyboard = [[ KeyboardButton(i) for i in update_tokens().keys()], ['Загрузить новый файл']]

	reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard = True)

	return reply_markup

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
	user = update.effective_user

	await update.message.reply_text(
		f'Привет, выбери текущий экзамен',
		reply_markup = exam_keyboard())

async def ans(update: Update, context: ContextTypes.DEFAULT_TYPE):
	global chat
	bots = update_tokens()
	if update.message.text not in bots.keys():
		text = chat.send_message(update.message.text + """ Проанализируй документ и выполни все указанные теоретические и практические задания, если они присутствуют.
														   Если задание теоретическое — дай краткое, но полное определение, объясни суть и приведи нужные формулы в человекочитаемом виде.
														   Если задание практическое — реши задачу пошагово, покажи промежуточные вычисления и финальный ответ.
														   Если теоретическое и практическое вместе — сначала теория, потом решение.
														   Ничего не придумывай: если задачи нет — не выдумывай. Отвечай только на явно поставленные вопросы.
														   Формулы пиши в обычном текстовом виде (не LaTeX, без спецсимволов).
														   Не пропускай ни один пункт задания. В ответах не используй Маркдаун, но можешь использовать смайлики для понятного оформления""")
		await update.message.reply_text(text)
	elif update.message.text in bots.keys():
		await update.message.reply_text(
			"Экзамен выбран, задавайте вопросы",
			reply_markup = exam_keyboard())

		chat = ChatBot(bots[update.message.text], url, api_key)


async def pic(update: Update, context: ContextTypes.DEFAULT_TYPE):
	await update.message.reply_text("Обрабатываю фотографию!")
	if update.message.photo != ():
		f = update.message.photo[-1].file_id
		new_file = file = await context.bot.get_file(f)
		file = await new_file.download_to_drive()
		text_question = await picture_response(update, file)
		if text_question is not None:
			text = chat.send_message(text_question + """ Проанализируй документ и выполни все указанные теоретические и практические задания, если они присутствуют.
														   Если задание теоретическое — дай краткое, но полное определение, объясни суть и приведи нужные формулы в человекочитаемом виде.
														   Если задание практическое — реши задачу пошагово, покажи промежуточные вычисления и финальный ответ.
														   Если теоретическое и практическое вместе — сначала теория, потом решение.
														   Ничего не придумывай: если задачи нет — не выдумывай. Отвечай только на явно поставленные вопросы.
														   Формулы пиши в обычном текстовом виде (не LaTeX, без спецсимволов).
														   Не пропускай ни один пункт задания. В ответах не используй Маркдаун, но можешь использовать смайлики для понятного оформления""")
			await update.message.reply_text(f'Текст с фото{text_question}')
			await update.message.reply_text(text)
		
async def doc(update: Update, context: ContextTypes.DEFAULT_TYPE):

	print(update.message.caption)
	if update.message.caption:
		text = update.message.caption
	else:
		await update.message.reply_text("При загрузке пишите название предмета")
		return
	
	await update.message.reply_text("Добавляю файл в свою бибилотеку")

	document = update.message.document
	file_id = document.file_id
	file_name = document.file_name
	file = await context.bot.get_file(file_id)
	path = await file.download_to_drive()

	link = chat.upload_file(str(path), url_upload)

	upload_tokens(text, link)

	os.remove(path)

	await update.message.reply_text("Загрузил")
    
async def link_to_file(update: Update, context: ContextTypes.DEFAULT_TYPE):

	data = update.message.text.split(' ')
	link = chat.upload_by_link(data[0])

	if link is not None:
		upload_tokens(data[1:], link)
		await update.message.reply_text("Успешно загрузил")
	else:
		await update.message.reply_text("Что то пошло не так, сори бро")



def main():
	

	application = Application.builder().token(bot_token).build()
	application.add_handler(CommandHandler('start', start))
	application.add_handler(MessageHandler(filters.Regex(r'^http'), link_to_file))
	application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ans))
	application.add_handler(MessageHandler(filters.PHOTO, pic))
	application.add_handler(MessageHandler(filters.Document.ALL, doc))


	application.run_polling()
if __name__ == "__main__":
	main()