from app import db

from app.models.articles import Article
from app.views.stemmer import create_wordlist


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
    hr_word_id = db.Column('hr_id', db.Integer, db.ForeignKey('hr_words.id'))
    en_word_id = db.Column('en_id', db.Integer, db.ForeignKey('en_words.id'))
    gender = db.Column(db.Enum('male', 'female', 'neuter', name="word_gender"))
    plural = db.Column(db.Boolean())
    note = db.Column(db.String())
    role_id = db.Column(db.Integer, db.ForeignKey('word_roles.id'))

    def __repr__(self):
        return '{} :: {}'.format(self.hr_words.term, self.en_words.term)

    def create_glossary(self, article_text):
        '''
        Given an article, create a set of words, get definitions, and output as json
        '''
        wordlist = create_wordlist(article_text)
        glossary = []
        for word in wordlist:

            ''' First check if word exists as is '''
            word_defs = Definition.query.join(Definition.hr_words, aliased=True).filter_by(term=word).limit(3)

            ''' If not, check if any words start with stemmed root '''
            if word_defs == None:
                word_defs = Definition.query.join(Definition.hr_words, aliased=True).filter_by(term=wordlist[word]).all()

            ''' Final check, remove last letter and try again for stemmed root '''
            if word_defs == None and len(wordlist[word][:-1]) > 2:
                word_defs = Definition.query.join(Definition.hr_words, aliased=True).filter(Rijec.term.startswith(wodlist[word][:-1])).limit(3)

            if word_defs:
                glossary.append(word_defs)
        return glossary



class Rijec(db.Model):
    '''
    Croatian word: id, term
    '''
    __tablename__ = 'hr_words'

    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(), unique=True)
    definitions = db.relationship('Definition', backref='hr_words', lazy='dynamic')

    def __repr__(self):
        return '<HR Term {}>'.format(self.term)


class Word(db.Model):
    '''
    English word: id, term
    '''
    __tablename__ = 'en_words'

    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(), unique=True)
    definitions = db.relationship('Definition', backref='en_words', lazy='dynamic')

    def __repr__(self):
        return '<EN Term {}>'.format(self.term)
