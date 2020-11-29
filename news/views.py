from django.shortcuts import render, redirect
from datetime import date, datetime
from .models import News, Category, images
from .forms import NewsForms
from django.http import Http404

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
    context = {
        'my_news': news
    }

    return render(request, 'myAllPostedNews.html', context)


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
    context = {
        'form': form,
        'news': news
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

    