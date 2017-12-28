import os
import json
from flask import Blueprint, render_template

from app import app
from app.models.articles import Article, ArticleText
from app.models.words import Definition

article_bp = Blueprint('articles', __name__)

@article_bp.route('/')
def index(page=1):
    all_articles = Article.query.order_by(Article.date)
    return render_template('articles/index.html', all_articles=all_articles)

@article_bp.route('/<article_id>/<article_slug>')
def show(article_id, article_slug):
    a = Article.query.get(article_id)
    article_text = ArticleText.query.filter(ArticleText.article_id==a.id).first()
    if article_text != None:
        at = article_text.text
    else:
        at = ArticleText().get_article_content(a)
    if article_text.has_dict == True:
        g_dir = os.path.join( app.root_path, 'static/public/glossaries/')
        glossary = json.loads(g_dir+article_id+'.json')
    else:
        glossary = Definition().create_glossary(article_id, at)
    return render_template('articles/show.html', a=a, at=at, glossary=glossary)

