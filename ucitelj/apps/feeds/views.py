from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader



from .models import Feed


def index(request):
    feed_list = Feed.objects.order_by('name')
    context = {
        'feed_list' : feed_list,
    }
    template = loader.get_template('feeds/index.html')
    return HttpResponse(template.render(context,request))

def detail(request, slug):
    feed = get_object_or_404(Feed, slug=slug)
    context = {
        'feed' : feed,
    }
    template = loader.get_template('feeds/show.html')
    return HttpResponse(template.render(context,request))
