import random
from sqlalchemy.sql.expression import func
from flask import Blueprint, render_template, request, jsonify, escape
from flask_user import login_required, roles_required, current_user

from app import app, db, csrf
from app.models.practice import Definition, WordRole, HrWord, EnWord, format_glossary, PRONOUNS, VERB_TENSES
from app.models.users import WordBank
from app.utils.verbs import Conjugation

practice_bp = Blueprint('practice', __name__)

''' INDEX, SHOW & ADD '''
@practice_bp.route('/')
def index(page=1):
    return render_template('practice/index.html')

@practice_bp.route('/<word_id>')
def show(word_id):
    w = Word.query.get(word_id)
    return render_template('practice/show.html', w=w)


''' DICTIONARY '''
@practice_bp.route('/dictionary')
def dictionary():
    return render_template('practice/dictionary.html')

@practice_bp.route('/define', methods=['GET'])
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
@practice_bp.route('/verbs', methods=['GET'])
def verb_practice():
    load_list = request.args.get('load_list', type=bool)
    if load_list == True:
        verb_query = Definition.query.order_by(func.random()).join(Definition.hr_words, aliased=True).filter(Definition.role_id==31).limit(20).all()
        verblist = format_glossary(verb_query)
        for v in verblist:
            pron = random.choice(PRONOUNS)
            v['pronoun_word'] = pron['word']
            v['pronoun_code'] = pron['code']
            v['verb_tense'] = random.choice(VERB_TENSES)
        return jsonify(verblist)
    else:
        context = {
                'pronouns': PRONOUNS,
                'tenses': VERB_TENSES
                }
        return render_template('practice/verbs.html', context=context)

@practice_bp.route('/verbs/check', methods=['GET'])
def verb_check():
    # check that all args are present
    if set(['answer','verb','pronoun_code','verb_tense','hr_id']).issubset(set([k for k in request.args.keys()])):
        answer = escape(request.args.get('answer', type=str))
        verb = escape(request.args.get('verb', type=str))
        pronoun = escape(request.args.get('pronoun_code', type=str))
        tense = escape(request.args.get('verb_tense', type=str))
        hr_id = escape(request.args.get('hr_id', type=int))

        answer_key = Conjugation(verb,pronoun,tense).conjugate()
        grade = 'correct' if answer_key == answer else 'incorrect'

        grade = {
                'grade': grade,
                'hr_id': hr_id,
                'correct_answer': answer_key,
                'answer': answer,
                'verb': verb
                }

        return jsonify(grade)
    else:
        return jsonify("Format error")


''' WORDBANK '''
@practice_bp.route('/wordbank/add/', methods=['GET'])
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


@practice_bp.route('/conjugate')
def conf():
    verb = 'spavati'
    pronoun = '3S'
    tense = 'past'
    v = Conjugation(verb,pronoun,tense).conjugate()
    return render_template('practice/conjugate.html', v=v)

# Admin actions
@practice_bp.route('/verbs/notaverb', methods=(['POST']))
@csrf.exempt
@login_required
@roles_required('admin')
def rm_verb_role():
    hr_id = request.form.get('hr_id')
    if hr_id:
        for d in Definition.query.filter(Definition.hr_word_id == hr_id, Definition.role_id == 31).all():
            d.role_id=None
        db.session.commit()
        return jsonify('Removed {} from verbs.'.format(hr_id))
    return jsonify(' No word id')
