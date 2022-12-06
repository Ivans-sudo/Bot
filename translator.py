from telegram.ext import CallbackContext
from telegram.ext.updater import Updater
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from telegram.ext.filters import Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from translate import Translator


def select_lang(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("Арабский", callback_data='arabic'),
            InlineKeyboardButton("Немецкий", callback_data='german'),
            InlineKeyboardButton("Испанский", callback_data='spanish'),
        ],
        [
            InlineKeyboardButton("Французский", callback_data='french'),
            InlineKeyboardButton("Китайский", callback_data='chineese'),
            InlineKeyboardButton("Английский", callback_data='english')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Выберите язык для перевода:', reply_markup=reply_markup)


lang = ''
def button(update: Update, context: CallbackContext):
    global lang
    lang = update.callback_query.data.lower()
    query = update.callback_query
    query.answer()
    if query.data == 'english':
        string = 'Английский'
    if query.data == 'french':
        string = 'Французский'
    if query.data == 'german':
        string = 'Немецкий'
    if query.data == 'chineese':
        string = 'Китайский'
    if query.data == 'arabic':
        string = 'Арабский'
    if query.data == 'spanish':
        string = 'Испанский'
    query.edit_message_text(text=f'Для перевода выбран ' + string + ' язык!')


def lang_translator(user_input):
    translator = Translator(from_lang='russian',to_lang=lang)
    translation = translator.translate(user_input)
    return translation



def reply(update, context):
    user_input = update.message.text
    update.message.reply_text(lang_translator(user_input))


def run():
    API = '5897302324:AAFgNetJhW0aeE3h1wv3EM70ghYFgU7fMJQ'
    updater = Updater(API, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', select_lang))
    dp.add_handler(CommandHandler('select_lang', select_lang))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text, reply))
    updater.start_polling()
    updater.idle()

run()
