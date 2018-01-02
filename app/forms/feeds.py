from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, TextField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, URL

from app import images
from app.models.feeds import Feed


class NewFeedForm(FlaskForm):
    name = StringField('', validators=[DataRequired()])
    rss = StringField('', validators=[URL()])
    body_tag = StringField('', validators=[DataRequired()])
    logo = FileField('logo', validators=[FileRequired(), FileAllowed(images, 'only images')])
    feed_type = StringField('', validators=[DataRequired()])
    country = RadioField(choices=Feed().country_choices())
    feed_type = RadioField(choices=Feed().type_choices())
    about = TextField('About')
    submit = SubmitField('Add Feed')

