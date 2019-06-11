# flask로 게시판 만들면서 배우기!

------

[TOC]

------

## Hello World

> 간단히 "Hello World" 출력하는 페이지 만들기

1. 설치

   - `pip install flask`

2. 코드 작성 - `flaskapp.py` 생성

   ```python
   from flask import Flask
   app = Flask(__name__)
   
   @app.route("/")
   def hello():
   	return "Hello World!"
   ```

3. 실행 - 가상환경 로드된 cmd

   ```bash
   (web_env) C:\> cd 프로젝트경로
   (web_env) C:\프로젝트경로> set FLASK_APP=flaskapp.py
   (web_env) C:\프로젝트경로> flask run
   ```

   http://localhost:5000 에 접속하면 Hello World! 떠야된다.

------

## Templates

> Template은 HTML 파일을 뜻한다.
> 이번엔 간단한 문자열이 아닌 template을 호출하즈아

1. `flaskapp.py` 수정

   ```python
   from flask import Flask, render_template
   app = Flask(__name__)
   
   @app.route("/")
   @app.route("/home") # 참고 1
   def home():
   	return render_template('home.html') # 참고 2
   
   @app.route("/about")
   def about():
   	return render_template('about.html')
   
   if __name__ == '__main__': # 참고 3
   	app.run(debug=True)
   ```

   참고:

   1. `@app.route('주소')`로 경로를 지정할 수 있다.
      예를 들어 `@app.route("/")`는 `localhost:5000/`,
      `@app.route("/home")`는 `localhost:5000/home`로
      접속할 수 있다는 뜻이다.
   2. flask 웹프레임워크를 MVC 패턴으로 이해하자면은
      여기서 render_template()은 View라고 볼 수 있다.
   3. 전에 `flask run`으로 웹서버를 실행하면
      production mode로 실행되기 때문에
      코딩하면 실시간으로 반영되지 않는다.
      위 처럼 코딩하고 `python flaskapp.py`로
      debugging mode로 실행할 수 있다.

2. `templates` 폴더 생성

   - `home.html` 생성 (아주 간단한 html 코드 적용)
   - `about.html` 생성 (아주 간단한 html 코드 적용)

3. 실행!

   - http://localhost:5000/
   - http://localhost:5000/home
   - http://localhost:5000/about

------

## Jinja

> Jinja는 Template 안에서 python 코드를 구현하는 코드다.

1. 기본적으로 Jinja는 Python에서 보내는 변수를 받고 처리하는 용도에 사용된다. `flaskapp.py`에서 변수를 보내게 설정해보자

   ```python
   # posts란 리스트 생성
   posts = [
   	{
   		'author': 'John Smith',
   		'title': 'Blog Post 1',
   		'content': 'First post content',
   		'date_posted': 'April 20, 2018'
   	},
   	{
   		'author': 'Jane Doe',
   		'title': 'Blog Post 2',
   		'content': 'Second post content',
   		'date_posted': 'April 1, 2018'
   	}
   ]
   
   @app.route("/")
   @app.route("/home")
   def home():
       # posts란 이름으로 posts 배열을 보낸다
   	return render_template('home.html', posts=posts)
   
   
   @app.route("/about")
   def about():
       # title이란 이름으로 'About'문자열 보낸다
   	return render_template('about.html', title='About')
   ```

2. `home.html`에서 변수받게 설정

   ```html
   <!DOCTYPE html>
   <html>
   <head>
       <!-- 참고 1 -->
   	{% if title %}
   		<title>Flask Blog - {{ title }}</title>
   	{% else %}
   		<title>Flask Blog</title>
   	{% endif %}
   </head>
   <body>
   	<!-- 참고 2 -->
   	{% for post in posts %}
   		<h1>{{ post.title }}</h1>
   		<p>By {{ post.author }} on {{ post.date_posted }}</p>
   		<p>{{ post.content }}</p>
   	{% endfor %}
   </body>
   </html>
   ```

   참고:

   1. Jinja 코드로 if-else문을 구현한다.
      - `{%  %}`는 기능을 구현하고,
      - `{{  }}`는 변수를 출력한다.
      - `{% if %}`는 `{% endif %}`로 꼭 닫아줘야 된다
   2. Jinja 코드로 for문을 구현한다.

3. `about.html`도 title 변수 받을 수 있게 수정해주자

------

## Layout

> 주로 웹페이지에선 body 태그 내용을 제외하고
> 나머지 html, head, title 태그 등은 대부분 중복되는 내용이다.
> 그래서 이러한 중복되는 코드는 하나의 template에 저장하고,
> 모든 template들은 이를 상속받게 할 수 있다.
> 이걸 layout 혹은 base라고 부른다.

1. `templates/layout.html` 생성

   ```html
   <!DOCTYPE html>
   <html>
   <head>
   	{% if title %}
   		<title>Flask Blog - {{ title }}</title>
   	{% else %}
   		<title>Flask Blog</title>
   	{% endif %}
   </head>
   <body>
   	<!-- 참고 1 -->
   	{% block content %}{% endblock %}
   </body>
   </html>
   ```

   참고:

   1. `content`라는 이름의 block을 만들고,
      이 영역안에 상속받는 template의 내용이 출력된다.

2. `templates/home.html` 수정

   ```html
   {% extends "layout.html" %} <!-- 참고 1 -->
   {% block content %} <!-- 참고 2 -->
   	{% for post in posts %}
   		<h1>{{ post.title }}</h1>
   		<p>By {{ post.author }} on {{ post.date_posted }}</p>
   		<p>{{ post.content }}</p>
   	{% endfor %}
   {% endblock content%}
   ```

   참고:

   1. `layout.html`을 상속받으라고 지시해준다
   2. `content` block 안에 넣는 내용이 `layout.html`의 `content` block 영역에 표출된다.

3. `templates/about.html`도 layout 상속받게 해주자

------

## Style

> 웹페이지에 당연히 스웨~그가 있어야 된다.

1. Boostrap 사이트로부터 css 링크, script 태그를 `layout.html`에 적절히 복붓해주자: [링크](<https://getbootstrap.com/docs/4.3/getting-started/introduction/#starter-template>)

2. Custom CSS도 추가해 주자

   - 프로젝트 폴더에 `static` 폴더를 생성해주고,
     그 안에 `main.css` 생성 (코드 참고)

   - `layout.html`에 css 링크 추가

     ```html
     <!-- head 태그 안에 -->
     <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='main.css') }}">
     ```

     참고: `url_for()`를 사용해서 `static` 폴더 안의 `main.css` 경로를 찍어준다.

   - `flaskapp.py`에 `from flask import url_for` 추가

3. 요즘 유행하는 blog 스타일을 따라하자~

   - `layout.html`에 navigation bar 추가 (코드 참고)
   - `layout.html`에 side bar 추가 (코드 참고)

4. **코드들이 너무 긴 것들은 github에 올라간 코드 참고하기를~**

## forms



