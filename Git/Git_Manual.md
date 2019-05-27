# Git 사용법
## 기본 명령어
1. git 저장소 (Respository) 초기화

   ```bash
   $ git init
   ```

   - 원하는 폴더를 저장소로 만들게 되면, `git bash`에서는 (`master`)라고 표기된다.
   - 그리고 숨김폴더로 `.git/`이 생성된다.
2. 커밋할 목록에 담기 (Staging  Area)

   ```bash
   $ git add .
   ```

   - 현재 작업 공간 (Working Directory/Tree)의 변경사항을 커밋할 목록에 추가한다 (add).
   - 리눅스에서 현재 디렉토리(폴더)를 표기하는 방법으로, 
     현재 내 폴더에 있는 파일의 변경사항을 전부 추가한다.
   - 단일파일만 추가하려면 `git add "파일이름"`
   - 폴더를 추가하려면 `git add "파일이름"`

3. 커밋하기

   ```bash
   $ git commit -m 'your message here'
   ```

   - 커밋을 할때에는 해당하는 버전의 이력을 의미하는 메시지를 반드시 적어준다.
   - 메시지는 지금 버전을 쉽게 이해할 수 있도록 작성한다.
   - 커밋은 현재 코드의 상태를 스냅샷 찍는 것이다.

4. 로그 확인하기

   ```bash
   student@M140418 MINGW64 ~/PycharmProjects/djangoon (master)
   $ git log
   commit 79620ed8e2daef0f1ebabbf42d0d0cd240aecf96 (HEAD -> master)
   Author: Ben Kim <ben.kim92@hotmail.com>
   Date:   Fri May 24 10:44:41 2019 +0900
   
   created .gitignore and HelloWorld.py
   ```

5. git 상태 확인하기

   ```bash
   $ git status
   ```

   - CLI (Command Line Interface) 현재 상태를 알기 위해 반드시 명령어를 통해 확인한다.
   - 커밋할 목록에 담겨 있는지, untracked 인지, 커밋할 내역이 있는지 등등 다양한 정보를 알려준다.

## 원경저장소 활용하기

1. 원격저장소 (Remote Repository) 등록하기

   ```bash
   $ git remote add <이름> <github url>
   ```

   - 위에 같이 (<,> 제외) 저장소 이름과 respository 경로를 지정해준다.
   - Remote는 한번만 등록하면 된다.
   - 아래의 명령어로 현재 등록된 원격 저장소를 확인할 수 있다.

   ```bash
   $ git remote --v
   ```

2. 원격저장소에 올리기 (push)

   ```bash
   $ git push <이름> master
   ```

   - remote를 통해서 원격저장소 master branch에 올린다.

3. 원격저장소로부터 가져오기 (pull)

   ```bash
   $ git pull <이름> master
   ```

## 원격저장소 복제 (clone) 하기

1. Repository의 있는 파일들을 저장할 local 폴더 하나 생성

2. 지정 폴더에서 git bash를 열고 밑에 명령어를 입력

   ```bash
   $ git clone <github url>
   ```





