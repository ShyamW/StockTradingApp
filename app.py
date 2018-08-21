from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

def make_new_user(username, password):
    print(username, password)
    return redirect(url_for('welcome'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return make_new_user(username, password)
    return render_template('register.html')

@app.route('/login')
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)




@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

if __name__ == '__main__':
    app.run()
