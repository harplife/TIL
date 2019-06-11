# Flask 웹프레임워크 활용

## 설치

- `pip install Flask`

## 간단한 뼈대 만들기

참고: 완전 초간단 버전도 있지만 웹페이지 규모가 커질수록 FILE TREE가 복잡해져 코딩이 어려워진다. 이 뼈대는 패키징, 블루프린트를 고려한 방식이다.

1. 프로젝트 폴더 > flaskblog

2. `flaskblog/run.py` 생성

   ```python
   from flaskapp import create_app
   
   app = create_app()
   
   if __name__ == '__main__':
       app.run(debug=True)
   ```

3. `flaskblog/flaskapp` 폴더 생성

   4. `./flaskapp/__init__.py` 생성

      ```python
      from flask import Flask
      from flaskapp.config import Config
      
      
      def create_app(config_class=Config):
          app = Flask(__name__)
          app.config.from_object(Config)
      
          # blueprint section
          from flaskapp.main.routes import main
          app.register_blueprint(main)
          
          return app
      ```

   - `./flaskapp/config.py` 생성

     1. Python Shell에 접속

        ```python
        >>> import secrets
        >>> secrets.token_hex(16)
        '42dd46dc9a5e66336105b6d43ba0d85b'
        ```

        - secrets 패키지로 16bit hex값 생성. 복붓하기!

     2. `config.py` 내용 추가

        ```python
        import os
        
        class Config:
            SECRET_KEY = '42dd46dc9a5e66336105b6d43ba0d85b'
            # SECRET_KEY = os.environ.get('SECRET_KEY')
        ```

        - 주로 이런 설정값들은 환경변수로 저장해놓는게 좋다.
        - 이 SECRET_KEY는 flask자체의 csrf 공격 방어장치에 사용된다. 정확한 원리는 모르나 일단 POST 방식으로 웹에서 form 값을 보내려면 무조건 있어야된다.

4. `./flaskapp/main` 폴더 생성

   - `../main/__init__.py` 생성 (비워둠)

   - `../main/routes.py` 생성

     ```python
     from flask import render_template, Blueprint
     
     main = Blueprint('main', __name__)
     
     @main.route("/")
     @main.route("/home")
     def home():
         # render_template()은 templates 안의 .html 호출
         return render_template('home.html')
     ```

5. `./flaskapp/templates` 폴더 생성

   - `../templates/layout.html` 생성

     ```html
     <!DOCTYPE html>
     <html lang="en">
     <head>
         <title>Homepage</title>
     </head>
     <body>
         <div class="container">
             {% block content %} <!-- 중요!* -->
             {% endblock %}
         </div>
     </body>
     </html>
     ```

     - layout.html은 주로 다른 템플렛 (.html 파일)이 상속받을 레이아웃이다.
       layout.html을 상속받는 템플렛은 layout.html에 있는 내용들이 다 적용된다.
     - *block 안에 내용은 상속받는 템플렛의 내용이 들어간다.

   - `../templates/home.html` 생성

     ```html
     {% extends 'layout.html' %} <!-- 상속!* -->
     {% block content %} <!-- 중요!** -->
         <h1>Welcome to my Homepage!</h1>
     {% endblock %}
     ```

     - *`layout.html`을 상속받는다는것을 명시한다.
     - **`content`라는 이름의 block에 내용을 기입한다.
       `layout.html`의 block과 이름이 동일해야 된다. 

6. flask 웹 연동 테스트

   - cmd (debugging mode)

     ```bash
     (web_env) C:\...\flaskblog>python run.py
     ```

     - 웹에서 `localhost:5000`로 접속

   - cmd (production mode)

     ```bash
     (web_env) C:\...\flaskblog>set FLASK_APP=run.py
     (web_env) C:\...\flaskblog>flask run --host=0.0.0.0
     ```

     - 웹에서 로컬 IP 주소로 접속 (예: `192.168.1.1:5000`)

## 페이지 추가

1. `../templates/about.html` 생성

   ```html
   {% extends 'layout.html' %} <!-- 상속!* -->
   {% block content %} <!-- 중요!** -->
       <h1>About page</h1>
   {% endblock %}
   ```

2. `../main/routes.py` 수정

   ```python
   # 밑에 부분 추가!
   @main.route("/about")
   def about():
   	return render_template('about.html')
   ```

## python 변수를 web으로 출력하기

1. `../main/routes.py` 수정

   ```python
   @main.route("/about")
   def about():
   	greet = "Hello, World!" # 보낼 변수
   	return render_template('about.html', greet=greet)
   ```

2. `../templates/about.html` 수정

   ```html
   {% extends 'layout.html' %}
   {% block content %}
   	<h1>About page</h1>
   	{% if greet %} <!-- greet이란 변수가 있으면 -->
   		<h2>{{ greet }}</h2> <!-- greet변수 출력 -->
   	{% endif %}
   {% endblock %}
   ```

## URL에서 보내는 값을 python에서 받기 

1. `../main/routes.py` 수정

   ```python
   @main.route("/greet/<string:name>") # url에서 받는 변수
   def greet(name): # 함수에서 받고
       # greet.html로 보내주자~
   	return render_template('greet.html', name=name)
   ```

