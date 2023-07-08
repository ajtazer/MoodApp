import os
import random
from social.models import Profile
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from allauth.socialaccount.models import SocialAccount


def index(request):
    return render(request, 'home.html')

def signup(request):
    photo_folder = 'media/dp/'
    photo_files = os.listdir(photo_folder)
    random_photo = random.choice(photo_files)
    photo_path = os.path.join(photo_folder, random_photo)
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.get(username=request.POST['username'])
                return render(request, 'register.html', {'error': 'Username is already taken!'})
            except User.DoesNotExist:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                bio = get_random_joke()
                is_google_auth = SocialAccount.objects.filter(user=user, provider='google').exists()
                profile = Profile(user=user, photo=photo_path, bio=bio, is_google_auth=is_google_auth)
                profile.save()
                auth.login(request, user)
                return redirect('/')
        else:
            return render(request, 'register.html', {'error': 'Password does not match!'})
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
    


def get_random_dp(dp_folder):
    """Returns a random image from the dp_folder directory."""
    dp_files = os.listdir(dp_folder)
    dp_file = random.choice(dp_files)
    return os.path.join(dp_folder, dp_file)

def get_profile_dp(request, user):
    """Returns the user's profile photo, or a random dp if the user does not have a profile photo."""
    dp = user.profile.photo
    if dp is None:
        dp = get_random_dp('dp_folder')
    return dp

@login_required
def profile(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'profile.html', context)

def get_random_joke():
    jokes = [
        "What do dentists call their x-rays? Tooth pics!",
        "Why did the melon jump into the lake? It wanted to be a water-melon.",
        "Why was 6 afraid of 7? Because 7 ate 9!",
        "Grandma: Back in our days, you could buy bread, milk, soaps, spices, eggs, meat, all for a dollar.",
        "Little Kid: You can’t do that now. They have CCTVs everywhere!",
        "When your teacher asks 'Where’s your homework?' It took a sick day. It had too many problems.",
        "You can’t trust atoms. They make up everything!",
        "Why won’t it hurt if you hit your friend with a 2-liter of soda? Because it’s a soft drink!",
        "Why do mushrooms get invited to all the best parties? He was a fun-gi!",
        "What has four wheels and flies? Garbage truck",
        "I got fired from my job at the bank today. An old lady came in and asked me to check her balance, so I pushed her over.",
        "What do you call an elephant that doesn’t matter? An irrelephant.",
        "Dad, can you put my shoes on? No, I don’t think they’ll fit me.",
        "Why do you smear peanut butter on the road? To go with the traffic jam.",
        "Where did Napoleon keep his armies? In his sleevies.",
        "Did you hear about the actor who fell through the floorboards? He was just going through a stage.",
        "Did you hear about the claustrophobic astronaut? He just needed a little space.",
        "Did you hear about the guy who stole a calendar? He got 12 months; they say his days are numbered.",
        "I used to be addicted to soap, but I’m clean now.",
        "There are two types of people in the world, those who can extrapolate from incomplete data.",
        "What’s the best part about living in Switzerland? Not sure, but the flag is a big plus.",
        "Why did the dog cross the road? To get to the barking lot!",
        "What do you call a bear with no teeth? A gummy bear.",
        "A nurse told me, 'Sorry for the wait!' I replied, 'It’s alright, I’m patient.'",
        "Working in a mirror factory is something I could totally see myself doing.",
        "I’m terrified of elevators, so I’m going to start taking steps to avoid them.",
        "Did you hear about the mathematician who’s afraid of negative numbers? He’ll stop at nothing to avoid them.",
        "Why are pirates called pirates? Because they arrrr!",
        "Helvetica and Times New Roman walk into a bar. 'Get out of here!', shouts the bartender. 'We don’t serve your type.'",
        "Can February March? No, but April May!",
        "What do you call a cold dog? A chili dog!"
    ]
    return random.choice(jokes)
