import re
import requests

from bs4 import BeautifulSoup
from slugify import slugify

from app import app, db
from app.models.feeds import Feed


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    feed_id = db.Column(db.Integer, db.ForeignKey(Feed.id))
    title = db.Column(db.String(250))
    date = db.Column(db.DateTime)
    img_url = db.Column(db.String(250))
    permalink = db.Column(db.String(250), unique=True)
    slug = db.Column(db.String(250))
    text = db.relationship("ArticleText", uselist=False, backref="article")

    def __repr__(self):
        return '<Article {}: {}>'.format(self.feed.name, self.title)


class ArticleText(db.Model):
    __tablename__ = 'article_texts'
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey(Article.id))
    text = db.Column(db.Text)

    def get_article_content(self, article):
        r = requests.get(article.permalink)
        soup = BeautifulSoup(r.content, 'lxml')
        at = ''
        e, n = re.split('\.|#', article.feed.body_tag)
        s = '#' if '#' in article.feed.body_tag else '.'
        if '#' in article.feed.body_tag:
            bt = soup.find(e, id=n)
        else:
            bt = soup.find(e, class_=n)
        ps = bt.find_all('p')
        for p in ps:
            if p.text != '':
                at + "<p>{}</p>".format(p.text.strip())

        with app.app_context():
            db.create_all()
            new_text = ArticleText(article=article, text=at)
            db.add(new_text)
            db.commit()
        return at

    def __str__(self):
        return "Article text for: {}".format(self.article.title)
