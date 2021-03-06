from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired
from db.db import DB

class RegisterForm(FlaskForm):
    id = StringField('ID', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    avatar = FileField('Avatar', validators=[FileRequired()])
    submit = SubmitField('Register')

    def validate(self):

        if not FlaskForm.validate(self):
            return False
        else:
            db = DB()

            if db.idexists(self.id.data):
                self.id.errors.append('The ID already exists')
                return False

            if db.usernameexists(self.username.data):
                self.username.errors.append('The username already exists')
                return False

            return True