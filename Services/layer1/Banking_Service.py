from Services.layer2 import Fund_Service
from Models import Model
from decimal import Decimal

def _is_deposit(action):
    """
    Returns:
        True if action is deposit
    """
    return str(action) == 'deposit'


def _withdraw_funds(amount, person):
    """ Withdraws funds from person's account
    Args:
        amount: amount of money to deposit
        person: person that wants to transfer money"""
    Fund_Service.remove_funds(amount, person)
    withdrawal = Model.BankWithdrawals(person_id=person.id, amount=amount)
    Model.db.session.add(withdrawal)
    Model.db.session.commit()


def _deposit_funds(amount, person):
    """ Deposits funds into person's account
    Args:
        amount: amount of money to deposit
        person: person that wants to transfer money"""
    Fund_Service.add_funds(amount, person)
    deposit = Model.BankDeposits(person_id=person.id, amount=amount)
    print(deposit)
    Model.db.session.add(deposit)
    Model.db.session.commit()


def bad_transfer(cash, amount, request_form):
    """
    Returns:
        True if user does not have at least the withdrawl amount """
    is_deposit = _is_deposit(str(request_form.form['Action']))
    if is_deposit:
        return False
    return cash < amount


def transfer_money(request_msg, person):
    """ Service to operate a money transfer
    Args:
        request_msg: request message through network
        person: person that wants to transfer money
    Returns:
        Success or Error Page """
    action = str(request_msg.form['Action'])
    bank_name = str(request_msg.form['Bank Name'])
    account_number = int(request_msg.form['Account Number'])
    routing_number = int(request_msg.form['Routing Number'])
    amount = Decimal(request_msg.form['Amount'])
    print(action, bank_name, account_number, routing_number, amount)
    if _is_deposit(action):
        _deposit_funds(amount, person)
    else:
        _withdraw_funds(amount, person)


