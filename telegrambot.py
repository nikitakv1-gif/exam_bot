import logging
import json
from chatpdf import ChatBot
import json 
from config import update_tokens
import os
from dotenv import load_dotenv

from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

chat = ChatBot('sourse_id', 'url', 'api_key')
url = 'https://api.chatpdf.com/v1/chats/message'

load_dotenv()

api_key = os.getenv('CHATPDF_API_KEY')  
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

def exam_keyboard():
	
	keyboard = [[ KeyboardButton(i) for i in update_tokens().keys()]]

	print(keyboard)

	reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard = True)

	return reply_markup

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
	user = update.effective_user

	await update.message.reply_text(
		f'Привет, выбери текущий экзамен',
		reply_markup = exam_keyboard())

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
	global chat
	bots = update_tokens()


	if update.message.text not in bots.keys():
		text = chat.send_message(update.message.text)
		await update.message.reply_text(text)
	else:
		await update.message.reply_text(
			"Экзамен выбран, задавайте вопросы",
			reply_markup = exam_keyboard())

		chat = ChatBot(bots[update.message.text], url, api_key)




def main():
	

	application = Application.builder().token(bot_token).build()
	application.add_handler(CommandHandler('start', start))
	application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


	application.run_polling(allowed_updates=Update.ALL_TYPES)
if __name__ == "__main__":
	main()