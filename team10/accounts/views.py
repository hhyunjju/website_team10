from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

def login_view(request):
    if request.method == 'POST':
        # POST 요청이 들어오면 로그인 처리를 시도합니다.
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # 로그인 성공 후 리다이렉트 또는 다른 작업을 수행합니다.
            return redirect('dashboard')  # 'dashboard'는 로그인 후 이동할 페이지 이름
        else:
            # 로그인 실패 시 오류 메시지 등을 처리합니다.
            error_message = '로그인 실패: 올바른 사용자 이름과 비밀번호를 입력하세요.'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        # GET 요청 시 로그인 페이지를 보여줍니다.
        return render(request, 'accounts/login.html')

def register_view(request):
    if request.method == 'POST':
        # POST 요청이 들어오면 회원가입 처리를 시도합니다.
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 회원가입 성공 후 리다이렉트 또는 다른 작업을 수행합니다.
            return redirect('login')  # 'login'은 회원가입 후 이동할 페이지 이름
    else:
        # GET 요청 시 회원가입 페이지를 보여줍니다.
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})





# 임시로 만들었습니다
def idFind(request):
    return render(request, 'accounts/idFind.html')
def passwordRecovery(request):
    return render(request, 'accounts/passwordRecovery.html')