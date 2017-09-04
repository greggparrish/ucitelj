from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader


from .models import Feed, Subscription


def index(request):
    feed_list = Feed.objects.order_by('name')
    user_subs = list(Subscription.objects.filter(user_id=request.user.id).values_list('feed_id', flat=True))
    context = {
        'feed_list' : feed_list,
        'user_subs' : user_subs
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

@login_required
def subscription(request):
    feed_id = None
    sub_type=None
    if request.method == 'GET':
        feed_id = request.GET.get('feed_id', False)
        sub_type = request.GET.get('sub_type', False)
    if feed_id and sub_type:
        fid = Feed.objects.get(id=int(feed_id))
        uid = request.user.id
        if sub_type == 'sub':
          sub, created = Subscription.objects.get_or_create(user_id=uid,feed_id=fid.id)
        else:
          Subscription.objects.filter(user_id=uid, feed_id=fid).delete()
    return HttpResponse('success')

