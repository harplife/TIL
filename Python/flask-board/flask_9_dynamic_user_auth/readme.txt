Flask를 활용한 Hello World라는 문자를 보여주는 앱

1. pip install flask
   -- flask 라는 패키지를 설치한다

(옵션 1)
===========================================
2. set FLASK_APP=flaskapp.py
   -- 환경변수 FLASK_APP을 지정해준다
   -- 이걸 지정해줘야 flask가 돌아간다
3. set FLASK_DEBUG=1
   -- 환경변수 FLASK_DEBUG를 1로 지정해준다
   -- debug 모드가 활성되야 코드변경사항이 실시간으로 적용된다.
   -- development 환경에서만 사용할 것.
      실제 구현환경 (production) 때는 해커를 방지하기 위해 debug mode off
4. flask run
   -- 문제 없으면 flask 서버가 돌아간다.
   -- localhost:5000 로 접속
===========================================

(옵션 2)
2. 밑에 코드를 구현할 시에 위에 환경변수들을 지정할 필요가 없다.

if __name__ == '__main__':
	app.run(debug=True)

3. python flaskapp.py
   -- 문제 없으면 flask 서버가 돌아간다.
   -- localhost:5000 로 접속
4. 주소에 /about 추가해서 접속할 시에 "About Page"라는 문자가 나온다.

===========================================
참고:

(RENDER_TEMPLATE)
1. render_template을 사용하면 templates 폴더안에 있는 .html 파일들을 불러올 수 있다.
2. 주로 template이란 단어는 html을 부를떄 사용된다.
3. 현재 이 정도 코드들만 구현하면 static web application 구현이 된다.

(JINJA)
1. flask를 사용하면 html내에서 python 코드를 구현할 수 있다.
2. 주로 {% 파이썬 함수 %}, {{ 파이썬 변수 }} 방식으로 사용된다. (코드 참고)

(LAYOUT)
1. 주로 body 태그 내용을 제외하고 나머지 html, head, title 태그들은 모든 template에서 반복된다.
2. 이렇게 반복되는 태그들을 따로 layout.html에 저장하고,
   각 template에 {% extends "layout.html" %} 써준다.
   layout.html에 body 태그안에 {% block content %}{% endblock %} 써주고,
   각 template에도 위처럼 써주고 그 사이에 사용할 html 콘텐츠를 넣어주면 된다. (코드참고)


(CSS/BOOTSTRAP)
1. 웹페이지 스타일은 CSS로 한다.
2. 직접 CSS을 만들 수 있지만 이미 BOOTSTRAP이라는 아름다운게 있으니 사용한다.
   -- 참고: https://getbootstrap.com/docs/4.3/getting-started/introduction/#starter-template
3. css 링크와 script 태그를 갖고와서 반복되는 거니 layout.html에 넣어서 사용한다.
4. 주로 <div> 태그를 사용해서 div에 대한 class로 스타일들을 적용한다.


(URL_FOR)
1. Flask의 기능중 URL_FOR 을 사용하면 쉽게 경로를 지정해줄 수 있다.
2. 이게 style에서 사용된 이유는 main.css 파일을 쉽게 불러올수 있게 사용된거다.
3. html에서 사용방법: {{ url_for('static'), filename='main.css' }}
   -- static 폴더안에 main.css라는 파일을 사용하라 지정


(FLASK_WTF, WTFORMS, VALIDATORS)
1. 웹어플 개발에서 login, register는 자주 사용되는 기능들이여서,
   FLASK에서 이 기능들을 파이썬 코드로 쉽게 구현할 수 있게 해준다.
   주로 FORM 같은 경우 HTML에서 직접 코드를 작성하지만,
   flask는 파이썬 코드를 html코드로 자동 변환해준다.
2. FlaskForm을 상속받는 클래스를 생성하고,
   클래스 안에 FORM의 내용을 기입하면 된다.
   (LoginForm 같은 경우 username, email, password, confirm_password, submit)
3. FORM 안에 있는 내용은 wtforms에서 갖고오는 FIELD 객체들을 갖고와서 사용한다.
   주로 문자열을 기입하는것은 StringField(). 비번기입하는 PasswordField, 등 있다.
4. 각 Field 안에서는 validators, 즉, 기입되는 정보에 대한 확인규칙을 지정해 줄 수 있다.
   - 이러한 확인규칙은 wtforms.validators에서 갖고올 수 있다.
   - DataRequired() => 데이터 꼭 기입해줘야 되는 규칙
   - Length(min=2, max=20) => 문자길이 2~20 사이라는 규칙
   - Email() => 이메일이 맞는지 확인하는 규칙
   - EqualTo('password') => 기입된 비번하고 같은지 확인하는 규칙
5. 이러한 form들을 만들고 flask실행 앱 (flaskapp.py)에서 forms.py를 import 해줘야 된다.
   - from forms import RegistrationForm, LoginForm
6. import한 form들을 지정 route (register, login)에 instance를 생성해 준다.
   - form = RegistrationForm()
7. 물론 이 form들이 갈 template(html)이 있어야되며, {{ form.변수.data }} 방식으로 사용한다.
   - register.html, login.html 코드 참고
