from django.http import HttpResponse

from .models import Post
from django.http import Http404
from .models import User

from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect

from .forms import PostForm
from .forms import PostModelForm

# Create your views here.
# 전체 목록 보기
def list(request):
        # 맨 처음 페이지를 요청해서 받아왔을 때
    post_list = Post.objects.all() 
    # return HttpResponse(post_all)
        # 이후 검색창에 검색어를 넣고 submit 했을 때
    search_key = request.GET.get('keyword')
    if search_key :
            # 이전에 입력했던 데이터는 search_key에 남아있다. 
            # 이전 입력 데이터도 쓰고자 한다면 context로 넘기면 된다.
        post_list = Post.objects.filter(title__contains=search_key)
    return render(request, 'brd/list.html', {'post_all':post_list, 'q':search_key})

# 상세 보기
def detail(request, no):
    post = get_object_or_404(Post, id=no)
    comment = post.comments.all()
    return render(request, 'brd/post_detail.html', {'post':post, 'comment_all':comment,})

# form 기반 데이터 추가 작업
def post_create(request):
    if request.method == 'POST':
        form = PostModelForm(request.POST)
        if form.is_valid():
            # DB에 추가
            # cleaned_data : dictionary
            # post = Post.objects.create(**form.cleaned_data)
            post = form.save(commit=False)
            post.ip = request.META['REMOTE_ADDR']
            post.save()
            return redirect(post)
    else:
        form = PostModelForm()
    return render(request, 'brd/post_form.html', {'form':form,})

# form 기반 데이터 수정 작업
def post_update(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        # post로 입력 받았을 때
        # 0. 입력받은 데이터 바인딩
        form = PostModelForm(request.POST, instance=post)
        # 1. 유효성 검사를 한다. 입력받은 데이터가 올바르게 입력 됐는지
        if form.is_valid():
            # 2. 데이터를 처리한다.
            form.save()
            return redirect('brd:notice_board')
    else:
        form = PostModelForm(instance=post)
    return render(request, 'brd/post_update.html', {'form':form,})

# 데이터 삭제 작업
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        post.delete()
        return redirect('brd:notice_board')
    else:
        return render(request, 'brd/post_delete.html', {'post':post})

def faq_view(request):
    # FAQ 페이지에 필요한 데이터를 처리
    # 예시: context = {'faq_data': faq_data}

    # FAQ 페이지의 템플릿을 렌더링하여 반환
    return render(request, 'brd/faq.html')