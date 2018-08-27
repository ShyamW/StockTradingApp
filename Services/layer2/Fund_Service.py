import requests
from pandas.io.json import json_normalize, loads
import pandas as pd
""" Service involving the transfer of funds """


def remove_funds(amount, person):
    """ Removes funds from person's account
    Args:
        amount: amount of money to deposit
        person: person that wants to transfer money"""

    # TODO remove funds from person's account
    print("Withdraw" + str(amount))
    return True


def add_funds(amount, person):
    """ Adds funds into person's account
    Args:
        amount: amount of money to deposit
        person: person that wants to transfer money"""

    # TODO add amount to person's account
    print("DEPOSIT" + str(amount))
    return
