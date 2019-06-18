from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_http_methods, require_GET
from .models import Post
from .forms import PostForm

# Create your views here.


@require_GET
def index(request):
    posts = Post.objects.order_by('-pk')
    context = {'posts': posts}
    return render(request, 'pages/index.html', context)


@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect('pages:detail', post.pk)
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'pages/form.html', context)


# boards/3/
@require_GET
def detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    context = {'post': post}
    return render(request, 'pages/detail.html', context)


# POST boards/3/delete/
@require_POST
def delete(request, post_pk):
    # 특정 보드를 불러와서 삭제한다.
    post = get_object_or_404(Post, pk=post_pk)
    post.delete()
    return redirect('pages:index')


@require_http_methods(['GET', 'POST'])
def update(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    #  POST boards/3/update/
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('pages:detail', post.pk)
    #  GET pages/3/update/
    else:
        form = PostForm(instance=post)  # board 데이터 할당
    context = {
        'form': form,
        'post_pk': post_pk,
    }
    return render(request, 'pages/form.html', context)