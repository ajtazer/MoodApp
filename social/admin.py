from django.contrib import admin
from social.models import SocialProfile, Post, Comment

admin.site.register(SocialProfile)
admin.site.register(Post)
admin.site.register(Comment)
