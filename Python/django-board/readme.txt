pip install django-extensions
python manage.py shell_plus
# 모델을 구성할때 필요한 import문들을 불러와 준다

board = Board.objects.get(id=11)
# 지정 보드에 대한 코멘트 달기
comment = Comment()
comment.content = 'first comment'
comment.board = board
# comment.board_id = board.id 로도 저장가능
comment.save()
comment.board # board 출력
# board의 id가 출력된다
comment.board.id
# board의 content 출력
comment.board.content

# board에 달린 코멘트 확인
board = Board.objects.get(id=3)
board.comment_set.all()

# 인스턴스 생성하면서 코멘트 달기
comment = Comment(board_id=board.id, content='another comment')
comment.save()
