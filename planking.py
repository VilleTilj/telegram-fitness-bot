'''
Class for adding planking records to databases
'''

from unittest import result

from matplotlib import pyplot as plt
from db_helper import DB_helper
import datetime
from dependencies import test_users, IS_TEST


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

    def show_todays_results(self, update, context, results):
        for key, value in results.items():
            item = str(datetime.datetime.today().date())
            output = list(filter(lambda x:item in x, value))
            update.message.reply_text(f'{test_users[key]} : {output}')

    
    def plot_all_results(self, update, context, results):
        for key, value in results.items():
            if key in test_users.keys():
                data = list(map(list, zip(*value)))
                plt.plot(data[0], data[1])
            print(data)

        plt.savefig('results.png')
        context.bot.sendPhoto(chat_id=update.message.chat_id, photo=open('results.png','rb'), caption='All entered planking results')


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
        
        elif('/get_all_results' in msg):
            chat_id = update.message.chat_id
            results = self.db.get_plank_results()
            filtered_results = {}
            if IS_TEST:
                for key, value in results.items():
                    if str(key) in test_users:
                        filtered_results[key] = value
                
                self.plot_all_results(update, context, filtered_results)
            
            elif chat_id in results:
                data = results[chat_id]
                self.plot_all_results(update, context, data)

            else:
                update.message.reply_text('Your have not uploaded any results yet!')
