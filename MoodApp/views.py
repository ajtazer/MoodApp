from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth

def index(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.get(username = request.POST['username'])
                return render (request,'register.html', {'error':'Username is already taken!'})
            except User.DoesNotExist:
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                auth.login(request,user)
                return redirect('/')
        else:
            return render (request,'register.html', {'error':'Password does not match!'})
    else:
        return render(request,'register.html')

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