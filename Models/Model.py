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
    # User auth info
    email = db.Column(db.String(100, collation='NOCASE'), primary_key=True, unique=True)
    password = db.Column(db.String(200), nullable=False, server_default='')

    # User info
    firstname = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    lastname = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')

    SSN = db.Column(db.String(9, collation='NOCASE'), nullable=False, server_default='')
    balance = db.Column(db.DECIMAL)

    def __init__(self, email, firstname, lastname, password, ssn, balance):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.ssn = ssn
        self.balance = balance

    def __repr__(self):
        return '<User %r>' % self.email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.email)

