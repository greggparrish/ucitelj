from sqlalchemy.sql.expression import func
from flask import Blueprint, render_template, request, jsonify

from app.models.words import Definition, HrWord, EnWord

word_bp = Blueprint('words', __name__)


# DICTIONARY
@word_bp.route('/dictionary')
def dictionary():
    return render_template('words/dictionary.html')


@word_bp.route('/define', methods=['GET'])
def define():
    dd = request.args.get('dict_dir')
    if dd == 'hr_en':
        hr_word = request.args.get('q_word').lower()
        word_defs = Definition.query.join(Definition.hr_words, aliased=True).filter(HrWord.term.like("{}%".format(hr_word))).order_by(func.length(HrWord.term)).limit(8).all()
        deflist = [d.hr_en_to_json() for d in word_defs]
    elif dd == 'en_hr':
        en_word = request.args.get('q_word').lower()
        word_defs = Definition.query.join(Definition.en_words, aliased=True).filter(EnWord.term.like("{}%".format(en_word))).order_by(func.length(EnWord.term)).limit(8).all()
        deflist = [d.en_hr_to_json() for d in word_defs]
    else:
        deflist = False
    return jsonify(deflist=deflist)
