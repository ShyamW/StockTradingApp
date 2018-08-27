from Services.layer2 import Fund_Service


def _is_deposit(action):
    """
    Returns:
        True if action is deposit
    """
    return action is 'deposit'


def _withdraw_funds(amount, person):
    """ Withdraws funds from person's account
    Args:
        amount: amount of money to deposit
        person: person that wants to transfer money"""

    # TODO remove funds from person's account if sufficient and record transfer
    Fund_Service.remove_funds(amount, person)
    return True


def _deposit_funds(amount, person):
    """ Deposits funds into person's account
    Args:
        amount: amount of money to deposit
        person: person that wants to transfer money"""

    # TODO add amount to person's account and record transfer
    print("DEPOSIT" + amount)
    Fund_Service.add_funds(amount, person)
    return


def transfer_money(request_msg, person):
    """ Service to operate a money transfer
    Args:
        request_msg: request message through network
        person: person that wants to transfer money
    Returns:
        Success or Error Page """
    action = str(request_msg.form['Action'])
    bank_name = int(request_msg.form['Bank Name'])
    account_number = int(request_msg.form['Account Number'])
    routing_number = int(request_msg.form['Routing Number'])
    amount = int(request_msg.form['Amount'])
    print(action, bank_name, account_number, routing_number, amount)
    if _is_deposit(action):
        _deposit_funds(amount, person)
    else:
        _withdraw_funds(amount, person)


