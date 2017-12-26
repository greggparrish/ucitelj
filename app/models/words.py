from app import db


class WordRole(db.Model):
    '''
    Adjective, verb, noun, etc.
    '''
    __tablename__ = 'word_roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class Definition(db.Model):
    '''
    M2M rel b/w en & hr words, plus role, plural, notes, gender
    '''
    __tablename__ = 'definitions'
    id = db.Column(db.Integer, primary_key=True)
    hr_word_id = db.Column( 'Rijec', db.Integer, db.ForeignKey('hr_words.id'))
    en_word_id = db.Column( 'Word', db.Integer, db.ForeignKey('en_words.id'))
    note = db.Column(db.String())
    role_id = db.Column(db.Integer, db.ForeignKey('word_roles.id'))

    def __repr__(self):
        return '<Definition: {} -- {}>'.format(self.hr_word.term, self.en_word.term)


class Rijec(db.Model):
    '''
    Croatian word: id, term
    '''
    __tablename__ = 'hr_words'

    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String())
    gender = db.Column(db.Enum('male', 'female', 'neuter', name="word_gender"))
    plural = db.Column(db.Boolean())
    definitions = db.relationship('Definition', backref='hr_words', lazy='dynamic')

    def __repr__(self):
        return '<HR Term {}>'.format(self.term)


class Word(db.Model):
    '''
    English word: id, term
    '''
    __tablename__ = 'en_words'

    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String())
    definitions = db.relationship('Definition', backref='en_words', lazy='dynamic')

    def __repr__(self):
        return '<EN Term {}>'.format(self.term)
