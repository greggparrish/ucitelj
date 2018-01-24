from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, RadioField, TextField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import ValidationError, DataRequired

from app.models.grammar import Verb, WordCase, Noun, Adjective, Adverb, GENDER_CHOICES


class WordCaseForm(FlaskForm):
    name = StringField('Case name', validators=[DataRequired()])
    table = StringField('Example table')
    submit = SubmitField('Add Case')

class VerbTypeForm(FlaskForm):
    head_verb = StringField('Head Verb', validators=[DataRequired()])
    code = StringField('Code', validators=[DataRequired()])
    submit = SubmitField('Add Verb Type')

class VerbForm(FlaskForm):
    hr_term = StringField('HR word', validators=[DataRequired()])
    en_term = StringField('EN definition', validators=[DataRequired()])
    type_id = SelectField('VerbType', coerce=int)
    submit = SubmitField('Add Verb')

class NounForm(FlaskForm):
    hr_term = StringField('HR word', validators=[DataRequired()])
    en_term = StringField('EN definition', validators=[DataRequired()])
    gender = RadioField(choices=GENDER_CHOICES)
    plural = BooleanField('Plural')
    animate = BooleanField('Animate')
    submit = SubmitField('Add Verb')

class AdjectiveForm(FlaskForm):
    hr_term = StringField('HR word', validators=[DataRequired()])
    en_term = StringField('EN definition', validators=[DataRequired()])
    submit = SubmitField('Add Adjective')

class AdverbForm(FlaskForm):
    hr_term = StringField('HR word', validators=[DataRequired()])
    en_term = StringField('EN definition', validators=[DataRequired()])
    submit = SubmitField('Add Adverb')
