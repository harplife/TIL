# Django 설치 및 활용

1. Django 설치

   ```bash
   $ pip install django
   ```

2. Django 프로젝트 생성

   ```bash
   $ django-admin startproject intro .
   ```

3. Django 서버 연동 테스트 (로케트 뜨면 제대로 깔린거임)

   ```bash
   $ python manage.py runserver
   ```

4. app 생성 (pages 라는 앱 생성)

   ```bash
   $ python manage.py startapp pages
   ```

5. 생성된 app 등록

   - intro 폴더 > settings.py > installed_apps > pages.apps.PagesConfig 추가

6. Django 설정 (언어, 시간)

   - LANGUAGE_CODE = 'ko-kr'
   - TIME_ZONE = 'Asia/Seoul'

7. 경로 추가

   - intro 폴더 > urls.py

     - from pages import views 추가
     - urlpatterns > path('index/', views.index) 추가

   - pages 폴더 > views.py

     ```python
     def index(request):
         return render(request, 'index.html')
     ```

8. index.html 파일 생성

   - pages 폴더 > templates 폴더 생성 > index.html 생성

9. 테스트

   ```bash
   $ python manage.py runserver
   ```

   - http://127.0.0.1:8000/index 접속

10. 변수 보내기

    - pages 폴더 > views.py > index 함수
      
      - 변수 생성
      - render() 수정
      
      ```python
      def index(request):
          greet = 'Hello World!'
          return render(request, 'index.html', {'hello': greet})
      ```
      
      - 주의: key, value값 이름이 중복되면 안 된다.
      
    - templates 폴더 > index.html > {{ hello }} 추가 (jinja 코딩)

11. 변수 받기

    - intro 폴더 > urls.py > urlpatterns > path('index/', views.index) 수정

      - 주의: 경로는 언제나 / 로 끝난다.
      
      ```python
      path('index/<str:name>/', views.index)
      ```
      
    - pages > views.py > index 함수 > name 받게 설정
    
      ```python
      def index(request, name):
          return render(request, 'index.html', {'name': name})
      ```
    
      