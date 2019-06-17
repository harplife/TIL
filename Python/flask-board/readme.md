# flask로 게시판 만들면서 배우기!

> **밑에 내용들을 순서대로 따라 하다보면 게시판 하나 만들어진다!!**

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

------

## forms

> 템플릿에서 직접 form을 작성하고 routes.py에서 
> 입력값을 받아서 처리하는 방식이 있지만, 
> flask_wtf이란 (복잡하지만) 편리한 패키지를 대신 사용할 수 있다.
>
> null 값 처리, 문자길이 처리, 비번/비번확인 처리 등의 
> Form 입력값 처리 기능들을 포함하기에
> 따로 작성할 필요 없어 편리하다!

1. flask-wtf 설치

   - `pip install flask-wtf`

2. 주로 게시판에 글 올리려면 로그인이 필요하다!

   - 일단 계정등록과 로그인 경로를 만들어주자~

     - `flaskapp.py`에서 home 경로 지정해준 것처럼
       간단히 register, login 경로 만들어 주고 얼맞게
       각자의 template들도 생성해주자

   - 프로젝트 폴더에 `forms.py` 생성

     ```python
     from flask_wtf import FlaskForm
     from wtforms import StringField, PasswordField, SubmitField, BooleanField
     from wtforms.validators import DataRequired, Length, Email, EqualTo
     
     # 계정생성 form
     class RegistrationForm(FlaskForm):
     	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
     	email = StringField('Email', validators=[DataRequired(), Email()])
     	password = PasswordField('Password', validators=[DataRequired()])
     	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
     	submit = SubmitField('Sign Up')
     
     # 로그인 form
     class LoginForm(FlaskForm):
     	email = StringField('Email', validators=[DataRequired(), Email()])
     	password = PasswordField('Password', validators=[DataRequired()])
     	remember = BooleanField('Remember Me')
     	submit = SubmitField('Login')
     ```

     참고:

     - flask_wtf 패키지를 사용하기 위해선 클래스를 생성하고 FlaskForm을 상속받는다.
     - `StringField`는 문자열을 받는 input 태그를 생성한다
     - `PasswordField`는 비번을 받는 input 태그를 생성한다
     - `SubmitField`는 submit 버튼을 생성한다
     - `BooleanField`는 체크박스를 생성한다
     - `validators`는 입력값을 확인해주는 기능들을 갖춘다
       - `DataRequired`는 null 값 방지
       - `Length`는 길이 제한
       - `Email`은 이메일 형식 (`john@email.com`)이 맞는지 확인
       - `EqualTo`는 지정 값과 동일한지 확인

   - 위에 만든 form들을 `flaskappy.py`에 적용해주자~

     ```python
     # 참고 1
     from forms import RegistrationForm, LoginForm
     # 참고 2
     app.config['SECRET_KEY'] = '42dd46dc9a5e66336105b6d43ba0d85b'
     
     # 참고 3(a)
     @app.route("/register", methods=['GET', 'POST'])
     def register():
     	form = RegistrationForm()
     	# 참고 3(b)
     	if form.validate_on_submit():
     		# 참고 4
     		flash(f'Account created for {form.username.data}!', 'success')
     		return redirect(url_for('home'))
     	return render_template('register.html', title='Register', form=form)
     
     @app.route("/login", methods=['GET', 'POST'])
     def login():
     	form = LoginForm()
     	if form.validate_on_submit():
     		# 짜가 계정 확인 절차
     		if form.email.data == 'admin@blog.com' and form.password.data == 'password':
     			flash('You have been logged in!', 'success')
     			return redirect(url_for('home'))
     		else:
     			flash('Login Unsuccessful. Please check yourname and password.', 'danger')
     	return render_template('login.html', title='Login', form=form)
     ```

     참고:

     1. `forms.py`로 부터 생성했던 form 클래스들을 import 해준다

     2. flask는 아주 착하게도 csrf 공격 방어 기능을 제공해준다.
        특히 form 자체를 사용하기 위해선 SECRET_KEY라는
        flask 설정값을 지정해줘야 된다.

        - 일단 간단히 secrets라는 내부모듈로 16진수 hex값을 생성해서 사용한다 (python shell)

          ```python
          >>> import secrets
          >>> secrets.token_hex(16)
          '42dd46dc9a5e66336105b6d43ba0d85b'
          ```

     3. b) `form.validate_on_submit()`은 form에 제대로 된
        입력값이 들어왔다는 신호를 POST request로 알려준다.
        a) 그럼으로서 `@app.route()`에 POST request 받는것을 지정해줘야 된다.

     4. flash 메시지는 화면 위에 이쁘게 메시지가 뜨는거다.
        flash 메시지를 받을 수 있게 `layout.html` main 태그 안, content block 위에 설정해주자

        ```html
        {% with messages = get_flashed_messages(with_categories=true) %}
        	{% if messages %}
        		{% for category, message in messages %}
        			<div class="alert alert-{{ category }}">
        				{{ message }}
        			</div>
        		{% endfor %}
        	{% endif %}
        {% endwith %}
        ```

   - form 클래스 생성하고, flaskapp에도 받게 설정해뒀으니
     이제 실제로 template에 form들을 적용해주자...
     코드가 길으니 github에 올라간 `login.html`, `register.html` 코드 참고!

     - 주의: csrf 공격 방어기능을 사용하려면
       **꼭!** form 태그안에 `{{ form.hidden_tag() }}` 기입해준다

