import os
import json
from flask import Blueprint, render_template
from flask_login import current_user

from app import app, db
from app.models.users import WordBank
from app.models.articles import Article, ArticleText
from app.models.words import Definition, create_glossary

article_bp = Blueprint('articles', __name__)

@article_bp.route('/')
def index(page=1):
    all_articles = Article.query.order_by(Article.date)
    return render_template('articles/index.html', all_articles=all_articles)

@article_bp.route('/<article_id>/<article_slug>')
def show(article_id, article_slug):
    wb = []
    a = Article.query.get(article_id)
    article_text = ArticleText.query.filter(ArticleText.article_id==a.id).first()
    if article_text != None:
        at = article_text.text
    else:
        at = ArticleText().get_article_content(a)
    if at == False:
        return render_template('errors/connection.html')
    elif article_text and article_text.has_dict == True:
        g_dir = os.path.join( app.root_path, 'static/public/glossaries/')
        try:
            glossary = json.load(open(g_dir+article_id+'.json'))
        except:
            glossary = create_glossary(article_id, at)
    else:
        glossary = create_glossary(article_id, at)

    ''' Get user saved words if logged in '''
    if current_user.is_authenticated:
        wbq = WordBank.query.with_entities(WordBank.hr_word_id).filter_by(user_id=current_user.id).all()
    if wbq:
        wb = [ w[0] for w in wbq ]
    article = {
            'a': a,
            'at': at,
            'glossary': glossary,
            'wb': wb
            }
    return render_template('articles/show.html', article=article)

