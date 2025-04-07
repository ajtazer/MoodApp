import os
import random
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from django.utils import timezone
import uuid
from datetime import datetime

# Define the media directory path relative to the base directory
MEDIA_DIR = os.path.join(settings.BASE_DIR, 'media')
PROFILES_DIR = os.path.join(MEDIA_DIR, 'profiles') # Define profiles subdir

def get_random_joke():
    jokes = [
        "What do dentists call their x-rays? Tooth pics!",
        "Why did the melon jump into the lake? It wanted to be a water-melon.",
        "Why was 6 afraid of 7? Because 7 ate 9!",
        "Grandma: Back in our days, you could buy bread, milk, soaps, spices, eggs, meat, all for a dollar.",
        "Little Kid: You can't do that now. They have CCTVs everywhere!",
        "When your teacher asks 'Where's your homework?' It took a sick day. It had too many problems.",
        "You can't trust atoms. They make up everything!",
        "Why won't it hurt if you hit your friend with a 2-liter of soda? Because it's a soft drink!",
        "Why do mushrooms get invited to all the best parties? He was a fun-gi!",
        "What has four wheels and flies? Garbage truck",
        "I got fired from my job at the bank today. An old lady came in and asked me to check her balance, so I pushed her over.",
        "What do you call an elephant that doesn't matter? An irrelephant.",
        "Dad, can you put my shoes on? No, I don't think they'll fit me.",
        "Why do you smear peanut butter on the road? To go with the traffic jam.",
        "Where did Napoleon keep his armies? In his sleevies.",
        "Did you hear about the actor who fell through the floorboards? He was just going through a stage.",
        "Did you hear about the claustrophobic astronaut? He just needed a little space.",
        "Did you hear about the guy who stole a calendar? He got 12 months; they say his days are numbered.",
        "I used to be addicted to soap, but I'm clean now.",
        "There are two types of people in the world, those who can extrapolate from incomplete data.",
        "What's the best part about living in Switzerland? Not sure, but the flag is a big plus.",
        "Why did the dog cross the road? To get to the barking lot!",
        "What do you call a bear with no teeth? A gummy bear.",
        "A nurse told me, 'Sorry for the wait!' I replied, 'It's alright, I'm patient.'",
        "Working in a mirror factory is something I could totally see myself doing.",
        "I'm terrified of elevators, so I'm going to start taking steps to avoid them.",
        "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them.",
        "Why are pirates called pirates? Because they arrrr!",
        "Helvetica and Times New Roman walk into a bar. 'Get out of here!', shouts the bartender. 'We don't serve your type.'",
        "Can February March? No, but April May!",
        "What do you call a cold dog? A chili dog!"
    ]
    return random.choice(jokes)

def get_default_profile_photo():
    """Selects a random photo from the media/profiles directory."""
    try:
        # Ensure the profiles directory exists
        if not os.path.exists(PROFILES_DIR):
            os.makedirs(PROFILES_DIR)
        
        # Look for images directly within the 'profiles' subdirectory
        image_files = [f for f in os.listdir(PROFILES_DIR) if os.path.isfile(os.path.join(PROFILES_DIR, f))]
        if image_files:
            # Return path relative to MEDIA_ROOT (e.g., 'profiles/random_image.jpg')
            return os.path.join('profiles', random.choice(image_files)) 
    except Exception as e:
        print(f"Error selecting random default photo: {e}")
    # Fallback to a known default or None
    # return 'profiles/default_avatar.png' # Example: if you add a default image
    return None

class SocialProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, default=get_random_joke)
    # Use upload_to='profiles/' - Django handles creating MEDIA_ROOT/profiles/
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True, default=get_default_profile_photo)
    
    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to="posts")
    caption = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.caption
    
    def like(self, user):
        """Add a like from a user"""
        if user not in self.liked_by.all():
            self.liked_by.add(user)
            self.likes += 1
            self.save()
            return True
        return False
    
    def unlike(self, user):
        """Remove a like from a user"""
        if user in self.liked_by.all():
            self.liked_by.remove(user)
            self.likes -= 1
            self.save()
            return True
        return False

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.id}"
