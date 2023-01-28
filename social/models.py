from django.db import models
from django.utils import timezone

class Profile(models.Model):
    # photo=models.ImageField()
    username = models.CharField(max_length=20)
    email=models.EmailField(max_length=100)
    bio = models.TextField()
    creation = models.DateTimeField('Account Created', default=timezone.now)

    def __str__(self):
        return self.username