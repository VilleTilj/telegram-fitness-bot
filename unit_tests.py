import pytest
from telegram.ext import Updater, MessageHandler, Filters
from planking import Plank 
from db_helper import DB_helper


def test_planking_get_commands():
    obj = Plank()
    assert obj.get_commands() != ''


def test_sqlite_add_result():
    db_tester = DB_helper()
    amount_before_add = len(db_tester.get_plank_results()['Test'])
    db_tester.add_planking_results('Test', 'Test', 'Test')
    amount_after_add = len(db_tester.get_plank_results()['Test'])
    assert (amount_after_add - amount_before_add) == 1

def test_sqlite_dell_result():
    db_tester = DB_helper()
    amount_before_del = len(db_tester.get_plank_results()['Test'])
    db_tester.delete_planking_result('Test')
    amount_after_del = len(db_tester.get_plank_results()['Test'])
    assert (amount_after_del - amount_before_del) == -1