3. 테스트!

   - login 페이지에서 `admin@blog.com/password`로 에러없이 로그인 되는지 확인!
   - login 페이지에서 입력값 없이 전송하면 에러 메시지 제대로 뜨는지 확인~
   - login 페이지에서 입력값 일부러 틀리게하면 에러 메시지 제대로 뜨는지 확인..
   - register 페이지.. 입력값 null 테스트, 입력값 이상하게 해봐서 제대로 에러 뜨는지 확인!!

## SQLITE 데이터베이스 설계

> Flask에서 SQLITE 데이터베이스와 연동하게 도와주는
> ORM (Object Relational Mapping) 도구는
> SQLALCHEMY라는 파이썬 패키지가 있다.
> SQL문을 사용할 필요가 없이 Python코드로
> 데이터베이스 CRUD 기능을 사용할 수 있다.
> 이걸 사용해서 사용자계정 DB, 게시글 DB를 만든다.

1. 패키지 설치

   - `pip install flask-sqlalchemy`

2. `flaskapp.py` 수정

   ```python
   # 밑에 부분들을 추가하면 된다~
   from flask_sqlalchemy import SQLAlchemy
   # sqlite기반 site.db 데이터베이스 파일사용 한다고 지정
   app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
   # SQLAlchemy 인스턴스 생성
   db = SQLAlchemy(app)
   
   # 사용자계정 데이터베이스 모델 구축!
   class User(db.Model):
   	id = db.Column(db.Integer, primary_key=True)
   	username = db.Column(db.String(20), unique=True, nullable=False)
   	email = db.Column(db.String(120), unique=True, nullable=False)
   	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
   	password = db.Column(db.String(60), nullable=False)
   	# create relationship
   	posts = db.relationship('Post', backref='author', lazy=True)
   
   	# dunder method, magic method
   	def __repr__(self):
   		return f"User('{self.username}', '{self.email}', '{self.image_file}')"
   
   # 게시글 데이터베이스 모델 구축~
   class Post(db.Model):
   	id = db.Column(db.Integer, primary_key=True)
   	title = db.Column(db.String(100), nullable=False)
   	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
   	content = db.Column(db.Text, nullable=False)
   	# setting foreign key using User model id
   	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
   
   	def __repr__(self):
   		return f"Post('{self.title}', '{self.date_posted}')"
   ```

   참고:

   - 모델들은 전부 `db.Model`을 상속받는 클래스로 구성된다.
   - `db.Column`은 테이블 열을 뜻하며, 상세한 설명은 필요없을 듯 하다.
   - `db.relationship`에 `backref='author'`는 중요!!
     - 보다시피 사용자계정 DB와 게시글 DB은 상관관계을 구축한다.
       게시글을 올리려면 게정이 있어야 되고,
       게시글 올린 계정 정보가 게시글 DB에서 query가 가능해야 된다.
       게시글 DB에서 연결된 계정정보를 가져올때,
       게시글.author로 하여금 데이터를 호출할 수 있다.
   - `__repr__`이 뭔지 궁금하면 dunder 혹은 magic method 구글해보기..

