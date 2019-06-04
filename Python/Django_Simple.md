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
          context = {'greet': greet}
          return render(request, 'index.html', context)
      ```
      
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
       

14. TBC