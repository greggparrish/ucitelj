import random
from sqlalchemy.sql.expression import func
from flask import Blueprint, render_template, request, jsonify
from flask_user import login_required, current_user

from app import app, db
from app.models.words import Definition, WordRole, HrWord, EnWord, format_glossary, PRONOUNS, VERB_TENSES
from app.models.users import WordBank

word_bp = Blueprint('words', __name__)

''' INDEX & SHOW '''
@word_bp.route('/')
def index(page=1):
    all_words = Word.query.order_by(Words.term)
    return render_template('words/index.html', all_words=all_words)

@word_bp.route('/<word_id>')
def show(word_id):
    w = Word.query.get(word_id)
    return render_template('words/show.html', w=w)


''' DICTIONARY '''
@word_bp.route('/dictionary')
def dictionary():
    return render_template('words/dictionary.html')

@word_bp.route('/define', methods=['GET'])
def define():
    dd = request.args.get('dict_dir')
    if dd == 'hr_en':
        hr_word = request.args.get('q_word').lower()
        word_defs = Definition.query.join(Definition.hr_words, aliased=True).filter(HrWord.term.like("{}%".format(hr_word))).order_by(func.length(HrWord.term)).limit(8).all()
        deflist = [ d.hr_en_to_json() for d in word_defs ]
    elif dd == 'en_hr':
        en_word = request.args.get('q_word').lower()
        word_defs = Definition.query.join(Definition.en_words, aliased=True).filter(EnWord.term.like("{}%".format(en_word))).order_by(func.length(EnWord.term)).limit(8).all()
        deflist = [ d.en_hr_to_json() for d in word_defs ]
    else:
        deflist=False
    return jsonify(deflist=deflist)


''' PRACTICE PAGES '''
@word_bp.route('/verbs/practice', methods=['GET'])
def verb_practice():
    load_list = request.args.get('load_list', type=bool)
    if load_list == True:
        verb_query = Definition.query.order_by(func.random()).join(Definition.hr_words, aliased=True).filter(Definition.role_id==31).limit(20).all()
        verblist = format_glossary(verb_query)
        for v in verblist:
            v['pronoun'] = random.choice(PRONOUNS)
            v['verb_tense'] = random.choice(VERB_TENSES)
        return jsonify(verblist)
    else:
        context = {
                'pronouns': PRONOUNS,
                'tenses': VERB_TENSES
                }
        return render_template('words/verb_practice.html', context=context)

@word_bp.route('/verbs/check', methods=['GET'])
def verb_check():
    if set(['answer','verb','pronoun','verb_tense','hr_id']).issubset(set([k for k in request.args.keys()])):
        answer = request.args.get('answer', type=str)
        verb = request.args.get('verb', type=str)
        pronoun = request.args.get('pronoun', type=str)
        verb_tense = request.args.get('verb_tense', type=str)
        hr_id = request.args.get('hr_id', type=int)

        check_answer = 'correct'

        grade = {
                'grade': check_answer,
                'hr_id': hr_id,
                'verb': verb
                }

        return jsonify(grade)
    else:
        return jsonify("Format error")


''' WORDBANK '''
@word_bp.route('/wordbank/add/', methods=['GET'])
@login_required
def insert_wordbank():
    word_id = None
    add_type = False
    if request.method == 'GET':
        word_id = request.args.get('word_id', type=int)
        add_type = request.args.get('add_type', type=str)
    if word_id:
        wid = HrWord.query.get(word_id)
        uid = current_user.id

        if add_type == 'add':
          wb = WordBank(user_id=uid,hr_word_id=wid.id)
          db.session.add(wb)
          db.session.commit()
          return jsonify('Added: {}'.format(wid))

        elif add_type == 'rm':
            wb = WordBank.query.filter_by(user_id=uid,hr_word_id=wid.id).first()
            if wb:
                db.session.delete(wb)
                db.session.commit()
                return jsonify('Removed: {}'.format(wid))
            else:
                return jsonify('Word not in your wordbank')
        else:
            return jsonify('Request format error')
    else:
        return jsonify('Request format error')
