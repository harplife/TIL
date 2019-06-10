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

   - intro 폴더 > settings.py > installed_apps

     ```python
     INSTALLED_APPS = [
         # new apps here
         'pages.apps.PagesConfig', # <-- 추가 부분
     
         # django default apps
         'django.contrib.admin',
         'django.contrib.auth',
         'django.contrib.contenttypes',
         'django.contrib.sessions',
         'django.contrib.messages',
         'django.contrib.staticfiles',
     ]
     ```

6. Django 설정 (언어, 시간)

   - intro 폴더 > settings.py > 수정

     ```python
     LANGUAGE_CODE = 'ko-kr'
     TIME_ZONE = 'Asia/Seoul'
     ```

7. 앱 경로 추가

   - intro 폴더 > urls.py

     ```python
     from django.contrib import admin
     from django.urls import path, include # <-- 추가
     
     urlpatterns = [
         path('pages/', include('pages.urls')), # <-- 추가
         path('admin/', admin.site.urls),
     ]
     ```

   - pages 폴더 > urls.py 생성

     ```python
     from django.urls import path
     from . import views
     
     urlpatterns = [
         path('index/', views.index),
     ]
     ```

   - pages 폴더 > views.py

     ```python
     def index(request):
         return render(request, 'pages/index.html')
     ```

9. index.html 파일 생성

   - pages 폴더 > templates 폴더 생성 > pages 폴더 생성 > index.html 생성

10. 테스트

   ```bash
   $ python manage.py runserver
   ```

   - http://127.0.0.1:8000/pages/index 접속

11. 변수 보내기

    - pages 폴더 > views.py > index 함수
      
      - 변수 생성
      - render() 수정
      
      ```python
      def index(request):
          greet = 'Hello World!'
          context = {'greet': greet}
          return render(request, 'pages/index.html', context)
      ```
      
    - templates 폴더 > index.html > {{ greet }} 추가 (jinja 코딩)

12. 변수 받기

    - pages 폴더 > urls.py > urlpatterns > `path('index/', views.index)` 수정

      - 주의: 경로는 언제나 / 로 끝난다.
      
      ```python
      path('index/<str:name>/', views.index)
      ```
      
    - pages > views.py > index 함수 > name 받게 설정

      ```python
      def index(request, name):
          greet = 'Hello, '
          context = {'greet': greet}
          context['name'] = name
          return render(request, 'pages/index.html', context)
      ```
      
      - index.html 에 {{ greet }}{{ name }} 추가
      - http://127.0.0.1:8000/pages/index/yourname 으로 접속하면 "Hello, yourname"이 출력된다.

13. ## Layout 설정 (Base라고도 불리는듯..)

    - Layout 설정은 웹사이트에 사용되는 모든 페이지의 공통점, 즉, html 태그, head 태그와 그 내용물 등을 하나의 html 파일에 모아서 자동으로 반복되게 만듦으로서 중복되는 코딩을 줄이는 방식이다.

    - pages > templates > layout.html 생성

      ```html
      <!DOCTYPE html>
      <html lang="en">
      <head>
          <meta charset="UTF-8">
          <title>Pages</title>
      </head>
      <body>
      
      <main>
          <header>
              <h1>Pages</h1>
          </header>
      
          <section>
              <!-- 앞으로 다른 페이지들은 이 content라는 block안에 호출이 된다. -->
              {% block content %} 
              {% endblock %}
              <!-- 참고로 content는 걍 이름이니 다르게 지정해줘도 된다. -->
          </section>
      
          <footer>
              <p>Copyright 2019</p>
          </footer>
      </main>
      
      </body>
      </html>
      ```

    - pages > templates > index.html 수정

      ```html
      {% extends 'pages/layout.html' %} <!-- layout을 상속받는다! -->
      
      {% block content %}
          <h1>THIS IS PAGES INDEX PAGE</h1>
      {% endblock %}
      ```

    - http://127.0.0.1:8000/pages/index 로 접속하면 layout.html을 상속받은 index.html이 표출된다.

