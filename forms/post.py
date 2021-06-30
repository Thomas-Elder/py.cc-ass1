from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    image = FileField('Image', validators=[FileRequired()])
    submit = SubmitField('Post')