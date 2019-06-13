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

# movies 앱 생성
python manage.py startapp movies

# models.py 수정
class movie(models.Model):
    title = models.CharField(max_length=100)
    title_origin = models.CharField(max_length=100)
    vote_count = models.IntegerField()
    open_date = models.CharField(max_length=30)
    genre = models.CharField(max_length=20)
    score = models.FloatField()
    poster_url = models.TextField()
    description = models.TextField()

# 모델 적용
python manage.py makemigrations
python manage.py migrate

# json 파일을 fixtures 라는 폴더안에 넣고,
# 데이터베이스에 입력 (밑에 명령어)
python manage.py loaddata movies.json


