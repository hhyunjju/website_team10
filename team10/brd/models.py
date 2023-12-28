from django.db import models
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=250) # 길이 제한 파라미터 필수
    body = models.TextField() # 길이 제한 없음
    ip = models.GenericIPAddressField(null=True) # ip값 받아오며 동시에 유효성 검사도 함.
    photo = models.ImageField(upload_to='brd_image/%Y-%m-%d/',null=True, blank=True)
    
    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse("brd:detail", args=[self.id])
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    message = models.TextField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.message
    
    
class User(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return self.name
