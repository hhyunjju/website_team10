from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile

class SignupForm(UserCreationForm):
    phone_number = forms.CharField()
    address = forms.CharField()
    nickname = forms.CharField(required=False)
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',) #사용자 생성을 위한 폼에만 필드를 추가
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.save()
        
        profile = Profile.objects.create(
            user=user,
            phone_number = self.cleaned_data['phone_number'],
            address = self.cleaned_data['address'],
            nickname = self.cleaned_data['nickname'],
            email=self.cleaned_data['email']
        )
        return user
    
# save 메서드를 오버라이드하여 사용자 객체를 생성한 후에 해당 사용자의 프로필을 생성합니다. 
# 이때, Profile 모델에 user, phone_number, address를 저장합니다.