'''
Class for adding planking records to databases
'''

class Plank():

    def __init__(self) -> None:
        self.commands = {
            '/lankutus' : self.add_result,
        }

    def get_commands(self):
        return self.commands

    def add_result(self, update, context):
        print(update.message.from_user)
        update.message.reply_text("Test plank class Commands")

    def message_handler(self, update, context):
        if update.message.text == '/lankutus':
            update.message.reply_text("Test plank class Messagehandler")

