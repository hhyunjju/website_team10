from django.db import models
from django.conf import settings

# Create your models here.
class CameraImage(models.Model):
    image = models.ImageField(upload_to='camera/')
    timestamp = models.DateTimeField(auto_now_add=True)

class PostureDetection(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timeymd = models.CharField(max_length=10, default='')
    timehms = models.CharField(max_length=8, default='')
    posturetype = models.IntegerField()
