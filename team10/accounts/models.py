from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=50)
    nickname = models.CharField(max_length=30, blank = True, default = '')
    email = models.EmailField()
    
    def save(self, *args, **kwargs):
        #닉네임이 비어있으면 사용자의 이름으로 채운다
        if not self.nickname:
            self.nickname = self.user.username
        super().save(*args, **kwargs)

