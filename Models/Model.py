from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Transaction(db.Model):
    """ Used to record stock Transaction history """
    transaction_id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer)
    stock_ticker = db.Column(db.String)
    quantity = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    avg_cost = db.Column(db.DECIMAL)

    def __repr__(self):
        return str((self.person_id, self.transaction_id, self.stock_ticker, self.quantity, self.date, self.date, self.avg_cost))


class StockHoldings(db.Model):
    """ Used to record current stock holdings for people """
    transaction_id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer)
    stock_ticker = db.Column(db.String)
    quantity = db.Column(db.Integer)
    avg_cost = db.Column(db.DECIMAL)

    def __repr__(self):
        return str((self.person_id, self.transaction_id, self.stock_ticker, self.quantity, self.date, self.avg_cost))


class BankWithdrawals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer)
    amount = db.Column(db.DECIMAL, nullable=False)

    def __repr__(self):
        return str((self.id, self.person_id, self.amount))


class BankDeposits(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer)
    amount = db.Column(db.DECIMAL)

    def __repr__(self):
        return str((self.person_id, self.amount))


# User Model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    # User auth info
    username = db.Column(db.String(100, collation='NOCASE'), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False, server_default='')

    # User info
    firstname = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    lastname = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')

    ssn = db.Column(db.String(9, collation='NOCASE'), nullable=False, server_default='')
    email = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    balance = db.Column(db.DECIMAL)

