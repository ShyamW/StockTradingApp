from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class BankWithdrawls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer)
    amount = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Transaction(db.Model):
    person_id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer)
    stock_ticker = db.Column(db.String)
    quantity = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    price_at_transaction = db.Column(db.Decimal)

    def __repr__(self):
        return self.person_id, self.transaction_id, self.stock_ticker, self.quantity, self.date, self.date, self.price_at_transaction