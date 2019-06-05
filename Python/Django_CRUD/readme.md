# Django - 데이터베이스 연동

## 기본 셋업

### 터미널 작업

```bash
$ pip install django
$ django-admin startproject crud .
$ python manage.py startapp boards
```

### crud > settings.py  (수정 부분)

```python
INSTALLED_APPS = [
    # Local apps
    'boards.apps.BoardsConfig',  # 이 부분 추가

    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

DATABASES = {
    'default': {
        # 기본적으로 sqlite3를 사용할 것임
        'ENGINE': 'django.db.backends.sqlite3',
        # 'ENGINE': 'django.db.backends.postgresql',
        # 'ENGINE': 'django.db.backends.mysql',
        # 'ENGINE': 'django.db.backends.oracle',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'ko-kr' # 이 부분 수정
TIME_ZONE = 'Asia/Seoul' # 이 부분 수정
USE_TZ = False # 이 부분 수정
```

## Board 모델 생성 (DB 설계도)

### boards > models.py

```python
class Board(models.Model):
    # id는 기본적으로 처음 테이블 생성시 자동으로 만들어진다.
    # id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=16)
    content = models.TextField()
    # 데이터가 생성이 될 떄 auto_now_add
    created_at = models.DateTimeField(auto_now_add=True)
    # 데이터가 수정이 될 떄 auto_now
    updated_at = models.DateTimeField(auto_now=True)
```

### Board 모델을 프로젝트에 적용

```bash
$ python manage.py makemigrations
```

- 제대로 적용될 시에 이런 결과가 나온다

  ```
  Migrations for 'boards':
    boards\migrations\0001_initial.py
      - Create model Board
  ```

### Board 테이블 DB에 생성

```bash
$ python manage.py migrate
```

- 제대로 적용될 시에 이런 결과가 나온다

  ```
  Operations to perform:
    Apply all migrations: admin, auth, boards, contenttypes, sessions
  Running migrations:
    Applying contenttypes.0001_initial... OK
    Applying auth.0001_initial... OK
    Applying admin.0001_initial... OK
    Applying admin.0002_logentry_remove_auto_add... OK
    Applying admin.0003_logentry_add_action_flag_choices... OK
    Applying contenttypes.0002_remove_content_type_name... OK
    Applying auth.0002_alter_permission_name_max_length... OK
    Applying auth.0003_alter_user_email_max_length... OK
    Applying auth.0004_alter_user_username_opts... OK
    Applying auth.0005_alter_user_last_login_null... OK
    Applying auth.0006_require_contenttypes_0002... OK
    Applying auth.0007_alter_validators_add_error_messages... OK
    Applying auth.0008_alter_user_username_max_length... OK
    Applying auth.0009_alter_user_last_name_max_length... OK
    Applying auth.0010_alter_group_name_max_length... OK
    Applying auth.0011_update_proxy_permissions... OK
    Applying boards.0001_initial... OK
    Applying sessions.0001_initial... OK
  ```

## Board 테이블에 내용 추가

```bash
$ python manage.py shell
>>> from boards.models import Board
```

### 첫 번째 방법

```python
>>> Board.objects.all() # SELECT * FROM boards
<QuerySet []>
>>> board = Board() # 테이블 인스턴스 생성
>>> board
<Board: Board object (None)>
>>> board.title = 'new Board' # title 추가
>>> board.content = 'Hello World' # content 추가
>>> board.title
'new Board'
>>> board.content
'Hello World'
>>> board.save() # 저장
>>> board
<Board: Board object (1)>
>>> Board.objects.all()
<QuerySet [<Board: Board object (1)>]>
```

### 두 번째 방법

```python
>>> board = Board(title="Second Board", content="Hello Django")
>>> board.save()
>>> board
<Board: Board object (2)>
>>> Board.objects.all()
<QuerySet [<Board: Board object (1)>, <Board: Board object (2)>]>
```

### 세 번째 방법

```python
>>> Board.objects.create(title="Third board", content="Hello YOU")
<Board: Board object (3)>
>>> Board.objects.all()
<QuerySet [<Board: Board object (1)>, <Board: Board object (2)>, <Board: Board object (3)>]>
```

## Board 테이블 출력

### boards > models.py 수정

```python
class Board(models.Model):
	# ..
    # 밑에 부분 추가
    def __str__(self):
        return f'{self.id}번째 글 - {self.title}'
```

### query

```bash
$ python manage.py shell
>>> from boards.models import Board
>>> Board.objects.all()
<QuerySet [<Board: 1번째 글 - new Board>, <Board: 2번째 글 - Second Board>, <Board: 3번째 글 - Third board>]>
```

## 관리자 계정으로 Board 테이블 확인

### boards > admin.py 수정

```python
from django.contrib import admin
from .models import Board

# Register your models here.
admin.site.register(Board)
```

### 관리자 계정 생성

```bash
$ python manage.py createsuperuser
사용자 이름 (leave blank to use 'student'): admin
이메일 주소: admin@email.com
Password:
Password (again):
비밀번호가 너무 일상적인 단어입니다.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.
```

### 관리자 페이지로 접속

```bash
$ python manage.py runserver
```

- <http://127.0.0.1:8000/admin> 로 접속 (admin/password)

  - ![django_capture](https://user-images.githubusercontent.com/44990492/58934444-78599080-87a5-11e9-8cab-ac835d38f887.PNG)

- Boards 클릭

  - ![django_capture_2](https://user-images.githubusercontent.com/44990492/58934525-a8089880-87a5-11e9-9b9d-09cbd2a18c40.PNG)


## Django 데이터베이스 활용 이해

```python
from boards.models import Board

# SELECT * FROM boards;
Board.objects.all()

# SELECT * FROM boards WHERE title='new Board';
Board.objects.filter(title='new Board')

# SELECT * FROM boards WHERE title='new Board' LIMIT 1;
Board.objects.filter(title='new Board').first()

# SELECT * FROM boards WHERE id=1;
Board.objects.filter(id=1).first()
Board.objects.get(id=1) # get()은 primary key에만.

# SELECT * FROM boards ORDER BY title ASC;
Board.objects.order_by('title').all()
# SELECT * FROM boards ORDER BY title DESC;
Board.objects.order_by('-title').all()

# QuerySet은 리스트처럼 인덱싱, 슬라이싱 가능!
Board.objects.all()[1] # 2번째거 갖고옴
Board.objects.all()[:2] # 1,2번꺼 갖고옴
```



