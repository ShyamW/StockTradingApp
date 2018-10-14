from flask import Flask, render_template, redirect, request, flash, url_for, session, abort, Markup
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_session import Session
from flask_session_captcha import FlaskSessionCaptcha
from forms import RegisterForm, LoginForm, PasswordChangeForm
from flask_sqlalchemy import SQLAlchemy
from decimal import Decimal
from io import BytesIO
from Services.layer1 import Mail_Service
import pyqrcode
import datetime

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

# Captcha Setup
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['CAPTCHA_ENABLE'] = True
app.config['CAPTCHA_LENGTH'] = 6
Session(app)
captcha = FlaskSessionCaptcha(app)


@app.route('/')
def landing():
    """
    Root Page. Force Login, then after login: redirect to welcome page
    """
    print("########################")
    print(str(current_user.is_authenticated))
    print("#########################")
    return render_template('index.html')


@app.route('/welcome')
@login_required
def welcome(failure=None, msg=None):
    """
    Welcome Page to view portfolio and stocks
    """
    from Services.layer1 import Portfolio_Service
    user = current_user
    name = current_user.email
    current_holdings, cash_value, portfolio_value, total_value = Portfolio_Service.get_portfolio(user)
    print(cash_value, current_holdings, portfolio_value, total_value)
    return render_template('welcome.html', name=name, current_holdings=current_holdings, cash_value=cash_value,
                           portfolio_value=portfolio_value, total_value=total_value, failure=failure,
                           msg=msg)


"""--------------------------------------   Banking Operations ------------------------------------------------"""

# Services
from Services.layer1 import Order_Service, Banking_Service
from Services.layer2 import Stock_Service


@app.route('/bank/', methods=["GET", "POST"])
@login_required
def bank():
    """
    Bank Page to do transfers
    """
    cash_value = current_user.balance
    name = current_user.email

    # if transfer is initiated: check it's allowed before execution
    if request.method == 'POST':
        amount = Decimal(request.form['Amount'])

        if Banking_Service.bad_transfer(cash_value, amount, request):
            return render_template('bank.html', request=int(amount), cash_value=cash_value, name=name, failure=True)
        Banking_Service.transfer_money(request, current_user)

    return render_template('bank.html', cash_value=current_user.balance, name=name)


"""--------------------------------------   Buying and Selling Stock ------------------------------------------------"""


@app.route('/stocks/show/<ticker>/Buy/', methods=["GET", "POST"])
@login_required
def buy_stock(ticker):
    """ Buys a stock if funds
    Params:
        ticker: ticker value for stock """
    name = current_user.email
    # if buying a stock
    if request.method == 'POST':
        return Order_Service.buy(ticker, request, current_user)
    else:  # if getting the buy page
        stock_price = Stock_Service.get_stock_price(ticker)
        return render_template('buy_stock.html', name=name, ticker=ticker, stock_price=stock_price)


@app.route('/stocks/show/<ticker>/Sell/', methods=["GET", "POST"])
@login_required
def sell_stock(ticker):
    """ Sells a stock if funds
    Params:
        ticker: ticker value for stock """
    name = current_user.email
    # if selling a stock
    if request.method == 'POST':
        quantity = request.form['quantity']
        return Order_Service.sell(ticker, quantity, current_user)
    else:
        stock_price = Stock_Service.get_stock_price(ticker)
        return render_template('sell_stock.html', name=name, ticker=ticker, stock_price=stock_price)


"""-------------------------------------------   Viewing A stock ----------------------------------------------------"""


@app.route('/stocks/show/')
@login_required
def redirect_show():
    """ Redirects to show_stock when user searches specific stock """
    ticker = request.args.get('ticker')
    return redirect('/stocks/show/' + ticker + '/')


@app.route('/stocks/bad/show/')
@login_required
def invalid_show():
    """ Redirects to welcome page and prints error to screen when viewing invalid stock """
    return welcome(True, "That stock Does not Exist!")


@app.route('/stocks/show/<ticker>/')
@login_required
def show_stock(ticker):
    """ Shows Stock data for <ticker>
    Params:
        ticker: ticker symbol for stock """
    name = current_user.email
    try:
        stock_price = Stock_Service.get_stock_price(ticker)
        return render_template('show_stock.html', name=name, ticker=ticker, stock_price=stock_price)
    except ValueError:
        print("INVALID!")
        return invalid_show()


"""----------------------------------     QR Code Setup / Two Factor Setup   ----------------------------------------"""


