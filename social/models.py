import os
import random
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount


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

random_photo = random.choice(os.listdir('media/'))
class SocialProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, default=get_random_joke())
    photo = models.ImageField(blank=True, default=random_photo)
    def __str__(self):
        return self.user.username