14. ## [Django 템플릿 언어 활용법](<https://docs.djangoproject.com/en/2.2/ref/templates/language/>)

    - 주로 .html 파일들을 템플릿이라 부른다. 밑에 사용되는 코드들은 모두 html 안에서 적용되는 코드다.

    - for문

      ```html
      {% for menu in menus %}
      	<p> {{ menu }} </p>
      {% endfor %}
      ```

    - if문

      ```html
      {% if menu == '짜장면' %}
      	<p> 짜장면은 고추가루랑! </p>
      {% endif %}
      ```

    - {{ forloop.counter }}

      - for문 안에 넣는다. for문이 돌아가는 순서대로 번호가 나온다.
      - 1 부터 시작 (counter0 하면 0 부터)

    - {% empty %}

      - for문 안에 넣는다. for문이 돌아가는 literal이 비어있으면 empty 밑에 있는 부분이 실행된다.

    - Lorem Ipsum: Placeholder 텍스트

      ```html
      {% lorem %} <!-- 빈 공간을 채우는 텍스트 -->
      {% lorem 3 w %} <!-- 3 단어 -->
      {% lorem 4 w random %} <!-- 4 단어, random -->
      {% lorem p %} <!-- 1 단락 -->
      ```

    - 문자열 처리

      ```html
      {{ 'ABC'|lower }} <!-- 소문자로 변환 -->
      {{ 'life is short'|title }} <!-- 첫문자 대문자 -->
      {{ 'abc'|length }} <!-- 글자 길이 (3) -->
      {{ sentence|truncatewords:3 }} <!-- 3글자 제한 -->
      {{ sentence|truncatechars:3 }} <!-- 2문자 제한 -->
      ```

    - 날짜/시간

      - views.py에서 직접 datetime 객체를 보내서 html에서 변수로 받고 표출할 수 있다 (settings.py에 설정된 언어로 표출된다).

        ```html
        {{ datetime객체 }}
        {{ datetime객체|date:"SHORT_DATE_FORMAT" }} <!-- 포매팅 적용 -->
        ```
      
      - Template 고유 기능 사용
      
        ```html
        {% now "DATETIME_FORMAT" %} <!-- 객체를 따로 받을 필요 없이 시간을 표출할 수 있다 -->
        {% now "SHORT_DATETIME_FORMAT" %} <!-- 시간을 짧게 표출 -->
        {% now "DATE_FORMAT" %} <!-- 날짜만 표출 -->
        {% now "SHORT_DATE_FORMAT" %} <!-- 날짜만 짧게 표출 -->
        {% now "Y년 m월 d일 (D) h:i" %} <!-- 2019년 6월 4일 (화요일) 11:25 -->
        
        {% now "Y" as current_yr %} <!-- 년도를 변수로 받아서 사용 -->
        	<p> Copyright {{ current_yr }} </p>
        ```

    - hyperlink

      ```html
      {{ 'google.com'|urlize }}
      ```

15. ## Throw & Catch (Form에서 값 보내기)

    - pages > urls.py > urlpatterns > throw 추가, catch 추가

    - pages > views.py > throw 함수 추가, catch 함수 추가
      - throw 함수

         ```python
         def throw(request):
             return render(request, 'pages/throw.html')
         ```
         
      - catch 함수

         ```python
         def catch(request):
             message = request.GET.get('message')
             context = {'message': message}
             return render(request, 'pages/catch.html', context)
         ```
      
    - templates > pages > throw.html, catch.html 추가

       - throw.html
       
          ```html
          <form action="/pages/catch/"> <!-- route ends with / -->
          	던질거: <input type="text" name="message">
          	<input type="submit">
          </form>
          ```
       
          - 주의: form 태그 action부분에 경로는 / 로 시작하고 /로 끝나야 된다.
       
       - catch.html
       
          ```html
          {% if message %}
          	<h2>Received: "{{ message }}"</h2>
          {% endif %}
          ```
       
    - http://127.0.0.1:8000/pages/throw 로 접속하여 변수 보내고 받기 해본다

16. ## STATIC 파일 설정 (CSS)

    - pages > urls.py > urlpatterns > css_example 추가

    - pages > views.py > css_example 추가

    - pages > templates > pages > css_example.html 생성

      ```html
      <!DOCTYPE html>
      {% load static %} <!-- static 폴더 로딩 -->
      <html lang="en">
      <head>
          <meta charset="UTF-8">
          <title>Title</title>
          <!-- css 파일 연결 -->
          <link rel="stylesheet" href="{% static 'pages/stylesheets/style.css' %}">
      </head>
      <body>
          <h1>STATIC EXAMPLE</h1>
      </body>
      </html>
      ```

    - pages > static 폴더 생성 > pages 폴더 생성 > stylesheets 폴더 생성 > style.css 생성

      ```css
      /* 아주 간단히~ */
      h1 {
        color: green;
      }
      ```
      
    - 참고:

      - static/pages/images 폴더를 생성하여 이미지들을 위에 같이 가져와 사용할 수 있다.
      - layout.html에 적용하면 상속되는 다른 페이지들도 동일한 css가 적용된다.

17. 

# 활용 예제

1. ASCII Art API 활용 [(링크)](<http://artii.herokuapp.com/>)

   - pages > urls.py > urlpatterns > artii 추가, result 추가

     ```python
     urlpatterns = [
         path('artii/', views.artii),
         path('result/', views.result),
     ]
     ```

   - pages > views.py > artii 추가, result 추가

     ```python
     def artii(request):
         return render(request, 'pages/artii.html')
     
     
     def result(request):
         font_url = "http://artii.herokuapp.com/fonts_list"
         fonts = requests.get(font_url).text
         fonts = fonts.split()
         word = request.GET.get('word')
     
         context = {}
         results = []
         for x in range(5):
             font = random.choice(fonts)
             artii_url = f"http://artii.herokuapp.com/make?text={word}&font={font}"
             result = requests.get(artii_url).text
             results.append([artii_url, result])
             context['results'] = results
     
         return render(request, 'pages/result.html', context)
     ```

     - 주의: Django의 request와 requests 패키지 혼동하지 말 것..
     - import random, requests

   - templates > pages > artii.html, result.html 추가

     - artii.html (폼 추가)

       ```html
       <form action="/pages/result/">
           영단어를 입력해주세요 :
           <input type="text" name="word">
           <input type="submit">
       </form>
       ```

     - result.html (결과값 받기)

       ```html
       {% for x in results %}
       	<h2>{{ x.0 }}</h2>
       	<pre>{{ x.1 }}</pre>
       	<hr />
       {% endfor %}
       ```

2. 