import datetime


from flask import Flask, request, url_for, redirect, render_template, flash
from flask_login import login_user, logout_user, login_required, current_user, LoginManager

from db.db import DB

from forms.login import LoginForm
from forms.register import RegisterForm
from forms.post import PostForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'very secure'

login = LoginManager(app)
login.login_view = 'login'

db = DB()

@login.user_loader
def load_user(id):
    return db.getuser(id)

#
# Routes
#
@app.route('/')
@app.route('/index')
def index():

    return render_template('index.html', current_user=current_user)

#
#
#
@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if request.method == 'POST':

        if form.validate_on_submit():

            if db.checkpassword(form.id.data, form.password.data):
                login_user(db.getuser(form.id.data))
                return redirect(url_for('forum'))

            else:
                return redirect(url_for('loginerror'))

    else:

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
    return redirect(url_for('login'))

#
#
#
@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()

    if request.method == 'POST':

        if form.validate_on_submit():

            db.setuser(form.id.data, form.username.data, form.password.data)
            return redirect(url_for('login'))
        else:
            return render_template('register.html', form=form)

    else:
        return render_template('register.html', form=form)

#
#
#
@app.route('/userpage')
@login_required
def userpage():
    # check if user logged in
    return render_template('userpage.html', current_user=current_user)

#
#
#
@app.route('/forum', methods=['GET', 'POST'])
@login_required
def forum():
    form = PostForm()
    posts = db.getposts()
    if request.method == 'POST':
        if form.validate_on_submit():
            db.addpost(form.subject.data, form.message.data, current_user)
            return redirect(url_for('forum'))
    else:

        img = db.getimg(current_user.id)

        return render_template(
            'forum.html', 
            form=form, 
            current_user=current_user,
            posts=posts,
            img=img)

#
# For local hosting
#
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)