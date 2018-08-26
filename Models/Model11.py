from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Transaction(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer)
    stock_ticker = db.Column(db.String)
    quantity = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    price_at_transaction = db.Column(db.DECIMAL(9,2))

    def __repr__(self):
        return str((self.person_id, self.transaction_id, self.stock_ticker, self.quantity, self.date, self.date, self.price_at_transaction))

class BankWithdrawls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer)
    amount = db.Column(db.DECIMAL, unique=True, nullable=False)

    def __repr__(self):
        return str(self.username)

class BankDeposits(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer)
    amount = db.Column(db.DECIMAL)

    def __repr__(self):
        return str((self.person_id, self.amount))


# User Model
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    # User auth info
    username = db.Column(db.String(100, collation='NOCASE'), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False, server_default='')

    # User info
    firstname = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    lastname = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
