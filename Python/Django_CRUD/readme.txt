1. 장고 설치
pip install django
2. 장고 프로젝트 생성
django-admin startproject intro .
3. 장고 서버 연동
python manage.py runserver
4. app 생성
python manage.py startapp pages
5. 생성된 app 등록 (intro > settings.py > installed_apps > app이름.apps.PagesConfig)
6. django 웹 설정 (settings.py) : 언어, 시간
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
7. 경로 추가 (index라는 경로 생성)
intro > urls.py > from 앱 import views > urlpatterns > path('index/', views.index) 추가
앱 > views.py > 밑에 처럼 추가;
def index(request):
    return render(request, 'index.html')
8. index.html 파일 생성
앱 > templates 폴더 생성 > index.html 생성


python manage.py makemigrations