2. `../templates/greet.html` 생성

   ```html
   {% extends 'layout.html' %}
   {% block content %}
   	<h1>Welcome page</h1>
   	{% if name %} <!-- name이란 변수를 잘 받았으면 -->
   		<h2>Hello, {{ name }}!</h2> <!-- 출력~ -->
   	{% endif %}
   {% endblock %}
   ```

## FORM에서 POST request로 입력값 받기

1. 템플릿에서 직접 form을 작성하고 routes.py에서 입력값을 받아서 처리하는 방식이 있지만, flask_wtf이란 (복잡하지만) 편리한 패키지를 대신 사용할 수 있다.

   - null 값 처리, 문자길이 처리, 비번/비번확인 처리 등의 Form 입력값 처리 기능들을 포함하기에 따로 작성할 필요 없어 편리하다!

2. flask-wtf 패키지 설치

   - pip install flask-wtf

3. `../main/forms.py` 생성

   ```python
   from flask_wtf import FlaskForm
   from wtforms import StringField, PasswordField, SubmitField, BooleanField
   from wtforms.validators import DataRequired, Email
   
   
   class LoginForm(FlaskForm):
   	email = StringField('Email', 
                           validators=[DataRequired(),
                                       Email()])
   	password = PasswordField('Password', 
                                validators=[DataRequired()])
   	remember = BooleanField('Remember Me')
   	submit = SubmitField('Login')
   ```

   - StringField : 문자열을 받는 text input
   - PasswordField : 비번 받는 text input
   - BooleanField : 체크 박스 input
   - SubmitField : submit 버튼 input
   - validators : 확인 목록
     - DataRequired : null 값을 방지한다
     - Email : 이메일 주소인지 확인한다 (예: `someone@email.com`)

4. `../main/routes.py` 수정

   ```python
   from flaskapp.main.forms import LoginForm # 추가
   
   # 추가
   @main.route("/login", methods=['GET', 'POST'])
   def login():
   	# 꼭 forms.py의 LoginForm 함수에 대한 인스턴스 생성!
   	form = LoginForm()
       # POST로 FORM 입력값이 문제없이 받아졌을 경우,
   	if form.validate_on_submit():
   		# 입력값 처리
   		if form.email.data == 'admin@blog.com' and form.password.data == 'password':
   			return "LOGIN SUCCESS!"
   		else:
   			return "LOGIN FAILURE"
   	# GET으로 들어올땐 login.html로 보내주면서 form도 같이~
   	return render_template('login.html', title='Login', form=form)
   ```

5. `../templates/login.html` 생성

   ```html
   {% extends "layout.html" %}
   {% block content %}
   	<div class="content-section">
   		<form method="POST" action="">
   			<!-- csrf token for security measures -->
   			{{ form.hidden_tag() }}
   			<fieldset class="form-group">
   				<legend class="border-bottom nb-4">Log In</legend>
   				<div class="form-group">
   					<!-- 이메일 영역 -->
   					{{ form.email.label(class="form-control-label") }}
   					{% if form.email.errors %}
   						{{ form.email(class="form-control form-control-lg is-invalid") }}
   						<div class="invalid-feedback">
   							{% for error in form.email.errors %}
   								<span>{{ error }}</span>
   							{% endfor %}
   						</div>
   					{% else %}
   						{{ form.email(class="form-control form-control-lg") }}
   					{% endif %}
   				</div>
   				<div class="form-group">
   					<!-- 비번 영역 -->
   					{{ form.password.label(class="form-control-label") }}
   					{% if form.password.errors %}
   						{{ form.password(class="form-control form-control-lg is-invalid") }}
   						<div class="invalid-feedback">
   							{% for error in form.password.errors %}
   								<span>{{ error }}</span>
   							{% endfor %}
   						</div>
   					{% else %}
   						{{ form.password(class="form-control form-control-lg") }}
   					{% endif %}
   				</div>
   				<div class="form-check">
   					<!-- 체크 박스 영역 -->
   					{{ form.remember(class="form-check-input") }}
   					{{ form.remember.label(class="form-check-input-label") }}
   				</div>
   			</fieldset>
   			<div class="form-group">
   				<!-- submit 버튼 영역 -->
   				{{ form.submit(class="btn btn-outline-info") }}
   			</div>
   		</form>
   	</div>
   {% endblock content%}
   ```

## FLASH 메시지

1. 완료, 성공, 경고 메시지 등을 출력하는데 용이한 기능.
   주로 FLASH 메시지는 모든 페이지에 출력될 수 있어야 됨으로,
   layout.html에 message 받는 영역을 지정해준다.

2. `../templates/layout.html` 수정

   ```html
   <!-- 되도록이면 body태그 안 최상위에 추가 -->
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

3. 위에 url로 값 받는 예시 활용 ([보기](#url에서-보내는-값을-python에서-받기))

   - `../main/routes.py` 수정

     ```python
     from flask import flash # 추가
     
     # greet 함수 추가~
     @main.route("/greet/<string:name>")
     def greet(name):
     	if name:
     		# flash 성공 메시지, class='success'
     		flash(f'Welcome, {name}!', 'success')
     	# return render_template('greet.html', name=name)
     	return render_template('greet.html')
     ```

4. http://localhost:5000/greet/name 으로 확인

## SQLITE 데이터베이스 활용

1. flask-sqlalchemy 패키지 설치
   - pip install flask-sqlalchemy
   - 

