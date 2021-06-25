from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    message = StringField('Massage', validators=[DataRequired()])
    image = PasswordField('Image')
    submit = SubmitField('Post')