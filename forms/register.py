from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from db.db import DB

class RegisterForm(FlaskForm):
    id = StringField('ID', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate(self):

        print('validating... ')

        if not FlaskForm.validate(self):
            print('default validation failed... ')
            return False
        else:
            db = DB()

            if db.idexists(self.id.data):
                print('id exists')
                self.id.errors.append('The ID already exists')
                return False

            if db.usernameexists(self.username.data):
                print('username exists')
                self.username.errors.append('The username already exists')
                return False

            return True