import logging
import json
from chatpdf import ChatBot
import json 
from config import update_tokens
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

load_dotenv()

api_key = os.getenv('CHATPDF_API_KEY')  
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

chat = ChatBot('sourse_id', 'url', 'api_key')


def exam_keyboard():
	
	keyboard = [[ KeyboardButton(i) for i in update_tokens().keys()]]

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
		text = chat.send_message(update.message.text + "Реши все теоретические и практические задачи, подробно распиши теорию и практику, если ты не видишь задачи, то ее не надо придумывать, решай только теоретические вопросы и наоборот формулы для задачи отдавай в человекочитаемом виде, не в Latex. Обязательно ответь на все пункты")
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
			text = chat.send_message(text_question + "Реши все теоретические и практические задачи, подробно распиши теорию и практику, если ты не видишь задачи, то ее не надо придумывать, решай только теоретические вопросы и наоборот формулы для задачи отдавай в человекочитаемом виде, не в Latex. Обязательно ответь на все пункты")
			await update.message.reply_text(f'Текст с фото{text_question}')
			await update.message.reply_text(text)
		





def main():
	

	application = Application.builder().token(bot_token).build()
	application.add_handler(CommandHandler('start', start))
	application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ans))
	application.add_handler(MessageHandler(filters.PHOTO, pic))


	application.run_polling()
if __name__ == "__main__":
	main()