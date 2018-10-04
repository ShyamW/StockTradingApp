from app import db
from passlib.hash import pbkdf2_sha256
import os
import base64
import onetimepass

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'


class StockTransactions(db.Model):
    """ Used to record stock Transaction history """
    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer)
    stock_ticker = db.Column(db.String)
    quantity = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    avg_cost = db.Column(db.DECIMAL)

    def __repr__(self):
        return str((self.person_id, self.stock_ticker, self.quantity, self.date, self.date, self.avg_cost))


class StockHoldings(db.Model):
    """ Used to record current stock holdings for people """
    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer)
    stock_ticker = db.Column(db.String)
    quantity = db.Column(db.Integer)
    avg_cost = db.Column(db.DECIMAL)

    def __repr__(self):
        return str((self.person_id, self.stock_ticker, self.quantity, self.avg_cost))

    def __init__(self, person_id, stock_ticker, quantity, avg_cost):
        self.person_id = person_id
        self.stock_ticker = stock_ticker
        self.quantity = quantity
        self.avg_cost = avg_cost


class BankWithdrawals(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer)
    amount = db.Column(db.DECIMAL, nullable=False)

    def __repr__(self):
        return str((self.person_id, self.amount))


class BankDeposits(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer)
    amount = db.Column(db.DECIMAL)

    def __repr__(self):
        return str((self.person_id, self.amount))


# User Model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # User auth info
    email = db.Column(db.String(100, collation='NOCASE'), unique=True)
    password = db.Column(db.String(200), nullable=False, server_default='')
    otp_secret = db.Column(db.String(16))

    # User info
    firstname = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    lastname = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    phonenumber = db.Column(db.String(10, collation='NOCASE'), nullable=False, server_default='')
    ssn = db.Column(db.String(9, collation='NOCASE'), nullable=False, server_default='')
    balance = db.Column(db.DECIMAL)

    def __init__(self, email, firstname, lastname, password, phonenumber, ssn, balance):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password = pbkdf2_sha256.hash(password)
        self.phonenumber = phonenumber
        self.ssn = pbkdf2_sha256.hash(ssn)
        self.balance = balance
        if self.otp_secret is None:
            # generate a random secret
            self.otp_secret = base64.b32encode(os.urandom(10)).decode('utf-8')

    def validate_password(self, userentered):
        return pbkdf2_sha256.verify(userentered, self.password)

    def validate_ssn(self, userentered):
        return pbkdf2_sha256.verify(userentered, self.ssn)

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

    def get_totp_uri(self):
        return 'otpauth://totp/2FA-Demo:{0}?secret={1}&issuer=2FA-Demo' \
            .format(self.email, self.otp_secret)

    def verify_totp(self, token):
        return onetimepass.valid_totp(token, self.otp_secret)
