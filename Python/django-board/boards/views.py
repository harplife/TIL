from django.shortcuts import render, redirect, get_object_or_404
from boards.models import Board, Comment
from django.views.decorators.http import require_http_methods, require_GET

# Create your views here.


@require_GET
def index(request):
    boards = Board.objects.all()
    context = {'boards': boards}
    return render(request, 'boards/index.html', context)


# 게시글 작성하고 올리는 페이지
def new(request):
    if request.method == 'GET':
        return render(request, 'boards/new.html')
    elif request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        id = request.POST.get('id')
        if id:
            board = Board.objects.get(id=id)
            board.title = title
            board.content = content
            image = request.FILES.get('image')
            board.image = image
            board.save()
            return redirect('boards:detail', board.id)
        image = request.FILES.get('image')
        board = Board(
            title=title,
            content=content,
            image=image,
        )
        board.save()
        # print(Board.objects.all())
        # return render(request, 'boards/create.html', context)
        return redirect('boards:detail', board.id)


# 특정 게시글 하나만 가지고 온다
def detail(request, board_id):
    # board = Board.objects.get(board_id=board_id)
    board = get_object_or_404(Board, id=board_id)
    comments = board.comment_set.order_by('-id').all()
    context = {
        'board': board,
        'comments': comments,
    }
    return render(request, 'boards/detail.html', context)


# 특정 게시글 하나를 지운다
@require_http_methods(['POST'])
def delete(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    board.delete()
    return redirect('boards:index')


# 게시글 작성하고 올리는 페이지
def edit(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    context = {'board': board}
    return render(request, 'boards/edit.html', context)


def new_comment(request, board_id):
    if request.method == 'GET':
        context = {
            'board_id': board_id
        }
        return render(request, 'boards/new_comment.html', context)
    if request.method == 'POST':
        board = get_object_or_404(Board, id=board_id)
        content = request.POST.get('content')
        comment = Comment(board_id=board.id, content=content)
        comment.save()
        return redirect('boards:detail', board.id)


@require_http_methods(['POST'])
def delete_comment(request, board_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return redirect('boards:detail', board_id)
