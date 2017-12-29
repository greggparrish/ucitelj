import re
import requests

from bs4 import BeautifulSoup
from slugify import slugify

from app import app, db


class Article(db.Model):
    '''
    Article base: FK to feed, rel w/ ArticleText
    '''
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    feed_id = db.Column(db.Integer, db.ForeignKey('feeds.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(250), nullable=False)
    date = db.Column(db.DateTime)
    img_url = db.Column(db.String(250))
    permalink = db.Column(db.String(250), nullable=False, unique=True)
    slug = db.Column(db.String(250), nullable=False, unique=True)
    text = db.relationship("ArticleText", uselist=False, backref="article")

    def __repr__(self):
        return '<Article {}: {}>'.format(self.feed.name, self.title)


class ArticleText(db.Model):
    '''
    Article text: Added on first visit to article.show via get_article_content
    '''
    __tablename__ = 'article_texts'
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id', ondelete='CASCADE'), nullable=False, unique=True)
    has_dict = db.Column(db.Boolean)
    text = db.Column(db.Text)

    def get_article_content(self, article):
        '''
        Get article body from body_tag, grab all p tags, add to db as string
        Return: article text string as at
        '''
        try:
          r = requests.get(article.permalink, timeout=2)
        except Exception as e:
          return False
        if r:
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
                if p.text and p.text != '</p>' and '[CDATA' not in p:
                    at += "<p>{}</p>".format(p.text.strip())
            new_text = ArticleText(
                    article_id=article.id,
                    text=at
                    )
            db.session.add(new_text)
            db.session.commit()
            return at

    def __str__(self):
        return "Article text for: {}".format(self.article.title)