8. 지정 route (register, login)에서 return값에 form도 넣어줘야 각 template에 form변수가 간다.
9. 주로 form의 method는 POST임으로서, 각 route에서 methods=['GET','POST']해줘야 된다. (코드 참고)
10. validator들이 제대로 실행되는지 확인하려면 {{ if form.변수.errors }}로 확인해야 된다. (코드 참고)
11. form이 제대로 submit됬는지 확인하려면 밑에 FLASH 함수를 사용한다.


(FLASH)
1. Flask의 flash('메세지')를 사용하면 post로 redirect된 페이지에서 flash 메세지를 확인할 수 있다.
2. 현재 구조로선 layout.html에 flash내용 받는 코드를 적용했다. (코드 참고)


(SQLALCHEMY)
1. flask에서 쉽게 db를 사용할수 있게 해주는 기능이다.
2. app.config으로 'SQLALCHEMY_DATABASE_URI' = 'sqlite:///site.db' 지정
   - 참고로 환경변수로 SQLALCHEMY_DATABASE_URI 저장해서 사용되는게 권장된다.
3. db = sqlalchemy(app)으로 sqlalchemy 인스턴스 생성
4. sqlalchemy는 주로 class를 사용해서 db 모델 객체를 생성한다.
   - 테이블이 생성되는게 아니라 db 구조가 생성되는 거다.
   - sql문을 사용할 필요 없이 python으로 하니 편하다;
   - 물론 나중에 직접 sql로 뭔가 할 수 있으면 좋겠지만...
   - relationship도 정의해서 User 모델과 Post 모델을 연결해줄 수 있다.
5. __repr__ 의 용도는 정확히 모르겠으니 python object modeling,
   혹은 dunder/magic method 찾아봐야 된다.
6. 아직 이 db는 홈페이지에 적용하지 않았다. 단지 db 생성 정도만 하게 되어있다.
7. 직접 sqlalchemy 사용해보는것은 db_python_practice.txt 와 db_user_instruction.png 참고


-- packaging --
1. 전에는 flaskapp.py에 모든 기능들을 넣어서 사용했었으나,
   기능이 많아질 수록 flaskapp.py 자체가 커지기 때문에 사용하기 불편해진다.
2. 위에 같은 이유로 flaskapp.py에 forms, models, routes 기능들을 각 .py파일로 옮긴다.
3. flaskapp.py에는 한개 import문과 if문 하나 있고, 자주 사용할꺼니 run.py로 이름 바꿔준다.
   - 앞으로 사용할떄 걍 python run.py 하면 된다.
4. 만들었던 forms, models, routes.py 파일들을 flaskapp이란 폴더에 넣어둔다.
5. flaskapp은 앞으로 사용할 package다.
   - 지정 .py 파일에서 객체를 갖고오면 module을 사용한다고 한다.
   - 지정 폴더로 부터 지정 .py파일의 객체를 갖고오면 package를 사용한다 한다.
   - 폴더를 python이 알아먹는 package로 만들려면 __init__.py 를 만든다.
     (비어있어도 괜찮다)
6. __init__.py
   - flaskapp 폴더 안에 있는 파이썬 객체를 갖고오면 기본적으로 __init__.py에 있는
     import, 변수, 함수들도 같이 사용된다. 폴더안에 모든 .py 파일들이 __init__으로 부터
     상속받는다고 생각하면 된다.
7. 주로 packaging을 하는 이유가 기능들을 세분화 하는것도 있지만, 
   circular import를 방지한다는 중요한 이유도 있다.


-- authorization/로그인 --
1. 애초에 웹개발에 있어 로그인 기능 구현은 자주 사용되고,
   개발하기 어려운 분야에 속한다.
2. 이런것을 아주 간단하게 사용할 수 있게 flask가 LoginManager라는것을 제공한다..
3. from flask_login import LoginManager 해줘야 된다. (init 코드 참고)
   - 인스턴스 생성
4. routes.py -> login route -> form.validate_on_submit() 코드 밑에,
   - 사용자가 입력한 password와 db에 있는 password가 동일한지 확인한다.
     - 참고로, from flask_bcrypt import Bcrypt, bcrypt 인스턴스 생성해서,
       register route안에서 사용자가 입력한 password를 hash 해준다. (코드 참고)
   - register된 (db) password와 사용자 입력 password가 동일할 시에,
     login_manager의 login_user를 사용해서 login 해준다. (cookie 사용)
5. 로그인 됬는지 확인하기 위해 account.html, account route 생성한다.
   - account.html 안에 login_manager의 current_user를 사용; current_user.username
   - account route는 login 된사람만 볼수 있게 login_manager의 login_required 기능 사용
6. 로그인 되어 있는 상태에서 login, register 들어가면 redirect하게 해준다.
   - login_manager의 current_user.is_authenticated 사용 (코드 참고)
7. 로그인 되어 있지 않은 상태에서 account 접속 시에 redirect;
   - init에서 login_manager.login_view, message 설정 (코드 참고)
8. 로그아웃 할 수 있게 logout route 설정;
   - login_manager의 logout_user 사용
9. 로그인/로그아웃 상태에 따라 navigation bar 내용 변경;
   - layout.html 코드 참고;