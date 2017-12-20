import datetime

from django.db.models import OuterRef, Subquery, Max
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader


from ..feeds.models import Feed, Subscription
from ..words.models import Rijec, Definition
from .models import Article, ArticleText
from .stemmer import create_wordlist


def index(request):
    ''' Get articles within last week from subbed feeds,
        or if user not logged in or has no subs,
        then get articles from feeds 1, 2 & 3
    '''
    if request.user.is_authenticated:
        user_subs = list(
            Subscription.objects.filter(
                user_id=request.user.id).values_list(
                'feed_id', flat=True))
        if user_subs:
            user_subs = Feed.objects.filter(
                id__in=user_subs).values_list(
                'id', flat=True)
        else:
            user_subs = Feed.objects.filter(
                id__in=[
                    1, 2, 3]).values_list(
                'id', flat=True)
    else:
        user_subs = Feed.objects.filter(
            id__in=[
                1, 2, 3]).values_list(
            'id', flat=True)

    articles = Article.objects.filter(
        feed_id__in=user_subs).order_by('feed_id', '-date').filter(
        date__gte=datetime.date.today() -
        datetime.timedelta(
            days=7))
    context = {
        'articles': articles,
    }
    template = loader.get_template('articles/index.html')
    return HttpResponse(template.render(context, request))


def detail(request, slug):
    '''
    get article, text if exists, if not, get_article_content, save, render
    '''
    article = get_object_or_404(Article.objects.prefetch_related(), slug=slug)
    try:
        at = list(ArticleText.objects.get(article_id=article.id))
    except BaseException:
        at = ArticleText.get_article_content(article)
    wordlist = create_wordlist(at)
    glossary = []
    for word in wordlist:

        ''' First check if word exists as is '''
        definition = Definition.objects.filter(
            rijec__term=word).select_related()

        ''' If not, check if any words start with stemmed root '''
        if len(definition) == 0:
            definition = Definition.objects.filter(rijec__term__startswith=wordlist[word])[
                :3].select_related()

        ''' Final check, remove last letter and try again for stemmed root '''
        if len(definition) == 0 and len(wordlist[word][:-1]) > 2:
            definition = Definition.objects.filter(
                rijec__term__startswith=wordlist[word][:-1])[:3].select_related()
        if len(definition) > 0:
            glossary.append(definition)
    context = {
        'article': article,
        'at': at,
        'wordlist': wordlist,
        'glossary': glossary
    }
    template = loader.get_template('articles/show.html')
    return HttpResponse(template.render(context, request))
