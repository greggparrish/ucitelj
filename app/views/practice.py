import random
from sqlalchemy.sql.expression import func
from flask import Blueprint, render_template, request, redirect, jsonify, escape, flash, url_for
from flask_user import login_required, roles_required, current_user

from app import db, csrf
from app.models.practice import Verb, VerbType, WordCase, Noun, Adjective, Adverb
from app.forms.practice import WordCaseForm, VerbTypeForm, VerbForm, NounForm, AdjectiveForm, AdverbForm
from app.models.words import Definition, WordRole, HrWord, EnWord, format_glossary, PRONOUNS, VERB_TENSES, GENDERS
from app.models.users import WordBank
from app.utils.verbs import Conjugation

practice_bp = Blueprint('practice', __name__)

@practice_bp.route('/')
def index():
    return render_template('practice/index.html')

@practice_bp.route('/list')
@login_required
@roles_required('admin')
def listall():
    wcs = WordCase.query.all()
    vts = VerbType.query.all()
    nouns = Noun.query.all()
    verbs = Verb.query.all()
    adjs = Adjective.query.all()
    advs = Adverb.query.all()
    context = {
            'wcs': wcs,
            'vts': vts,
            'nouns': nouns,
            'verbs': verbs,
            'adjs': adjs,
            'advs': advs,
            }
    return render_template('practice/listall.html', context=context)

@practice_bp.route('/verbs', methods=['GET'])
def verbs():
    load_list = request.args.get('load_list', type=bool)
    if load_list == True:
        verb_query = Definition.query.order_by(func.random()).join(Definition.hr_words, aliased=True).filter(Definition.role_id==31).limit(20).all()
        verblist = format_glossary(verb_query)
        for v in verblist:
            p = random.choice(PRONOUNS)
            p_code = p['code']+random.choice(GENDERS) if len(p['code']) == 2 else p['code']
            v['pronoun_word'] = p['word']
            v['pronoun_code'] = p_code
            vt = random.choice(VERB_TENSES)
            # filter out imperative if not 2S, 2P or 1P
            v['verb_tense'] = 'present' if vt == 'imperative' and p_code[:-1] not in ['2S','2P','1P'] else vt
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


# WORDBANK
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
            check_word = WordBank.query.filter_by(user_id=uid,hr_word_id=wid.id).first()
            if check_word:
                return jsonify('Word already in your wordbank: {}'.format(wid.term))
            else:
                wb = WordBank(user_id=uid,hr_word_id=wid.id)
                db.session.add(wb)
                db.session.commit()
                return jsonify('Added: {}'.format(wid.term))

        elif add_type == 'rm':
            wb = WordBank.query.filter_by(user_id=uid,hr_word_id=wid.id).first()
            if wb:
                db.session.delete(wb)
                db.session.commit()
                return jsonify('Removed: {}'.format(wid.term))
            else:
                return jsonify('Word not in your wordbank')
        else:
            return jsonify('Request format error')
    else:
        return jsonify('Request format error')


@practice_bp.route('/conjugate')
def conj_test():
    verb = random.choice(['spavati', 'bruniti', 'vidjeti', 'kupovati'])
    p = random.choice(PRONOUNS)['code']
    pronoun = p+random.choice(GENDERS) if len(p) == 2 else p
    tense = random.choice(VERB_TENSES)
    v = Conjugation(verb,pronoun,tense).conjugate()
    return render_template('practice/conjugate.html', v=v)
