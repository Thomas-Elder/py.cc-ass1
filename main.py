import datetime
from forms.updatepost import UpdatePostForm
from forms.updatepassword import UpdatePasswordForm
import os

from flask import Flask, request, url_for, redirect, render_template, flash
from flask_login import login_manager, login_user, logout_user, login_required, current_user, LoginManager
from werkzeug.utils import secure_filename

from db.db import DB

from forms.login import LoginForm
from forms.register import RegisterForm
from forms.post import PostForm
from forms.updatepassword import UpdatePasswordForm
from forms.updatepost import UpdatePostForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'very secure'

loginManager = LoginManager(app)
loginManager.login_view = 'login'

db = DB()

@loginManager.user_loader
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

            login_user(db.getuser(form.id.data))
            return redirect(url_for('forum'))

        else:
            return render_template('login.html', form=form)   

    else:
        return render_template('login.html', form=form)   

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

            db.setuser(form.id.data, form.username.data, form.password.data, request.files['avatar'])

            return redirect(url_for('login'))

        else:
            return render_template('register.html', form=form)

    else:
        return render_template('register.html', form=form)

#
#
#
@app.route('/userpage', methods=['GET'])
@login_required
def userpage():
    
    img = db.getimg(current_user.id)

    # Create update password form
    updatepasswordform = UpdatePasswordForm()
    passworderror = request.args.get('passworderror')

    if passworderror != None and passworderror != 'None':
        updatepasswordform.oldpassword.errors = [passworderror]

    # Now for update post forms, we need an instance for each post.
    # So init a list, get all the user posts
    updatepostforms = []
    userposts = db.getposts(current_user.id)

    # Create a new postform for each post, add post data to it, for prefilling
    for post in userposts:
        updatepostform = UpdatePostForm(id=post.id)
        updatepostform.subject.data = post.subject
        updatepostform.message.data = post.message
        updatepostforms.append(updatepostform)

    # This creates a nifty tuple of posts and forms which we can iterate neatly
    # over in the view.
    postandforms = list(zip(userposts, updatepostforms))

    return render_template(
        'userpage.html',
        img=img,
        current_user=current_user,
        updatepasswordform=updatepasswordform,
        postandforms=postandforms
        )

#
#
#
@app.route('/updatepassword', methods=['POST'])
@login_required
def updatepassword():

    updatepasswordform = UpdatePasswordForm(id=current_user.id)

    if updatepasswordform.validate_on_submit():

        # push password to db
        db.setpassword(current_user.id, updatepasswordform.newpassword.data)

        # and redir to login, need to log the user out so they can log in with new creds
        logout_user()
        return redirect(url_for('login'))

    else:
        # redirect to userpage, passing the password form.
        return redirect(url_for('userpage', passworderror=updatepasswordform.oldpassword.errors))


#
#
#
@app.route('/updatepost', methods=['POST'])
@login_required
def updatepost():

    updatepostform = UpdatePostForm()

    if updatepostform.validate_on_submit():
        # push updated post to db
        db.updatepost(updatepostform.postid.data, updatepostform.subject.data, updatepostform.message.data, current_user, request.files['image'])
        # and redir to forum
        return redirect(url_for('forum'))
    else:
        
        return redirect(url_for('userpage'))

#
#
#
@app.route('/forum', methods=['GET', 'POST'])
@login_required
def forum():

    form = PostForm()

    if request.method == 'POST':
        if form.validate_on_submit():

            db.addpost(form.subject.data, form.message.data, current_user, request.files['image'])

            return redirect(url_for('forum'))
    else:

        img = db.getimg(current_user.id)
        posts = db.getposts()
        userposts = db.getposts(current_user.id)

        return render_template(
            'forum.html', 
            form=form, 
            current_user=current_user,
            posts=posts,
            userposts=userposts,
            img=img
            )

#
# For local hosting
#
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8181, debug=True)