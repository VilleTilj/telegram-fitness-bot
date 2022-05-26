'''
Class for adding planking records to databases
'''

from db_helper import DB_helper
import datetime


class Plank():

    def __init__(self) -> None:
        self.commands = {
            '/lankutus' : self.add_result,
        }
        self.db = DB_helper()
        self.db.setup()
        self.waiting_result = False


    def get_commands(self):
        return self.commands


    def add_result(self, update, context):
        print(update.message.from_user)
        update.message.reply_text("Test plank class Commands")


    def message_handler(self, update, context):
        msg = update.message.text

        if ('/lankutus' in msg) and (len(msg.split()) == 1):
            self.waiting_result = True
            update.message.reply_text("Send the planking result as integer format or stop entering the result by answering with text 'stop'.")

        elif self.waiting_result:
            if msg.isdigit():
                self.waiting_result = False
                self.db.add_planking_results(update.message.chat_id, datetime.datetime.today().date(), msg)
                update.message.reply_text('Planking result saved!')
            
            elif msg == 'stop':
                self.waiting_result = False
                update.message.reply_text('Asking for result stopped.')
            
            else:
                update.message.reply_text("Send the planking result as integer format or stop entering the result by answering with text 'stop'.")

        elif ('/lankutus' in msg) and (len(msg.split()) == 2):
            self.db.add_planking_results(update.message.chat_id, datetime.datetime.today().date(), msg.split()[1])
            update.message.reply_text('Planking result saved!')
        
