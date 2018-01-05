import sys
from sqlalchemy.sql.expression import func
from app import db

from app.models.articles import Article, ArticleText
from app.utils.stemmer import create_wordlist
from app.utils.glossary import write_json_glossary

PRONOUNS = ['ja','ti','on','ona','ono','mi','vi','oni','one','ona']
VERB_TENSES = ['present','past', 'future', 'conditional', 'imperative']

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
    __table_args__ = (db.UniqueConstraint('hr_word_id','en_word_id', 'role_id', name='hr_en_uniq'),)

    id = db.Column(db.Integer, primary_key=True)
    hr_word_id = db.Column(db.Integer, db.ForeignKey('hr_words.id', ondelete='CASCADE'), nullable=False)
    en_word_id = db.Column(db.Integer, db.ForeignKey('en_words.id', ondelete='CASCADE'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('word_roles.id'), nullable=True)
    gender = db.Column(db.Enum('male', 'female', 'neuter', name="word_gender"))
    plural = db.Column(db.Boolean())
    note = db.Column(db.String())
    guess = db.Column(db.Boolean(), nullable=True)

    def __repr__(self):
        return '{}: {}'.format(self.hr_words.term, self.en_words.term)

    def en_hr_to_json(self):
        return dict(
                def_id=self.id,
                value=self.en_words.term,
                label="{} : {}".format(self.en_words.term, self.hr_words.term)
                )

    def hr_en_to_json(self):
        return dict(
                def_id=self.id,
                value=self.hr_words.term,
                label="{} : {}".format(self.hr_words.term, self.en_words.term)
                )

class HrWord(db.Model):
    '''
    Croatian word: id, term
    '''
    __tablename__ = 'hr_words'

    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(), unique=True, nullable=False)
    definitions = db.relationship('Definition', backref='hr_words', lazy='dynamic')
    users = db.relationship("WordBank", backref='hr_word')

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


def create_glossary(a_id, article_text):
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
            if not word_defs:
                word_defs = Definition.query.join(Definition.hr_words, aliased=True).filter(HrWord.term.like("{}%".format(para[word]))).order_by(func.length(HrWord.term)).limit(3).all()

            ''' Final check, remove last letter and try again for stemmed root '''
            if not word_defs and len(para[word][:-1]) > 2:
                word_defs = Definition.query.join(Definition.hr_words, aliased=True).filter(HrWord.term.like("{}%".format(para[word][:-1]))).limit(3).all()

            if word_defs:
                for w in word_defs:
                    paralist.append(w)

        para_all = format_glossary(paralist)
        glossary.append({
            'paragraph' : paracount,
            'definitions' : [para_all]
            })
        paracount += 1
    print(glossary, file=sys.stdout)
    jg = write_json_glossary(a_id, glossary)
    if jg:
        at = ArticleText.query.filter(ArticleText.article_id==a_id).first()
        at.has_dict = True
        db.session.commit()
    return jg


def format_glossary(wbl):
    '''
    Take list of Definition query results
    return list with concatenated en_words for each unique hr_word
    ex: [{'def_id': 16300, 'hr_word': 'stanje', 'en_words': ['state', 'condition']}, ...]
    '''
    wb = []
    hrs = set([ w.hr_words.term for w in wbl ])
    for hr in hrs:
        def_group=[]
        ens = set([ wd.en_words.term for wd in wbl if wd.hr_words.term == hr ])
        word_id = [ wd.hr_words.id for wd in wbl if wd.hr_words.term == hr ]
        def_group = {
            'def_id' : word_id[0],
            'hr_word' : hr,
            'en_words' : [ w for w in ens ]
            }
        wb.append(def_group)
    return wb
