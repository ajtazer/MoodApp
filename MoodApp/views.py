import os
import random
from social.models import SocialProfile, Post, Comment
from social.models import get_random_joke
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from allauth.socialaccount.models import SocialAccount
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.conf import settings

@login_required
def feed(request):
    # Get all posts ordered by creation date (newest first)
    posts = Post.objects.all().order_by('-created')
    
    # Check which posts the current user has liked
    for post in posts:
        post.user_has_liked = request.user in post.liked_by.all()
    
    return render(request, 'feed.html', {'posts': posts})

@login_required
def like_post(request, post_id):
    """Handle post like action"""
    post = get_object_or_404(Post, id=post_id)
    
    # Toggle like status
    if request.user in post.liked_by.all():
        post.unlike(request.user)
        action = 'unliked'
    else:
        post.like(request.user)
        action = 'liked'
    
    # Return JSON response for AJAX or redirect for non-JS
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'likes': post.likes,
            'action': action
        })
    else:
        return redirect('Feeds Page')

@login_required
def add_comment(request, post_id):
    """Add a comment to a post"""
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        comment_text = request.POST.get('comment_text', '').strip()
        
        if comment_text:
            # Create new comment
            comment = Comment.objects.create(
                post=post,
                user=request.user,
                text=comment_text
            )
            
            # Return JSON response for AJAX or redirect for non-JS
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'comment_id': str(comment.id),
                    'username': comment.user.username,
                    'text': comment.text,
                    'created': comment.created.strftime('%B %d, %Y %H:%M')
                })
    
    # Default redirect to feed
    return redirect('Feeds Page')

@login_required
def post_detail(request, post_id):
    """Display a detailed view of a post with comments"""
    post = get_object_or_404(Post, id=post_id)
    post.user_has_liked = request.user in post.liked_by.all()
    comments = post.comments.all()
    
    # Check if the post author is the creator
    is_creator = (post.user == 'tazer') # Assuming 'tazer' is the admin username
    
    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'is_creator': is_creator # Pass the variable to the template
    })

@login_required()
def upload(request):
    if request.method=="POST":
        user=request.user.username
        img=request.FILES.get("images")
        caption=request.POST['caption']

        new_post=Post.objects.create(user=user, image=img, caption=caption)
        new_post.save()
        return redirect("/")
    else:
        return HttpResponse("<h1>File Uploaded EASTER EGG Lesgo</h1>")

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
                # SocialProfile is created automatically via signal or default
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
    
    # Ensure a SocialProfile exists for the user
    social_profile, created = SocialProfile.objects.get_or_create(user=user)
    
    # Try to get Google specific data
    google_data = SocialAccount.objects.filter(provider='google', user=user).first()
    
    if google_data:
        picture = google_data.extra_data.get('picture')
        name = google_data.extra_data.get('name', user.username)
        # If the social profile was just created and has no photo, 
        # try to fetch and save the Google picture
        if created and picture and not social_profile.photo:
            try:
                # Basic image fetching (consider a more robust solution for production)
                import requests
                response = requests.get(picture, stream=True)
                if response.status_code == 200:
                    # Create a filename (e.g., user_id.jpg)
                    filename = f"{user.id}.{picture.split('.')[-1].split('?')[0]}"
                    social_profile.photo.save(filename, ContentFile(response.content), save=True)
                else:
                    print(f"Failed to fetch Google profile picture: {response.status_code}")
            except Exception as e:
                print(f"Error fetching/saving Google picture: {e}")
    else:
        # For non-Google or direct sign-up users
        name = user.username
    
    # Now get the photo URL from the SocialProfile (might be Google's or the default random one)
    picture_url = social_profile.photo.url if social_profile.photo else None
    bio = social_profile.bio
    
    # Add creator highlight logic
    is_creator = (user.username == 'tazer') # Assuming 'tazer' is the admin username

    return render(request, 'profile.html', {
        'bio': bio, 
        'name': name, 
        'picture': picture_url,
        'is_creator': is_creator
    })

@login_required
def explore(request):
    users = User.objects.all()
    
    user_profiles = []
    for user in users:
        try:
            # Ensure profile exists
            social_profile, _ = SocialProfile.objects.get_or_create(user=user)
            
            # Try to get Google account data if available
            google_data = SocialAccount.objects.filter(provider='google').filter(user=user).first()
            
            picture_url = social_profile.photo.url if social_profile.photo else None
            name = user.username

            if google_data:
                # Prefer Google name if available
                name = google_data.extra_data.get('name', user.username)
                # Use Google picture if profile photo is missing
                if not picture_url:
                     picture_url = google_data.extra_data.get('picture')

            is_creator = (user.username == 'tazer')
            
            user_profiles.append({
                'username': user.username,
                'name': name,
                'picture': picture_url,
                'id': user.id,
                'is_creator': is_creator
            })
        except Exception as e:
            # Log error or handle users without profiles gracefully
            print(f"Error processing user {user.username} for explore page: {e}")
            pass
    
    return render(request, 'explore.html', {'user_profiles': user_profiles})
