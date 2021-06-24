import datetime


from flask import Flask, request, url_for, redirect, render_template
from google.cloud import datastore
from auth.auth import Auth
from forum.forum import Forum

app = Flask(__name__)

datastore_client = datastore.Client()

auth = Auth(datastore_client)
forum = Forum(datastore_client)

#
# Routes
#
@app.route('/')
@app.route('/index')
def index():

    return render_template(
        'index.html', loggedin=auth.loggedin, user=auth.user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        # check user input against db
        # set logged in true
        auth.login()
        # redirect to userpage
        return redirect(url_for('userpage'))
    else:
        # display log in page
        return render_template(
            'login.html', loggedin=auth.loggedin, user=auth.user)      

@app.route('/logout')
def logout():
    auth.logout()

    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # set logged in true
        auth.login()
        # redirect to userpage
        return redirect(url_for('userpage'))
    else:
        return render_template(
            'register.html', loggedin=auth.loggedin, user=auth.user)

@app.route('/userpage')
def userpage():
    # check if user logged in
    return render_template(
        'userpage.html', loggedin=auth.loggedin, user=auth.user)

@app.route('/forum')
def forum():
    # check if user logged in
    return render_template(
        'forum.html', loggedin=auth.loggedin, user=auth.user)

#
# For local hosting
#
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)