import datetime


from flask import Flask, request, url_for, redirect, render_template, flash
from flask_login import login_user, logout_user, login_required, current_user, LoginManager

from google.cloud import datastore
from db.db import DB
from db.auth import Auth
from db.forum import Forum
from forms.login import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'very secure'

login = LoginManager(app)
login.login_view = 'login'

datastore_client = datastore.Client()

auth = Auth(datastore_client)
forum = Forum(datastore_client)
db = DB(datastore_client)

@login.user_loader
def load_user(id):
    return db.getuser(int(id))

#
# Routes
#
@app.route('/')
@app.route('/index')
def index():

    return render_template(
        'index.html', current_user=current_user)

#
#
#
@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():

        if db.checkpassword(int(form.id.data), form.password.data):

            login_user(db.getuser(int(form.id.data)))

            return redirect(url_for('index'))

        else:
            return redirect(url_for('loginerror'))

    return render_template('login.html', form=form)   

#
#
#
@app.route('/loginerror', methods=['GET'])
def loginerror():
    return render_template('loginerror.html')
#
#
#
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

#
#
#
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # set logged in true
        auth.login()
        # redirect to userpage
        return redirect(url_for('userpage'))
    else:
        return render_template(
            'register.html')

#
#
#
@app.route('/userpage')
@login_required
def userpage():
    # check if user logged in
    return render_template(
        'userpage.html', current_user=current_user)

#
#
#
@app.route('/forum')
@login_required
def forum():
    # check if user logged in
    return render_template(
        'forum.html', current_user=current_user)

#
# For local hosting
#
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)