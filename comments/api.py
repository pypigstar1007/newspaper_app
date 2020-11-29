from django.http import Http404, HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from news.models import News
from .models import likes, dislikes, comment as commentTable
import json
from users.models import userExtraField


def add_like(request):
    if request.user.is_authenticated:
        
        news_id = request.GET.get('articale_id')
        news_is = News.objects.get(id = news_id)
        print(news_is)
        try:
            like_obj = likes.objects.get(for_news = news_is)
        except likes.DoesNotExist:
            like_obj = likes(for_news=news_is)
            like_obj.save()
        
        like_obj.like_by.add(request.user)
        like_obj.save()
        data = {
            'total' : like_obj.like_by.all().exclude(id = news_is.created_by.id).count()
        }
        return HttpResponse(json.dumps(data))

    else:
        raise Http404()

def remove_like(request):
    if request.user.is_authenticated:
        
        news_id = request.GET.get('articale_id')
        news_is = News.objects.get(id = news_id)
        like_obj = likes.objects.get(for_news = news_is)
        like_obj.like_by.remove(request.user)
        like_obj.save()
        data = {
            'total' : like_obj.like_by.all().exclude(id = news_is.created_by.id).count()
        }
        return HttpResponse(json.dumps(data))

    else:
        raise Http404()

def add_dislike(request):
    if request.user.is_authenticated:
        
        news_id = request.GET.get('articale_id')
        news_is = News.objects.get(id = news_id)
        print(news_is)
        try:
            dislike_obj = dislikes.objects.get(for_news = news_is)
        except dislikes.DoesNotExist:
            dislike_obj = dislikes(for_news=news_is)
            dislike_obj.save()
        
        dislike_obj.dislike_by.add(request.user)
        dislike_obj.save()
        data = {
            'total' : dislike_obj.dislike_by.all().exclude(id = news_is.created_by.id).count()
        }
        return HttpResponse(json.dumps(data))

    else:
        raise Http404()

def remove_dislike(request):
    if request.user.is_authenticated:
        
        news_id = request.GET.get('articale_id')
        news_is = News.objects.get(id = news_id)
        print(news_is)
        like_obj = dislikes.objects.get(for_news = news_is)
        like_obj.dislike_by.remove(request.user)
        like_obj.save()
        data = {
            'total' : like_obj.dislike_by.all().exclude(id = news_is.created_by.id).count()
        }
        return HttpResponse(json.dumps(data))

    else:
        raise Http404()


@csrf_exempt
def add_comment(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            article = request.POST['articale_id']
            message = request.POST['message']
            news = News.objects.get(id=article)
            extra= userExtraField.objects.get(user=request.user)
            comments = commentTable(comment_for = news, commented_by=request.user, message=message)
            comments.save()
            data = {'data': serializers.serialize('json', [comments, ])}
            if extra.profile_pic:
                data['profile_pic'] = extra.profile_pic.url
            else:
                data['profile_pic'] = '/static/icon/default-avatar.png'
            return HttpResponse(json.dumps(data))

    raise Http404()

def get_comment(request):
    news_id = request.GET.get('article_id')
    news_is = News.objects.get(id=news_id)
    main_comment = commentTable.objects.filter(comment_for=news_is, parent=None).order_by('-created_at')
    child_comment = commentTable.objects.filter(comment_for=news_is).exclude(parent=None).order_by('-created_at')
    main_comments = []
    child_comments = []
    for comment in main_comment:
        extra = userExtraField.objects.get(user=comment.commented_by)
        obj = {
            'username': comment.commented_by.username,
            'message': comment.message, 
            'parent': comment.parent, 
            'pk': comment.id,
            # 'created_at': comment.created_at
        }
        if extra.profile_pic:
            obj['profile_pic'] = extra.profile_pic.url
        else:
            obj['profile_pic'] = '/static/icon/default-avatar.png'

        main_comments.append(obj)

    for comment in child_comment:
        extra = userExtraField.objects.get(user=comment.commented_by)
        obj = {
            'username': comment.commented_by.username,
            'message': comment.message, 
            'parent': comment.parent.id, 
            'pk': comment.id,
            # 'created_at': comment.created_at
        }
        if extra.profile_pic:
            obj['profile_pic'] = extra.profile_pic.url
        else:
            obj['profile_pic'] = '/static/icon/default-avatar.png'
            
        child_comments.append(obj)
    data = {
        'main_comment': main_comments,
        'child_comment': child_comments 
    }
    return HttpResponse(json.dumps(data))


@csrf_exempt
def add_reply(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            news_is = News.objects.get(id = request.POST['articale_id'])
            messages = request.POST['message']
            parent_comment = commentTable.objects.get(id=request.POST['parent'])
            comments = commentTable(comment_for=news_is, commented_by=request.user, message=messages, parent=parent_comment)
            comments.save()
            data = serializers.serialize('json', [comments, ])
            return HttpResponse(json.dumps(data))
        
    raise Http404()