import datetime

from django.db.models import OuterRef, Subquery, Max
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader


from ..feeds.models import Feed, Subscription
from .models import Article
from .get_articles import update_articles


def index(request):
    ''' Get articles within last week from subbed feeds,
        or if user not logged in or has no subs,
        then get articles from feeds 1, 2 & 3
    '''
    if request.user.is_authenticated():
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
        feed_id__in=user_subs).order_by('feed_id').filter(
        date__gte=datetime.date.today() -
        datetime.timedelta(
            days=7))
    context = {
        'articles': articles,
    }
    template = loader.get_template('articles/index.html')
    return HttpResponse(template.render(context, request))

def detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    context = {
        'article' : article,
    }
    template = loader.get_template('articles/show.html')
    return HttpResponse(template.render(context,request))
