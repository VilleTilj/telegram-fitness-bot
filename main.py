import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dependencies import TOKEN
import planking

'''
Enable simple loggings for debugging and error cases to two different files.
'''
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

plank = planking.Plank()




def handle_messages(update, context):
    '''
    Handle message request coming to the bot.
    - Currently supporting only planking excercise tracking and /help command.
    '''
    if update.message.text == '/help':
        help(update)
    else:
        plank.message_handler(update, context)


def help(update):
    '''
    Return information of the commands that bot has
    '''
    update.message.reply_text("Available commands are:\n/planking\n-Add planking result in seconds.\n/get_week_results\n-Returns figure visualizing last weeks planking records.\n/get_all_results\n-Return figure visualizing all entered records.\n/best_result\n-Returns your best recorded planking result.")



def main():
    try:
        updater = Updater(token=TOKEN, use_context=True)
        updater.dispatcher.add_handler(MessageHandler(Filters.all, handle_messages))
        updater.start_polling()
        updater.idle()
    except Exception as e:
        error_logger.error(e)

if __name__ == '__main__':
    main()