3. SQLALCHEMY 사용해보기!

   1. 이번 단계는 웹에서 구현하는게 아니라
      따로 python shell에서 사용해보는 단계임..

   2. 프로젝트 폴더 경로에서 가상환경과 연결된 cmd 열기~

   3. Python Shell에서 sqlalchemy 사용해보기

      ```python
      # db는 SQLAlchemy 인스턴스 받은 객체임
      from flaskapp import db
      from flaskapp import User, Post
      
      db.create_all() # db 생성
      User.query.all() # User db 내용 모두 호출
      Post.query.all() # Post db 내용 모두 호출
      user_1 = User(username='Corey', email='C@demo.com', password='password') # 내용 생성
      db.session.add(user_1) # 현재 세션에 내용 추가
      user = User.query.get(1) # User db에 첫번째 계정 호출
      post_1 = Post(title='Blog 1', content='First Post Content!', user_id=user.id) # 첫 계정으로 첫 게시글
      post_2 = Post(title='Blog 2', content='Second Post Content!', user_id=user.id) # 첫 계정으로 2번째 게시글
      
      db.session.add(post_1) # 세션에 게시글 1 추가
      db.session.add(post_2) # 세션에 게시글 2 추가
      db.session.commit() # 세션 저장!
      
      user.posts # 첫 계정의 게시글들을 호출한다
      post_1.author # 첫 글의 게시자 정보를 호출한다
      post_2.author # 두번째 글의 게시가 정보를 호출한다
      
      db.drop_all() # 데이터베이스 내용 전체 삭제
      ```

## Packaging

> 이 글 작성하면서 거부감이 제일 많이 가는 부분.. ㅎ
> 페키징은 말 그대로 이쁘게 포장하는 거다.
> 이떄까지 거의 모든 코드를 `flaskapp.py`에 쏘아붇었지만,
> 이제부터는 코드를 기능별로 세분화해서,
> 각자의 `.py` 모듈로 만들어 주고,
> 이 모듈들을 파이썬 패키지로 감싸준다.

1. 기능 세분화

   - 현재 `flaskapp.py`에는 앱 설정, DB 모델, 라우팅 경로가 있다.
     이들을 각자 `__init__.py`, `models.py`, `routes.py`로 나눠주자.

   - `__init__.py` : 앱 설정 코드들

     ```python
     from flask import Flask
     from flask_sqlalchemy import SQLAlchemy
     
     app = Flask(__name__)
     app.config['SECRET_KEY'] = '42dd46dc9a5e66336105b6d43ba0d85b'
     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
     db = SQLAlchemy(app)
     
     from flaskapp import routes
     ```

   - `models.py` : db 관련 코드들

     ```python
     from datetime import datetime
     from flaskapp import db
     
     class User(db.Model):
     	# 코드 생략
     
     class Post(db.Model):
     	# 코드 생략
     ```

   - `routes.py` : 라우팅 경로 관련 코드들

     ```python
     from flask import render_template, url_for, flash, redirect
     from flaskapp.forms import RegistrationForm, LoginForm
     from flaskapp.models import User, Post
     from flaskapp import app
     
     @app.route("/")
     @app.route("/home")
     def home():
     	return render_template('home.html', posts=posts)
     
     # 코드 생략
     ```

   - 패키징

     - 프로젝트 폴더 경로에 `flaskapp` 이름으로 폴더하나 생성
       - 굳이 `flaskapp`이름은 고정된게 아니니 아무 이름도 됨~
     - `flaskapp` 폴더에 위에 생성했던 파일 3개를 넣어준다!
     - 참고: `__init__.py`가 폴더 안에 있으면 파이썬은
       이 폴더를 파이썬 패키지로 인식한다!
       그 말은 즉슨 `flaskapp` 폴더 안에 있는 모듈을
       다음과 같이 호출할 수 있다;
       `from flaskapp.models import User, Post`
     - `site.db` 파일도 `flaskapp` 폴더로 옮겨주자!
     - `static`, `templates` 폴더들도  `flaskapp` 폴더로 옮기자~~

