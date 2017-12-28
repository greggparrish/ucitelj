import sys
from app import db

from app.models.articles import Article, ArticleText
from app.utils.stemmer import create_wordlist
from app.utils.glossary import write_json_glossary


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
    hr_word_id = db.Column(db.Integer, db.ForeignKey('hr_words.id', ondelete='CASCADE'), nullable=False)
    en_word_id = db.Column(db.Integer, db.ForeignKey('en_words.id', ondelete='CASCADE'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('word_roles.id'), nullable=True)
    gender = db.Column(db.Enum('male', 'female', 'neuter', name="word_gender"))
    plural = db.Column(db.Boolean())
    note = db.Column(db.String())

    def __repr__(self):
        return '{} :: {}'.format(self.hr_words.term, self.en_words.term)

    def create_glossary(self, article_id, article_text):
        '''
        Given an article, create a wordlist using utils.stemmer, get definitions, save as json file in public/
        Return: glossary as json
        '''
        wordlist = create_wordlist(article_text)
        glossary = []
        paracount = 1
        for para in wordlist:
            paralist = []
            for word in para:

                ''' First check if word exists as is '''
                word_defs = Definition.query.join(Definition.hr_words, aliased=True).filter_by(term=word).limit(3).all()

                ''' If not, check if any words start with stemmed root '''
                if word_defs == None:
                    word_defs = Definition.query.join(Definition.hr_words, aliased=True).filter_by(term=wordlist[word]).limit(3).all()

                ''' Final check, remove last letter and try again for stemmed root '''
                if word_defs == None and len(wordlist[word][:-1]) > 2:
                    word_defs = Definition.query.join(Definition.hr_words, aliased=True).filter(Rijec.term.startswith(wordlist[word][:-1])).limit(3).all()

                if word_defs:
                    def_group = {
                        'def_id' : word_defs[0].id,
                        'hr_word' : word_defs[0].hr_words.term,
                        'en_words' : [ w.en_words.term for w in word_defs ]
                        }
                    paralist.append(def_group)
            if paralist:
                glossary.append({
                    'paragraph' : paracount,
                    'definitions' : [paralist]
                    })
            paracount += 1
        jg = write_json_glossary(article_id, glossary)
        if jg:
            article_text = ArticleText.query.filter(article_id==article_id).first()
            article_text.has_dict = True
            db.session.commit()
        return jg


class HrWord(db.Model):
    '''
    Croatian word: id, term
    '''
    __tablename__ = 'hr_words'

    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(), unique=True, nullable=False)
    definitions = db.relationship('Definition', backref='hr_words', lazy='dynamic')

    def __repr__(self):
        return '<HR Word {}>'.format(self.term)


class EnWord(db.Model):
    '''
    English word: id, term
    '''
    __tablename__ = 'en_words'

    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(), unique=True, nullable=False)
    definitions = db.relationship('Definition', backref='en_words', lazy='dynamic')

    def __repr__(self):
        return '<EN Word {}>'.format(self.term)
