import pytest
from telegram.ext import Updater, MessageHandler, Filters
from planking import Plank 
from mock import patch



class Test_planking_methods():

    def test_get_commands(self):
         obj = Plank()
         assert obj.get_commands() != ''