2. `run.py`

   - 이제 `flaskapp.py`에 남아있는 코드는 딱 두 줄일 것이다!
     `flaskapp` 패키지로부터 `app` 인스턴스 호출하는 코드 한 줄 추가.
     그리고 `flaskapp.py`를 `run.py`로 이름을 바꿔주자!

     ```python
     from flaskapp import app
     
     if __name__ == '__main__':
     	app.run(debug=True)
     ```

3. 현재 프로젝트 구조

   - 최상위 프로젝트 폴더
     - `run.py`
     - `flaskapp` 폴더
       - `static` 폴더
         - `main.css`
       - `templates` 폴더
         - `home.html`
         - `about.html`
         - `layout.html`
         - `login.html`
         - `register.html`
       - `__init__.py`
       - `forms.py`
       - `models.py`
       - `routes.py`
       - `site.db`

4. 테스트!!

   - `python run.py`로 실행해보자~

## 사용자 접근 제어 + DB 연결

> 웹개발에 있어 로그인 기능 구현은 거의 필수다!
> 근데 말이 간단히 로그인 기능이지,
> 실로 이걸 구현하려면 여러 기능들이 있어야  된다..
> 바로 이건 첩첩산중.
> 다행이도 flask가 이것도 해결해준다!
> 개봉박두 LoginManager!

1. LoginManager 설치

   - `pip install Flask-Login`

2. `./flaskapp/__init__.py` 라인 몇 개 추가~

   ```python
   from flask_login import LoginManager
   
   login_manager = LoginManager(app)
   login_manager.login_view = 'login'
   login_manager.login_message_category = 'info'
   ```

3. bcrypt

   - 데이터를 암호화 해주는 기능!
     앞으로 계정 DB에 비번 저장할때 비번을 암호화 할거임.
   - 설치
     - `pip install flask-bcrypt`
   - `./flaskapp/__init__.py` 라인 두 개 추가
     - `from flask_bcrypt import Bcrypt`
     - `bcrypt = Bcrypt(app)`

4. `./flaskapp/routes.py` - 계정 생성, 로그인 경로

   ```python
   # 추가
   from flaskapp import app, db, bcrypt
   from flask_login import login_user, current_user, logout_user, login_required
   
   @app.route("/register", methods=['GET', 'POST'])
   def register():
   	# 현재 접속된 계정이 있으면 redirect 해준다
   	if current_user.is_authenticated:
   		return redirect(url_for('home'))
   	form = RegistrationForm()
   	if form.validate_on_submit():
   		# brcypt로 비번을 암호화 해준다!!!
   		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
   		# 사용자 데이터
   		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
   		# 터미널에서 미리 db.create_all() 해줘야된다.
   		# 세션 입력값 저장
   		db.session.add(user)
   		db.session.commit()
   		flash('Your account has been created! You are now able to log in', 'success')
   		return redirect(url_for('login'))
   	return render_template('register.html', title='Register', form=form)
   
   @app.route("/login", methods=['GET', 'POST'])
   def login():
   	# 접속되어있음 딴데가라고
   	if current_user.is_authenticated:
   		return redirect(url_for('home'))
   	form = LoginForm()
   	if form.validate_on_submit():
   		# 입력된 이메일이 db에 있는지 확인
   		user = User.query.filter_by(email=form.email.data).first()
   		# 비번이 매치되는지 확인
   		if user and bcrypt.check_password_hash(user.password, form.password.data):
   			# 이메일, 비번이 모두 매치되면 로그인!
   			login_user(user, remember=form.remember.data)
   			# 참고 1
   			next_page = request.args.get('next')
   			return redirect(next_page) if next_page else redirect(url_for('home'))
   		else:
   			flash('Login Unsuccessful. Please check email and password', 'danger')
   	return render_template('login.html', title='Login', form=form)
   ```

   참고:

   1. `next_page` 변수는 나중에 로그인 상태가 아니면
      접속할 수 없는 페이지에서 로그인 페이지로
      redirect 됬을 경우에 사용된다.
      URL에 `next`라는 키값으로 접속하려 했던 경로를
      받아논 상태에서, 로그인이 되고 난 후에
      그 경로로 다시 redirect 해준다!

5. 계정 확인 페이지 추가!

   - `../templates/account.html`
     - 
   - `./flaskapp/routes.py`에 경로 추가

