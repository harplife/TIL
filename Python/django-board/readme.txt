pip install django-extensions
python manage.py shell_plus
# ���� �����Ҷ� �ʿ��� import������ �ҷ��� �ش�

board = Board.objects.get(id=11)
# ���� ���忡 ���� �ڸ�Ʈ �ޱ�
comment = Comment()
comment.content = 'first comment'
comment.board = board
# comment.board_id = board.id �ε� ���尡��
comment.save()
comment.board # board ���
# board�� id�� ��µȴ�
comment.board.id
# board�� content ���
comment.board.content

# board�� �޸� �ڸ�Ʈ Ȯ��
board = Board.objects.get(id=3)
board.comment_set.all()

# �ν��Ͻ� �����ϸ鼭 �ڸ�Ʈ �ޱ�
comment = Comment(board_id=board.id, content='another comment')
comment.save()
