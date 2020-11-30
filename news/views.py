from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import date, datetime

from .models import News, Category, images, MyFavoriteNews
from .forms import NewsForms
from comments.models import likes, dislikes

# Create your views here.
def index(request):
    context = {}
    all_cat = Category.objects.all()
    todays_news = []
    newss = News.objects.all()
    for i in newss:
        print(i.created_at)
    for cat in all_cat:

        news = News.objects.filter(created_at__date = date.today(), category=cat)
        print(news)
        obj = {
            "category": cat,
            "news": news
        }
        todays_news.append(obj)
    print(todays_news)
    context['todays_news'] = todays_news
    return render(request, 'dashboard.html', context)


def add_news(request):
    context = {}
    if (request.user.is_authenticated) == False:
        return redirect('getLogin')
    if request.method == 'POST':
        headline = request.POST['headline']
        title = request.POST['title']
        news_body = request.POST['news_body']
        category =Category.objects.get(id= request.POST['category'])
        news = News(headline = headline, title=title, news_body=news_body, category=category, created_by=request.user)
        news.save()
        image1 = request.FILES.get('image1', None)
        image2 = request.FILES.get('image2', None)
        image3 = request.FILES.get('image3', None)
        if image1 is not None:
            image = images(image_for = news, imgage=image1)
            image.save()

        if image2 is not None:
            image = images(image_for = news, imgage=image2)
            image.save()
        if image3 is not None:
            image = images(image_for = news, imgage=image3)
            image.save()
        return redirect('index')

    category = Category.objects.all()
    context['categorys'] = category
    return render(request, 'addNews.html', context)        


def all_news(request):
    if (request.user.is_authenticated) == False:
        return redirect('getLogin')
    news = News.objects.filter(created_by = request.user)
    imageses = images.objects.filter(image_for__in = news)
    context = {
        'my_news': news,
        'image': imageses
    }

    return render(request, 'myAllPostedNews.html', context)


@login_required(login_url='/login/')
def favourite_news(request):
    all_likess = likes.objects.filter(like_by= request.user)
    newses = []
    context = {}
    ids = []
    for likess in all_likess:
        newses.append(likess.for_news)
        ids.append(likess.for_news.id)
    print(newses)
    imageses = images.objects.filter(image_for__in = newses)
    fev_cats = MyFavoriteNews.objects.get(users = request.user)
    fev_cat_news = News.objects.filter(category__in = fev_cats.fav_categorys.all()).exclude(id__in=ids).order_by('-created_at')
    print(fev_cat_news)
    context['newses'] = newses
    context['image'] = imageses
    context['categorys']= Category.objects.all()
    context['fev_cat_news'] = fev_cat_news
    return render(request, 'favourite_news.html', context)


@login_required(login_url='/login/')
def edit_my_news(request, slug, id):
    
    try:
        news = News.objects.get(id=id)
    except News.DoesNotExist:
        raise Http404()
    
    if request.method == 'POST':
        form = NewsForms(request.POST, instance=news)
        if form.is_valid():
            form.save()
            return redirect('my_all_news')
    
    form = NewsForms(instance=news)
    iamgess = images.objects.filter(image_for = news)
    context = {
        'form': form,
        'news': news,
        'imagess': iamgess
    }

    return render(request, 'updateNews.html', context)


def read_full_news(request, slug, id):
    try:
        get_news = News.objects.get(id=id)
    except News.DoesNotExist:
        raise Http404()
    
    related_news = News.objects.filter(created_at__date = date.today(), category = get_news.category).exclude(id=get_news.id).order_by('-created_at')[ : 5]
    context = {}
    image_list = []
    imagess = images.objects.filter(image_for = get_news)
    lists = ['First', 'Second', 'Third']
    context['like'] = 'text-secondary'
    context['like_count'] = 0
    context['dislike'] = 'text-secondary'
    context['dislike_count'] = 0
    if request.user.is_authenticated:
        check_for_like = likes.objects.filter(for_news = get_news, like_by = request.user)
        if(check_for_like.count() > 0):
            context['like'] = 'text-primary'
            context['like_count'] = check_for_like.count()
        
        check_for_dislike = dislikes.objects.filter(for_news = get_news, dislike_by = request.user)
        if(check_for_dislike.count() > 0):
            context['dislike'] = 'text-danger'
            context['dislike_count'] = check_for_dislike.count()
    for i in range(len(imagess)):
        obj = {
            'pos': lists[i],
            'images': imagess[i]
        }
        image_list.append(obj)

    print(image_list)
    context['main_news'] = get_news
    context['related_newses'] = related_news
    context ['now'] = datetime.now()
    context['images'] = image_list
    return render(request, 'detailsOfNews.html', context)


def deletes(request, slug, id):
    try:
        news = News.objects.get(id=id)
    except News.DoesNotExist:
        raise Http404()

    filtered_images = images.objects.filter(image_for = news)
    for image in filtered_images:
        image.delete()
    news.delete()
    return redirect('my_all_news')

    
def add_fev(request):
    cat_id = request.GET.get('cat_id')
    cat = Category.objects.get(id=cat_id)
    try:
        my_fev = MyFavoriteNews.objects.get(users=request.user)
    except MyFavoriteNews.DoesNotExist:
        my_fev = MyFavoriteNews(users=request.user)
        my_fev.save()

    my_fev.fav_categorys.add(cat)
    news = News.objects.filter(category=cat).order_by('-created_at')
    return HttpResponse('category added.')