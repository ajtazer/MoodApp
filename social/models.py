from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    creation = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='dp', blank=True)
    username = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True, null=True)
    is_google_auth = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

