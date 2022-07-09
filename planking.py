'''
Class for adding planking records to databases
'''

from matplotlib import pyplot as plt
import matplotlib.dates as mdates
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

    def show_best_results(self, update, context, results):
        '''Return users best planking results as a text message'''
        for key, value in results.items():
            if int(key) == update.message.chat_id:
                data = list(map(list, zip(*value)))
                output = max(data[1])
                update.message.reply_text(f'User @{update.message.chat.username} best planking results : {output} seconds.')
                break

    
    def plot_week_results(self, update, context, results):
        '''Return photo visualizing planking results from last 7 days'''
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
                data = self.__get_highest_results(data)
                x = [datetime.datetime.strptime(d,'%Y-%m-%d').date() for d in data[0]]
                plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
                plt.gca().xaxis.set_major_locator(mdates.DayLocator())
                plt.plot(x, data[1], marker='o', linestyle='--',)
                plt.gcf().autofmt_xdate()
                plt.title('Last 7 days planking results, best of each day.')
                plt.xlabel('Date')
                plt.ylabel('Seconds')

        plt.savefig('results.png')
        context.bot.sendPhoto(chat_id=update.message.chat_id, photo=open('results.png','rb'), caption='Your last 7 days entered planking results!')

    

    def plot_all_results(self, update, context, results):
        '''Find users results and plot them in a figure that is returned'''
        for key, value in results.items():
            if int(key) == update.message.chat_id:
                data = list(map(list, zip(*value)))
                data = self.__get_highest_results(data)
                x = [datetime.datetime.strptime(d,'%Y-%m-%d').date() for d in data[0]]
                fig, ax = plt.subplots()
                plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
                plt.gca().xaxis.set_major_locator(mdates.DayLocator())
                plt.plot(x, data[1], marker='o', linestyle='--',)
                plt.gcf().autofmt_xdate()
                plt.title('All entered planking results, best of each day.')
                plt.xlabel('Date')
                plt.ylabel('Seconds')

                every_nth = 4
                for n, label in enumerate(ax.xaxis.get_ticklabels()):
                    if n % every_nth != 0:
                        label.set_visible(False)

        plt.savefig('results.png')
        context.bot.sendPhoto(chat_id=update.message.chat_id, photo=open('results.png','rb'), caption='All entered planking results')

    def __get_highest_results(self, data) -> list:
        temp: list[tuple] = [()]
        for i, day in enumerate(data[0]):
            if day not in temp[-1]: 
                temp.append( (day, data[1][i]))
 
            elif data[1][i] > temp[1][-1]:
                temp[-1] = (day, data[1][i])
        data = list(map(list, zip(*temp[1:])))
        return data

    def message_handler(self, update, context):
        '''Handle upcoming request messages and select know commands'''
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
