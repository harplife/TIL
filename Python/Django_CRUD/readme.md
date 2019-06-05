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

LANGUAGE_CODE = 'ko-kr' # 이 부분 수정
TIME_ZONE = 'Asia/Seoul' # 이 부분 수정
USE_TZ = False # 이 부분 수정
```

## 모델 생성 (DB 설계도)

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

### 모델 수정 적용

```bash
$ python manage.py makemigrations
```

- 제대로 적용될 시에 이런 결과가 나온다

  ```
  Migrations for 'boards':
    boards\migrations\0001_initial.py
      - Create model Board
  ```

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



