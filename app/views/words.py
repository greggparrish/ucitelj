from sqlalchemy.sql.expression import func
from flask import Blueprint, render_template, request, jsonify

from app import app
from app.models.words import Definition, WordRole, HrWord, EnWord

word_bp = Blueprint('words', __name__)

@word_bp.route('/')
def index(page=1):
    all_words = Word.query.order_by(Words.term)
    return render_template('words/index.html', all_words=all_words)

@word_bp.route('/<word_id>')
def show(word_id):
    w = Word.query.get(word_id)
    return render_template('words/show.html', w=w)

@word_bp.route('/dictionary')
def dictionary():
    w='111'
    return render_template('words/dictionary.html', w=w)

@word_bp.route('/define', methods=['GET'])
def define():
    dd = request.args.get('dict_dir')
    if dd == 'hr_en':
        hr_word = request.args.get('q_word')
        word_defs = Definition.query.join(Definition.hr_words, aliased=True).filter(HrWord.term.like("{}%".format(hr_word))).limit(6).all()
        deflist = [ d.hr_en_to_json() for d in word_defs ]
    elif dd == 'en_hr':
        en_word = request.args.get('q_word')
        word_defs = Definition.query.join(Definition.en_words, aliased=True).filter(EnWord.term.like("{}%".format(en_word))).limit(6).all()
        deflist = [ d.en_hr_to_json() for d in word_defs ]
    else:
        deflist=False
    return jsonify(deflist=deflist)
