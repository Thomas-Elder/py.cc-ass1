from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired

class UpdatePostForm(FlaskForm):
    postid = HiddenField('')
    subject = StringField('Subject', validators=[DataRequired()])
    message = StringField('Message', validators=[DataRequired()])
    image = FileField('Image', validators=[FileRequired()])
    submit = SubmitField('Update')

    def validate(self):

        if not FlaskForm.validate(self):
            print('why are we here?')
            return False

        else:
            return True