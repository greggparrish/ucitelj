from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, URL

from app import images
from app.models.feeds import Feed


class FeedForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    rss = StringField('RSS feed', validators=[URL()])
    body_tag = StringField('Body Tag', validators=[DataRequired()])
    logo = FileField('Logo', validators=[FileRequired(), FileAllowed(images, 'only images')])
    feed_type = StringField('Feed Type', validators=[DataRequired()])
    country = RadioField(choices=Feed().country_choices())
    feed_type = RadioField(choices=Feed().type_choices())
    about = TextAreaField('About')
    submit = SubmitField('Submit')

