import os
import random
from social.models import SocialProfile
from social.models import get_random_joke
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from allauth.socialaccount.models import SocialAccount


def index(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.get(username=request.POST['username'])
                return render(request, 'register.html', {'error': 'Username is already taken!'})
            except User.DoesNotExist:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                social_profile = SocialProfile(user=user)
                social_profile.save()
                auth.login(request, user)
                return redirect('/')
        else:
            return render(request, 'register.html', {'error': 'Passwords do not match!'})
    else:
        return render(request, 'register.html')




def signin(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password = request.POST['password'])
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            return render (request,'login.html', {'error':'Username or password is incorrect!'})
    else:
        return render(request,'login.html')

def logout(request):
    if request.method == 'GET':
        auth.logout(request)
        return redirect('/')
    else:
        return HttpResponse('<h1>SOMETHING WENT WRONG, TAZER BLIND SPOT HAHA U WIN</h1>')
    
@login_required
def profile(request):
    user = request.user
    data=SocialAccount.objects.filter(provider='google').filter(user=user)
    social_profile = SocialProfile.objects.filter(user=user)
    if data:
        picture = data[0].extra_data['picture']
        name = data[0].extra_data['name']
        bio = get_random_joke()
    else:
        if social_profile:
            picture = social_profile[0].photo.url
            name = social_profile[0].user.username
            bio = social_profile[0].bio

    return render(request, 'profile.html',{'bio':bio, 'name': name, 'picture': picture})
