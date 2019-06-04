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

7. 경로 추가

   - intro 폴더 > urls.py

     ```python
     from pages import views # <-- 추가
     
     urlpatterns = [
         path('index/', views.index), # <-- 추가
         path('admin/', admin.site.urls),
     ]
     ```

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
          context = {'greet': greet}
          return render(request, 'index.html', context)
      ```
      
    - templates 폴더 > index.html > {{ greet }} 추가 (jinja 코딩)

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

12. [Django Template Lanauge](<https://docs.djangoproject.com/en/2.2/ref/templates/language/>)

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

13. Throw & Catch (Form에서 값 보내기)

    - intro > urls.py > urlpatterns > throw 추가, catch 추가

    - pages > views.py > throw 함수 추가, catch 함수 추가
      - catch 함수

         ```python
         def catch(request):
             message = request.GET.get('message')
             context = {'message': message}
             return render(request, 'catch.html', context)
         ```

    - templates > throw.html, catch.html 추가

       - throw.html
       
          ```html
          <form action="/catch/"> <!-- route ends with / -->
          	던질거: <input type="text" name="message">
          	<input type="submit">
          </form>
          ```
       
       - catch.html
       
          ```html
          {% if message %}
          	<h2>Received: "{{ message }}"</h2>
          {% endif %}
          ```
       
14. STATIC 파일 설정 (CSS)

    - intro > urls.py > urlpatterns > css_example 추가

    - pages > views.py > css_example 추가

    - pages > templates > css_example.html 생성

      ```html
      <!DOCTYPE html>
      {% load static %} <!-- static 폴더 로딩 -->
      <html lang="en">
      <head>
          <meta charset="UTF-8">
          <title>Title</title>
          <!-- css 파일 연결 -->
          <link rel="stylesheet" href="{% static 'stylesheets/style.css' %}">
      </head>
      <body>
          <h1>STATIC EXAMPLE</h1>
      </body>
      </html>
      ```

    - pages > static 폴더 생성 > stylesheets 폴더 생성 > style.css 생성

      ```css
      /* 아주 간단히~ */
      h1 {
        color: green;
      }
      ```

15. 패키징

    - Django는 한 앱만 사용하는게 아니라 여러 앱을 생성하고 사용할 수 있다.

    - 앱 하나 추가 생성 (utilities 앱)

      ```bash
      $ python manage.py startapp utilities
      ```

    - intro > settings.py > INSTALLED_APPS > 'utilities.apps.UtilitiesConfig' 추가

    - urls.py 정리

      - intro > urls.py > urlpatterns > pages.views 사용하는 path CUT
        - from django.urls import include 추가
        - urlpatterns > path('pages/', include('pages.urls')) 추가
        - urlpatterns > path('utilities/', include('utilities.urls')) 추가
      - pages > urls.py 생성 > urlpatterns > path PASTE > from . import views 추가

    - pages > templates > pages 폴더 생성 > template들 모두 옮기기

      - utilities > templates> utilities 폴더 생성 > template은 여기에 생성

    - 각 template의 form태그 action 값들 수정

      - 예: action='/index/' > action='/pages/index'

    - pages > views.py > 각 함수의 return render 수정

      - 예: return render(request, 'index.html') > return render(request, 'pages/index.html')

    - 참고: 여러 앱을 사용할 것을 예상할 시에 미리 templates, urls.py, views.py 사용방식을 패키징 방식으로 적용할 것..

16. 

## 활용 예제

1. ASCII Art API 활용 [(링크)](<http://artii.herokuapp.com/>)

   - intro > urls.py > urlpatterns > artii 추가, result 추가

     ```python
     urlpatterns = [
         path('artii/', views.artii),
         path('result/', views.result),
     ]
     ```

   - pages > views.py > artii 추가, result 추가

     ```python
     def artii(request):
         return render(request, 'artii.html')
     
     
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
     
         return render(request, 'result.html', context)
     ```

     - 주의: Django의 request와 requests 패키지 혼동하지 말 것..
     - import > random, requests

   - templates > artii.html, result.html 추가

     - artii.html (폼 추가)

       ```html
       <form action="/result/">
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