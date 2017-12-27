from app import app
from app.models.articles import Article, ArticleText
from flask import Blueprint, render_template

from app.models.words import Definition

article_bp = Blueprint('articles', __name__)

@article_bp.route('/')
def index(page=1):
    all_articles = Article.query.order_by(Article.date)
    return render_template('articles/index.html', all_articles=all_articles)

@article_bp.route('/<article_id>/<article_slug>')
def show(article_id, article_slug):
    a = Article.query.get(article_id)
    at = ArticleText.query.filter(ArticleText.article_id==a.id).first()
    if at != None:
        at = at.text
    else:
        at = ArticleText().get_article_content(a)
    g = Definition().create_glossary(at)
    return render_template('articles/show.html', a=a, at=at, g=g)

