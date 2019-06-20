from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_http_methods, require_GET
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

# Create your views here.


@require_GET
def index(request):
    posts = Post.objects.order_by('-pk')
    context = {'posts': posts}
    return render(request, 'pages/index.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('pages:detail', post.pk)
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'pages/form.html', context)


# boards/3/
@require_GET
def detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comments = post.comment_set.order_by('-pk').all()
    comment_form = CommentForm()
    person = get_object_or_404(get_user_model(), pk=post.user_id)
    context = {
        'post': post,
        'comment_form': comment_form,
        'comments': comments,
        'person': person,
    }
    return render(request, 'pages/detail.html', context)


# POST boards/3/delete/
@require_POST
def delete(request, post_pk):
    # 특정 보드를 불러와서 삭제한다.
    post = get_object_or_404(Post, pk=post_pk)
    if request.user != post.user:
        return redirect('pages:detail', post_pk)
    post.delete()
    return redirect('pages:index')


@login_required
@require_http_methods(['GET', 'POST'])
def update(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.user != post.user:
        return redirect('pages:detail', post_pk)
    #  POST boards/3/update/
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)  # 바로 저장을 하지 않고,
            post.user = request.user  # 세션에 사용자 ID값을 갖고와서,
            post.save()  # db에 같이 저장
            return redirect('pages:detail', post.pk)
    #  GET pages/3/update/
    else:
        form = PostForm(instance=post)  # board 데이터 할당
    context = {
        'form': form,
        'post_pk': post_pk,
    }
    return render(request, 'pages/form.html', context)


@require_POST
def make_comment(request, post_pk):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    # 댓글 작성 로직
    form = CommentForm(request.POST)
    if form.is_valid():
        comment_form = form.save(commit=False)
        comment_form.user = request.user  # == comment_form.user_id = request.user.id
        comment_form.post_id = post_pk
        comment_form.save()
    return redirect('pages:detail', post_pk)


@require_POST
def delete_comment(request, post_pk, comment_pk):
    # 댓글 삭제 로직
    comment = get_object_or_404(Comment, pk=comment_pk)
    if comment.user == request.user:
        comment.delete()
    return redirect('pages:detail', post_pk)


@login_required
def like(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    user = request.user

    if user in post.like_users.all():
        post.like_users.remove(user)
    else:
        post.like_users.add(user)

    return redirect('pages:detail', post_pk)


@login_required
def follow(request, post_pk, user_pk):
    user = request.user
    person = get_object_or_404(get_user_model(), pk=user_pk)

    if user != person:
        if user in person.followers.all():
            person.followers.remove(user)
        else:
            person.followers.add(user)
    return redirect('pages:detail', post_pk)