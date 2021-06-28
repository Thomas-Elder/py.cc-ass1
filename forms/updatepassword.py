from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from db.db import DB

class UpdatePasswordForm(FlaskForm):

    id = StringField('ID', validators=[DataRequired()])
    oldpassword = PasswordField('Old Password', validators=[DataRequired()])
    newpassword = PasswordField('New Password', validators=[DataRequired()])
    submit = SubmitField('Change')

    def validate(self):

        if not FlaskForm.validate(self):
            return False
        else:
            db = DB()

            if db.checkpassword(self.id.data, self.oldpassword.data):
                return True

            self.oldpassword.errors.append('The old password is incorrect')
            return False