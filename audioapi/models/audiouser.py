from django.db import models
from django.contrib.auth.models import User

class AudioUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=150, blank=False)
    image = models.CharField(max_length=200, blank=False)
    