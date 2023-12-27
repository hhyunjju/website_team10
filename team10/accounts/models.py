from django.db import models
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.signals import user_logged_in

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

class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    
    #중복 로그인 방지
    def block_duplicate_login(sender, request, user, **kwargs):
        login_user_list = UserSession.objects.filter(user=user)
        for user_session in login_user_list:
            session = SessionStore(user_session.session_key)
            session.delete()
        session_key = request.session.session_key
        UserSession.objects.create(user=user, session_key = session_key)
    user_logged_in.connect(block_duplicate_login)