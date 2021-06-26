from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from db.db import DB

class LoginForm(FlaskForm):
    id = StringField('ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate(self):

        if not FlaskForm.validate(self):
            return False
        else:
            db = DB()

            if db.checkpassword(self.id.data, self.password.data):
                self.password.errors.append('ID or password is invalid')
                return True

            return False