from app import app
from app.models.words import WordRole, HrWord, EnWord
from flask import Blueprint, render_template

word_bp = Blueprint('words', __name__)

@word_bp.route('/')
def index(page=1):
    all_words = Word.query.order_by(Words.term)
    return render_template('words/index.html', all_words=all_words)

@word_bp.route('/<word_id>')
def show(word_id):
    w = Word.query.get(word_id)
    return render_template('words/show.html', w=w)

