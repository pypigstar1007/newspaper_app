from django.shortcuts import render
from .models import News, Category
from .forms import NewsForms
# Create your views here.
def index(request):
    return render(request, 'dashboard.html')


def add_news(request):
    context = {}
    if request.method == 'POST':
        pass

    form = NewsForms()
    context['form'] = form
    return render(request, 'addNews.html', context)        
