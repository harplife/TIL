from django.shortcuts import render, redirect
from boards.models import Board

# Create your views here.


def index(request):
    boards = Board.objects.all()
    context = {'boards': boards}
    return render(request, 'boards/index.html', context)


# 게시글 작성하고 올리는 페이지
def new(request):
    return render(request, 'boards/new.html')


"""
new.html에서 작성한 게시글을 POST 방식으로 받고,
데이터베이스에 저장해준다.
저장 후 index페이지로 redirect
"""
def create(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    board = Board()
    board.title = title
    board.content = content
    board.save()
    # print(Board.objects.all())
    # return render(request, 'boards/create.html', context)
    return redirect(f'/boards/{board.id}')


# 특정 게시글 하나만 가지고 온다
def detail(request, id):
    board = Board.objects.get(id=id)
    context = {'board': board}
    return render(request, 'boards/detail.html', context)


# 특정 게시글 하나를 지운다
def delete(request, id):
    board = Board.objects.get(id=id)
    board.delete()
    return redirect('/boards/')
