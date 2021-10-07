from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

TELEGRAM_TOKEN = '2033287598:AAFBPr75b4abzYk0rMSH2Q4ph9mvMmC1U38'

updater = Updater(token=TELEGRAM_TOKEN)


def say_hi(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='Извени Макс нас всех')


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    buttons = ReplyKeyboardMarkup([
            ['Который час?', 'Определи мой ip'],
            ['/random_digit']
        ])
    context.bot.send_message(
        chat_id=chat.id,
        text='Спасибо, что вы включили меня, {}!'.format(name),
        reply_markup=buttons
        )


def danil_pidr(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='Данил пидр')


updater.dispatcher.add_handler(MessageHandler(Filters.text('Пидор'), danil_pidr))

updater.dispatcher.add_handler(CommandHandler('start', wake_up))

updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))

updater.start_polling()
