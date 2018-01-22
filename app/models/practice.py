from app import db
from app.models.words import PRONOUNS, GENDERS, VERB_TENSES


# Cleaned word models b/c dictionary db is still a mess

GENDER_CHOICES = tuple(GENDERS)

class WordCase(db.Model):
    '''
    Cases: Nominative, accusative, etc.
    '''
    __tablename__ = 'word_cases'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    table = db.Column(db.Text(), nullable=True)
    def __repr__(self):
        return f'<Case: {self.name}>'

class VerbType(db.Model):
    '''
    Conjugation type for verb, how stem changes etc
    head_verb, code, verbs (assoc)
    '''
    __tablename__ = 'verb_types'
    id = db.Column(db.Integer, primary_key=True)
    head_verb = db.Column(db.String(24), unique=True, nullable=False)
    code = db.Column(db.String(8), unique=True, nullable=False)
    verbs = db.relationship('Verb', backref='verb_type', lazy='dynamic')

    def __repr__(self):
        return f'<Verb type: {self.code} {self.head_verb}>'


class Verb(db.Model):
    '''
    hr_term, en_term, type_id
    '''
    __tablename__ = 'verbs'
    id = db.Column(db.Integer, primary_key=True)
    hr_term = db.Column(db.String(), unique=True, nullable=False)
    en_term = db.Column(db.String(), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('verb_types.id'), nullable=False)

    def __repr__(self):
        return f'<Verb: {self.hr_term} > {self.en_term}>'

class Noun(db.Model):
    '''
    hr_term, en_term, gender, plural, animate
    '''
    __tablename__ = 'nouns'
    id = db.Column(db.Integer, primary_key=True)
    hr_term = db.Column(db.String(), unique=True, nullable=False)
    en_term = db.Column(db.String(), nullable=False)
    gender = db.Column(db.Enum(*GENDER_CHOICES, name="noun_gender"))
    plural = db.Column(db.Boolean())
    animate = db.Column(db.Boolean())

    def __repr__(self):
        return f'<Noun: {self.hr_term} > {self.en_term}>'

class Adjective(db.Model):
    '''
    hr_term, en_term
    '''
    __tablename__ = 'adjectives'
    id = db.Column(db.Integer, primary_key=True)
    hr_term = db.Column(db.String(), unique=True, nullable=False)
    en_term = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Adjective: {self.hr_term} > {self.en_term}>'

class Adverb(db.Model):
    '''
    hr_term, en_term
    '''
    __tablename__ = 'adverbs'
    id = db.Column(db.Integer, primary_key=True)
    hr_term = db.Column(db.String(), unique=True, nullable=False)
    en_term = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<adverb: {self.hr_term} > {self.en_term}>'
