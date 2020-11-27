from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import *
from django.http import HttpResponseRedirect

# Create your views here.

def getLogin(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = name_users(request.POST)   
        if form.is_valid():      
            username = request.POST['username']  
            password = request.POST['password'] 
            user = authenticate(request, username = username, password=password)
            if user:
                login(request, user)
            if request.GET.get('next', None):
                return HttpResponseRedirect(request.GET['next'])
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'users/login.html', {'form' : form, 'error':'please give us right password'})
    form = name_users()
    return render(request, 'login.html', {'form': form})


def signup(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = new_user(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['username']
            f_name = form.cleaned_data['f_name']
            l_name = form.cleaned_data['l_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            conf_password = form.cleaned_data['conf_password']
            if password == conf_password:
                try:
                    user = User.objects.create_user(username=user_name, first_name=f_name, last_name = l_name, email=email, password=password)
                    user.save()
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                except :
                    context={}
                    context['error'] = "Username already exist."
                    context['form'] = new_user()
                    return  render(request, 'signup.html', context)
          
    form = new_user()
    return  render(request, 'signup.html', {'form': form})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('getLogin'))

