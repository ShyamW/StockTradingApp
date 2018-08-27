from flask import Flask, render_template, redirect, request, flash, url_for
from flask_login import LoginManager, login_required, login_user, logout_user
from forms import RegisterForm, LoginForm
from flask_sqlalchemy import SQLAlchemy


# Services
from Services.layer1 import Order_Service, Banking_Service
from Services.layer2 import Stock_Service

""" Controller Class """
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Models/test.db'
db = SQLAlchemy(app)


# App config.
DEBUG = True
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
app.secret_key = 'secretkeyherepleaseeeeee'

# Flask-Login Setup
login_manager = LoginManager()
login_manager.init_app(app)

person = "bob"



@app.route('/')
def landing():
    """
    Root Page. Force Login, then after login: redirect to welcome page
    """
    return render_template('index.html')


@app.route('/welcome')  # TODO; get total portfolio value, cash value, stock value, stock breakdown
@login_required
def welcome():
    """
    Welcome Page to view portfolio and stocks
    """
    return render_template('welcome.html')

"""-------------------------------------------   ACCOUNT MANAGEMENT ----------------------------------------------------"""


@app.route('/register', methods=['GET', 'POST'])
def register():
    from Models.Model import User
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if User.query.filter_by(email=form.email.data).first():
                return "Email address already exists"
            else:
                # TODO ENCRYPT PASSWORD AND SSN
                user = User(form.email.data, form.firstname.data, form.lastname.data, form.password.data, form.ssn.data, 0)
                db.session.add(user)
                db.session.commit()

                login_user(user)

                return redirect(url_for('welcome'))
        else:
            return "Form didn't validate"
    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    from Models.Model import User
    form = LoginForm()

    if request.method == 'GET':
        return render_template('login.html', form=form)
    else:
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                # TODO DECRYPT PASSWORD AND CHECK
                if user.password == form.password.data:
                    login_user(user)
                    return redirect(url_for('welcome'))
                else:
                    # Wrong password
                    # TODO add message
                    return render_template('login.html')
            else:
                # No such user
                # TODO add message
                return render_template('register.html')
        else:
            return "Form didnt validate"


@login_manager.user_loader
def load_user(email):
    from Models.Model import User
    return User.query.filter_by(email=email).first()


@app.route('/logout')
@login_required
def logout():
    logout_user()
    # TODO add message for logged out
    return render_template("index.html")





@app.route('/bank/', methods=["GET", "POST"])
def bank():
    """
    Bank Page to do transfers
    """
    if request.method == 'POST':
        Banking_Service.transfer_money(request, person)
    cash_value = 0
    name = 'jon'
    return render_template('bank.html', cash_value=cash_value, name=name)


"""--------------------------------------   Buying and Selling Stock ------------------------------------------------"""


@app.route('/stocks/show/<ticker>/Buy/', methods=["GET", "POST"])
def buy_stock(ticker):
    """ Buys a stock if funds
    Params:
        ticker: ticker value for stock """
    # if buying a stock
    if request.method == 'POST':
        quantity = int(request.form['quantity'])
        url = Order_Service.buy(ticker, quantity, person)
        return redirect(url)
    else:  # if getting the buy page
        stock_price = Stock_Service.get_stock_price(ticker)
        return render_template('buy_stock.html', ticker=ticker, stock_price=stock_price)


@app.route('/stocks/show/<ticker>/Sell/', methods=["GET", "POST"])
def sell_stock(ticker):
    """ Sells a stock if funds
    Params:
        ticker: ticker value for stock """
    # if selling a stock
    if request.method == 'POST':
        quantity = int(request.form['quantity'])
        url = Order_Service.sell(ticker, quantity, person)
        return redirect(url)
    else:
        stock_price = Stock_Service.get_stock_price(ticker)
        return render_template('sell_stock.html', ticker=ticker, stock_price=stock_price)


"""-------------------------------------------   Viewing A stock ----------------------------------------------------"""


@app.route('/stocks/show/')
def redirect_show():
    """ Redirects to show_stock when user searches specific stock """
    ticker = request.args.get('ticker')
    return redirect('/stocks/show/' + ticker + '/')


@app.route('/stocks/show/<ticker>/')
def show_stock(ticker):
    """ Shows Stock data for <ticker>
    Params:
        ticker: ticker symbol for stock """
    stock_price = Stock_Service.get_stock_price(ticker)
    return render_template('show_stock.html', ticker=ticker, stock_price=stock_price)


if __name__ == '__main__':
    app.run()
