# Flask+Ngrok+Telegram = 챗봇

1. 초간단 flask app 설정

   ```python
   from flask import Flask
   app = Flask(__name__)
   
   def telegram():
       return ''
   ```

2. [Ngrok 다운로드](<https://ngrok.com/download>)

3. Ngrok 설정

   - ngrok 계정 생성

   - flask app이 있는 폴더 경로에 ngrok.exe 파일을 옮겨논다.

   - 프로젝트 경로 안 터미널에서 다음 명령어를 실행

     ```bash
     $ ./ngrok.exe http 5000
     ```
   - 위 명령어를 실행하면 localhost에 flask 서버로 포워딩 해주는 public url이 생성된다 (예: https://abf74cec.ngrok.io)
   - 생성된 주소를 밑에 텔레그램 webhook에 설정

4. [Telegram 봇 생성](<https://core.telegram.org/bots#6-botfather>)

5. [Telegram Webhook 설정 - setWebhook](<https://core.telegram.org/bots/api#setwebhook>)

   - https://api.telegram.org/bot<token>/setWebhook?url=<ngrok url>/<token or hex값 비밀번호>  <<< 로 접속
   - ngrok 주소 뒤에 남이 함부로 접속할 수 없게 복잡한 문자열을 추가한다.
   - 참고: ngrok public url은 8시간 시간 제한이 있어 만료 후에 다시 생성해야 된다. 다시 생성할 시에 주소가 바뀌니 webhook 설정도 매번 해줘야 된다.

6. FLASK 라우트 생성 및 설정

   ```python
   token = "8568****:AAHdrQteZHFZzjUksx-_hv43wY9scb--Mg*"
   @app.route(f"/{token}", methods=["POST"])
   def incoming():
       response = request.get_json()
       # response를 파싱하면 sender ID, Name, Msg 있음
       return '', 200
   ```

   - Flask 서버, Ngrok 서버가 돌아가는 상태이며, Telegram의 webhook이 설정이 되어있으면 봇에 메시지가 전송될 시에 webhook이 ngrok을 통해 flask 서버로 메시지를 relay 해준다.
   - 참고: return값은 무조건 '', 200 해줘야 된다. (API 문서 참고)

7. Flask에 받는 메시지 (예: "hello")에 대해 각 기능을 설정해주면 챗봇 완료!

## 추가 deet

1. Telegram 사용할 시에 매번 Token값을 사용해야 되고, 이런 코드를 공유할 떄 token 값이 노출된다. 이를 방지하기 위해 다음과 같이 한다;

   - decouple 패키지 설치 및 .env 파일 생성

      ```bash
      $ pip install python-decouple
      $ touch .env
      ```

   - .env 파일에 토큰값 기입

     - TOKEN='856***499:AAHdrQteZHFZzjUksx-_hv43wY9scb--Mg*'
     
   - token을 사용하는 각 python 파일에 다음과 같이 적용
   
      ```python
      from decouple import config
      token = config('TOKEN')
      ```
   - github에 업로드할 시에는 .gitignore에 .env를 추가