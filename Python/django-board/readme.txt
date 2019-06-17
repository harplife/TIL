### 코멘트 기능 구현 ###

models.py, admin.py에 코드 추가
makemigrations, migrate 다 해주기

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

# Boards 모델에 image필드 추가!
1. pip install Pillow
2. models.py - Board - 이미지 필드 추가
3. python manage.py makemigrations
4. python manage.py migrate
5. views.py - new - get image
6. new.html - input type="file" name="image" accept="image/*"
7. new.html - form 태그에 enctype="multipart/form-data" 추가
8. settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
9. 프로젝트 폴더 - media 폴더 생성
10. crud - urls.py - urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 추가

# 이미지 프로세싱 모듈
pip install pilkit
pip install django-imagekit
# models.py 에서 image를 수정해주자~ 임포트도 잘 해주고~
image = ProcessedImageField(
    upload_to='boards/images', # 저장위치 (media 이후의 경로)
    processors=[Thumbnail(200, 300)],
    format='JPEG',
    options={'quality': 90},
)


### pages ###
django form 기능들을 활용한다!
