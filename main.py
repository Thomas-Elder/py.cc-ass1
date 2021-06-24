import datetime

from flask import Flask, request, url_for, redirect, render_template
from google.cloud import datastore

app = Flask(__name__)

datastore_client = datastore.Client()

def store_time(dt):
    entity = datastore.Entity(key=datastore_client.key('visit'))
    entity.update({
        'timestamp': dt
    })

    datastore_client.put(entity)


def fetch_times(limit):
    query = datastore_client.query(kind='visit')
    query.order = ['-timestamp']

    times = query.fetch(limit=limit)

    return times

#
# Routes
#
@app.route('/')
def index():

    return render_template(
        'index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        # check user input against db
        # set logged in true
        # redirect to userpage
        return redirect(url_for('userpage'))
    else:
        # display log in page
        return render_template(
            'login.html')      

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # set logged in true
        # redirect to userpage
        return redirect(url_for('userpage'))
    else:
        return render_template(
            'register.html')

@app.route('/userpage')
def userpage():
    # check if user logged in
    return render_template(
        'userpage.html')

@app.route('/forum')
def forum():
    # check if user logged in
    return render_template(
        'forum.html')

#
# For local hosting
#
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)