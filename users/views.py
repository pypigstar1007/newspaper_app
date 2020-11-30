import json
from django.shortcuts import render, redirect, reverse, HttpResponse
from django.http import Http404
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from newspaper.settings import EMAIL_HOST_USER
from .forms import *
from .models import userExtraField


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
                print('here i')
                login(request, user)
                if request.GET.get('next', None):
                    return HttpResponseRedirect(request.GET['next'])
                return HttpResponseRedirect(reverse('index'))
            else:
                print('here')
                return render(request, 'login.html', {'form' : form, 'error':'please give us right password'})
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
            dob = request.POST['dob']
            if password == conf_password:
                # try:
                user = User.objects.create_user(username=user_name, first_name=f_name, last_name = l_name, email=email, password=password)
                user.save()
                user_data = userExtraField(user = user, dob=dob)
                user_data.save()
                subject = "email subscribe notification"
                massage = 'Welcome {0} to our site.'.format(user.first_name)
                send_mail(
                subject,
                massage,
                EMAIL_HOST_USER,
                [user.email, ],
                fail_silently= False,
                )
                print('i am here')
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
                # except :
                #     context={}
                #     context['error'] = "Username already exist."
                #     context['form'] = new_user()
                #     return  render(request, 'signup.html', context)
          
    form = new_user()
    return  render(request, 'signup.html', {'form': form})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('getLogin'))


def myData(request):

    if request.user.is_authenticated:
        user_data = userExtraField.objects.get(user = request.user)
        
        data = {
            'profile_pic': '',
            'dob': user_data.dob.isoformat(),
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email
        }
        if user_data.profile_pic:
            data['profile_pic'] = user_data.profile_pic.url
        # print(data)
        return HttpResponse(json.dumps(data))
    else: 
        raise Http404()


@csrf_exempt
def update_profile(request):
    print('======================', request.POST)
    profile_pic = request.FILES.get('profile_pic', None)
    dob = request.POST.get('dob')
    profilePic = request.POST['profilePic']
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    user = request.user
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    extra = userExtraField.objects.get(user=user)
    print('===============', profile_pic, profilePic)
    if (profile_pic is not None) or (profilePic == 'False'):
        if extra.profile_pic :
            extra.profile_pic.delete()
        extra.profile_pic = profile_pic
    extra.dob = dob
    extra.save()
    return HttpResponse({'update': 'updated successful.'})


def check_username(request):
    val = request.GET.get('username')
    users = User.objects.filter(username=val).count()
    data = {
        'total_user': users
    }
    return HttpResponse(json.dumps(data))