from django.shortcuts import render, redirect
from datetime import date, datetime
from .models import News, Category, images
from .forms import NewsForms
from django.http import Http404

# Create your views here.
def index(request):
    context = {}
    news = News.objects.filter(created_at__date = date.today())
    print(news)
    context['todays_news'] = news
    return render(request, 'dashboard.html', context)


def add_news(request):
    context = {}
    if request.method == 'POST':
        form = NewsForms(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.created_by = request.user
            news.save()
            return redirect('index')

    form = NewsForms()
    context['form'] = form
    return render(request, 'addNews.html', context)        


def all_news(request):
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
        'form': form
    }

    return render(request, 'updateNews.html', context)


def read_full_news(request, slug, id):
    try:
        get_news = News.objects.get(id=id)
    except News.DoesNotExist:
        raise Http404()
    
    related_news = News.objects.filter(created_at__date = date.today(), category = get_news.category).exclude(id=get_news.id).order_by('-created_at')[ : 5]
    context = {}
    print(get_news.created_at)
    context['main_news'] = get_news
    context['related_newses'] = related_news
    context ['now'] = datetime.now()
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

    