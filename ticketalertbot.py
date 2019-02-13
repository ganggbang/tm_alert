#!/usr/bin/python3
import pymysql
import logging
import re

from user import *
from connection import create_connection
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup
from telegram.ext import InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, RegexHandler,
						  ConversationHandler)


def main_menu_keyboard():
	keyboard = [[InlineKeyboardButton('Add Link', callback_data='add_link')],
							[InlineKeyboardButton('Settings', callback_data='settings')],
							[InlineKeyboardButton('View Links', callback_data='view_links')]]
	return InlineKeyboardMarkup(keyboard)


def main_menu_message():
	return 'Choose the option in menu:'


def main_menu(bot, update):
	query = update.callback_query
	bot.edit_message_text(chat_id=query.message.chat_id,
			message_id=query.message.message_id,
			text=main_menu_message(),
			reply_markup=main_menu_keyboard())



def start(bot, update):
	user_id = update['message']['chat']['id']

	if existing_user(user_id):
		update.message.reply_text(main_menu_message(), reply_markup=main_menu_keyboard())
	else:
		user = {
			"tm_id": str(user_id),
			"first_name": str(update['message']['chat']['first_name']),
			"last_name": str(update['message']['chat']['last_name']),
			"username": str(update['message']['chat']['username'])
		}

		save('users', user)
		update.message.reply_text(main_menu_message(), reply_markup=main_menu_keyboard())


def addlink_menu(bot, update):
	query = update.callback_query
	bot.edit_message_text(chat_id=query.message.chat_id,
			message_id=query.message.message_id,
			text="Please enter your link")
	return LINK


def addlink(bot, update):
	text = update.message.text

	user_id = update['message']['chat']['id']
	addlinkDB(text, user_id)

	update.message.reply_text('Your LINK has been successfully added',
		reply_markup=main_menu_keyboard())

	return ConversationHandler.END

def error(bot, update, error):
	"""Log Errors caused by Updates."""
	logger.warning('Update "%s" caused error "%s"', update, error)


def done(update):
	update.message.reply_text(""
							  "{}"
							  "Until next time!")

	return ConversationHandler.END


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

LINK, Binance_API, POS_SIZE, SPREAD, TAKE_PROFIT, STOP_LOSS, TRIGGER, PASTEIN = range(8)

logger = logging.getLogger(__name__)
updater = Updater('796932137:AAG7hqpAlrP4dFfOr8pwmbT0_owQ7ReWN6Y')
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='view_links'))


conv_handler = ConversationHandler(
	#per_message = True,
	entry_points=[CallbackQueryHandler(addlink_menu, pattern='^add_link'),],

	states={
		LINK: [MessageHandler(Filters.text,	addlink),],
	},

	fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)]
)


updater.dispatcher.add_handler(conv_handler)
updater.dispatcher.add_error_handler(error)

updater.start_polling()