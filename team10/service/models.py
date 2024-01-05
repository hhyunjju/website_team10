from django.db import models
from django.conf import settings

# Create your models here.
class CameraImage(models.Model):
    image = models.ImageField(upload_to='camera/')
    timestamp = models.DateTimeField(auto_now_add=True)

class PostureDetection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=-1)
    timeymd = models.CharField(max_length=10, null=True)
    timehms = models.CharField(max_length=8, null=True)
    posturetype = models.IntegerField(default=-1)