@app.route('/twofactor')
@login_required
def two_factor_setup():
    # since this page contains the sensitive qrcode, make sure the browser
    # does not cache it
    return render_template('two_factor_setup.html'), 200, {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}


@app.route('/qrcode')
def qrcode():
    # render qrcode for FreeTOTP
    from Models.Model import User
    user = User.query.filter_by(email=session['email']).first()
    if user is None:
        abort(404)

    # for added security, remove username from session
    del session['email']
    url = pyqrcode.create(user.get_totp_uri())
    stream = BytesIO()
    url.svg(stream, scale=3)
    return stream.getvalue(), 200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}


"""-------------------------------------------   ACCOUNT MANAGEMENT -------------------------------------------------"""


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Register User route
    Returns:
        if validated -> welcome page
        else -> stays on register page
    """
    from Models.Model import User
    form = RegisterForm()
    if request.method == 'POST':
        # Check if form is validated and captcha is correct
        if form.validate_on_submit() and captcha.validate():
            # Check if user is already registered and flash warning
            if User.query.filter_by(email=form.email.data).first():
                login_link = "<a href=\"/login\" class=\"alert-link\">Sign in Here</a>"
                flash(Markup("Email address already exists. " + login_link))
                return render_template('register.html', form=form)
            else:
                # Add user to database
                user = User(form.email.data, form.firstname.data, form.lastname.data, form.password.data, form.phonenumber.data, form.ssn.data, 0)
                db.session.add(user)
                db.session.commit()
                # User is registered now login
                login_user(user)
                Mail_Service.send_email(form.email.data, "Account Creation", user, request.remote_addr)
                session['email'] = user.email
                return redirect(url_for('two_factor_setup'))
        else:
            # Failed register so redirect page
            flash("Sorry there was an issue with the form. Try again")
            return render_template('register.html', form=form)
    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login route
    Returns:
        if correct login -> redirects to welcome Page
        else -> stays on login page and displays warning
    """
    from Models.Model import User
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    else:
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                # Check password and token
                correctPassword = user.validate_password(form.password.data)
                correctToken = user.verify_totp(form.token.data)
                if correctPassword and correctToken:
                    login_user(user)
                    Mail_Service.send_email(form.email.data, "Login", user, request.remote_addr)
                    flash("Logged In")
                    return redirect(url_for('welcome'))
                else:
                    # Wrong password or token entered
                    if not correctToken:
                        flash("Incorrect Token. Please try again")
                    if not correctPassword:
                        flash("Incorrect password. Please try again")
                    Mail_Service.send_email(form.email.data, "Login Attempt", user, request.remote_addr)
                    return render_template('login.html', form=form)
            else:
                # No such user
                flash("No Such User Please Register")
                return redirect(url_for('register'))
        else:
            # Failed login so redirect page
            flash("Failed to Login")
            return render_template('login.html', form=form)


@login_manager.user_loader
def load_user(email):
    from Models.Model import User
    return User.query.filter_by(email=email).first()


@app.route('/logout')
@login_required
def logout():
    """
    Logout route
    Logs user out of system
    Return:
        redirects to welcome page
    """
    logout_user()
    flash("Logged Out Successfully")
    return redirect('/welcome')


@app.route('/changepassword', methods=['GET', 'POST'])
@login_required
def changepassword():
    form = PasswordChangeForm()
    if request.method == 'GET':
        return render_template('changepassword.html', form=form, name=current_user.email)
    else:
        if form.validate_on_submit():
            if current_user.validate_password(form.currentpassword.data):
                local_object = db.session.merge(current_user)
                local_object.password = current_user.update_password(form.newpassword.data)
                db.session.add(local_object)
                db.session.commit()
                Mail_Service.send_email(current_user.email, "Password Changed", current_user, request.remote_addr)
                flash("Password Sucessfully Changed")
            else:
                flash("Incorrect Current Password")
                return render_template('changepassword.html', form=form, name=current_user.email)
        else:
            flash("Error with form")
            return render_template('changepassword.html', form=form, name=current_user.email)
    return redirect(url_for('account'))


@app.route('/account')
@login_required
def account():
    return render_template('account.html', name=current_user.email)


@app.route("/deleteaccount")
@login_required
def deleteaccount():
    local_object = db.session.merge(current_user)
    Mail_Service.send_email(current_user.email, "Account Deleted", current_user, request.remote_addr)
    db.session.delete(local_object)
    db.session.commit()
    flash("Account Deleted Successfully")
    return redirect(url_for('landing'))


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('landing'))


@app.before_request
def before_request():
    Session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=5)
    Session.modified = True


if __name__ == '__main__':
    app.run()
