import requests
from pandas.io.json import json_normalize, loads
import pandas as pd
from decimal import *
""" Service involving the transfer of funds """


def remove_funds(amount, person):
    """ Removes funds from person's account
    Args:
        amount: amount of money to deposit
        person: person that wants to transfer money"""
    person.balance -= Decimal(amount)
    from Models.Model import db
    db.session.commit()
    print("Removed " + str(amount))


def add_funds(amount, person):
    """ Adds funds into person's account
    Args:
        amount: amount of money to deposit
        person: person that wants to transfer money"""
    person.balance += Decimal(amount)
    from Models.Model import db
    db.session.commit()
    print("Added " + str(amount))
