'''
Class for adding planking records to databases
'''

from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('agg')
from db_helper import DB_helper
import datetime
from dependencies import test_users, IS_TEST


class Plank():
    '''
    Class that handless bots planking messages, saving data and plotting figures.
    '''
    def __init__(self) -> None:
        self.db = DB_helper()
        self.db.setup()
        self.waiting_result = False

    def add_result(self, update):
        print(update.message.from_user)
        update.message.reply_text("Test plank class Commands")

    def show_best_results(self, update, context, results):
        for key, value in results.items():
            if int(key) == update.message.chat_id:
                data = list(map(list, zip(*value)))
                output = max(data[1])
                update.message.reply_text(f'User @{update.message.chat.username} best planking results : {output} seconds.')
                break

    
    def plot_week_results(self, update, context, results):
        for key, value in results.items():
            if int(key) == update.message.chat_id:
                data = list(map(list, zip(*value)))
                dt = datetime.datetime.today()
                week_dates = ([ (dt - datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7) ])
                idx = []
                for i, date in enumerate(data[0]):
                    if date in week_dates:
                        idx.append(i)

                data[0], data[1] = [data[0][i] for i in idx], [data[1][i] for i in idx]
                plt.plot(data[0], data[1], marker='o', linestyle='--',)

        plt.savefig('results.png')
        context.bot.sendPhoto(chat_id=update.message.chat_id, photo=open('results.png','rb'), caption='Your last 7 days entered planking results!')

    

    def plot_all_results(self, update, context, results):
        '''Find users results and plot them in a figure that is returned'''
        for key, value in results.items():
            if int(key) == update.message.chat_id:
                data = list(map(list, zip(*value)))
                plt.plot(data[0], data[1], marker='o', linestyle='--',)
                plt.legend()

        plt.savefig('results.png')
        context.bot.sendPhoto(chat_id=update.message.chat_id, photo=open('results.png','rb'), caption='All entered planking results')


    def message_handler(self, update, context):
        msg = update.message.text

        if ('/planking' in msg) and (len(msg.split()) == 1):
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
            self.__method_handler(update, context, self.plot_all_results)

        elif('/get_week_results' in msg):
            self.__method_handler(update, context, self.plot_week_results)

        elif('/best_result' in msg):
            self.__method_handler(update, context, self.show_best_results)
            

    def __method_handler(self,update, context, function):
        results = self.db.get_plank_results()
        chat_id = update.message.chat_id
        filtered_results = {}
        if IS_TEST:
            for key, value in results.items():
                if str(key) in test_users:
                    filtered_results[key] = value
            
                function(update, context, filtered_results)
            
        elif chat_id in results:
            data = results[chat_id]
            function(update, context, data)

        else:
            update.message.reply_text('Your have not uploaded any results yet!')
