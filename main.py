import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dependencies import TOKEN
import planking


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.debug('Test')

error_logger = logging.getLogger("ErrorLogger")
file_settings = logging.FileHandler('logs/errors.log')
error_logger.addHandler(file_settings)
error_logger.warning('Test file logging')

def messages(update, context):
    plank = planking.Plank()
    plank.message_handler(update, context)


def help(update, context):
    print(update.message.from_user)
    update.message.reply_text("This is the help")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    updater.dispatcher.add_handler(MessageHandler(Filters.all, messages))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

