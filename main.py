import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dependencies import TOKEN
from telegram import Bot


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def messages(update, context):
    print(update.message.from_user)

def main():
    updater = Updater(token=TOKEN, use_context=True)
    updater.dispatcher.add_handler(MessageHandler(Filters.all, messages))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

