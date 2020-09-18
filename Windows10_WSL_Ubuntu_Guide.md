# Windows 10 WSL Ubuntu 가이드라인

## 개요

- Microsoft Store를 통해서 Ubuntu를 설치하는 경우 Ubuntu 설치 경로는 시스템 드라이브 (C)로 묶이며 변경이 *거의* 불가능하다. WSL Ubuntu이미지를 import해서 export하는 방안도 있긴 하나, 굳이 그렇게 까지 해야될까?
- Docker를 통해서 Ubuntu를 설치하는 경우 Ubuntu 이미지/콘테이너 설치 경로는 시스템 드라이브 (C)로 묶이며 이것도 또한 변경이 불가능하다. Stackoverflow 조차도 포기한 토픽이니 더한 삽질을 하지 말자. 물론 volume 또는 bind mount등의 솔루션이 있다고 하지만 이건 결국 Share 폴더 하나 만드는 작업으로, 시스템 구성 파일들은 결국 시스템 드라이브에 쌓인다.
- 저자는 시스템 드라이브 파티션 사이즈를 유난히 작게 해놔서 위에 조건들이 부적절함으로, 이를 극복하는 방안을 제시한다.

## 설치 방법

1. WSL Ubuntu 이미지를 설치할 경로를 선택한다. 예를 들어, D:\\WSL 폴더를 선택한다.

   ```powershell
   cd D:\\WSL
   ```

2. Microsoft Store 사이트(aka.ms)에서 Ubuntu 설치 파일만 가져온다. Store를 통해서 설치하는게 아닌것 꼭 참고. Ubuntu 설치 파일은 MS에서 대놓고 공개하는게 아니기 때문에 재량껏 찾아봐야 된다. 일단 밑에 명령어는 Ubuntu 20.04버전 설치파일을 가져오는 거니 그냥 사용할 것. 무조건 최신께 좋은게 아닌것이니 [Ubuntu 18.04 버전 링크](https://aka.ms/wsl-ubuntu-1804), [Ubuntu 16.04 버전 링크](https://aka.ms/wsl-ubuntu-1604) 참고.

   ```powershell
   Invoke-WebRequest -Uri https://aka.ms/wslubuntu2004 -OutFile wslubuntu2004.appx -UseBasicParsing
   ```

3. 설치파일이 .appx 형식으로 되어있어 zip파일로 변환해주고 압축 풀어준다.

   ```powershell
   move .\wslubuntu2004.appx .\wslubuntu2004.zip
   Expand-Archive .\wslubuntu2004.zip
   ```

4. 압축 풀어줘서 나온 Ubuntu 폴더에 들어가면 ubuntu2004.exe 파일이 있다. 실행해주자.

   ```powershell
   cd .\wslubuntu2004\
   .\ubuntu2004.exe
   ```

5. 실행하면 아주 간단하게 Ubuntu가 열린다. 초기설정으로 아이디/비밀번호 입력이 요구되니 간단히 해준다.

6. 여기서 끝! 하기 보다는 윈도우에 WSL 관리자 기능이 있으니 활용해주자. 밑에 명령어를 사용하면 현재 윈도우에 설치된 WSL 커널 리스트를 뽑을 수 있으며, 기본 (Default) WSL이 어느것으로 지정되어 있는지 확인이 가능하다. 기본 WSL 커널은 코맨드창에서 wsl 명령어를 실행하면 접속되는 WSL 커널이다.

   ```powershell
   wslconfig /l # Ubuntu 20.04 이름이 Ubuntu-20.04로 나온다.
   ```

7. 혹시 방금 설치한 Ubuntu 20.04가 기본으로 설정되어 있지 않으면 밑에 명령어 실행해주자.

   ```powershell
   wslconfig /setdefault Ubuntu-20.04
   ```

8. 여기까지 에러없이 됬다면 설치는 제대로 된것으로 본다. 에러 났으면 난 모르니 스택신님과 구글신님께 여쭤볼것.

9. 이제 다 설치됬고 실행도 되고 하니.. 리눅스 창시자 Linus Torvalds신님께 감사 기도문을 드리자.

   ```bash
   sudo apt update
   sudo apt upgrade
   ```

10. 여기서 동일한 버전의 WSL Ubuntu를 어떻게 여러개 설치할까 고민해본다. 그냥 똑같이 다시 반복하면 되지 않냐~라고 할 수도 있겄지만, 사실 그렇게 간단하지 않은게 WSL Ubuntu의 이름 때문이다. 그렇다, 위와 같이 설치하는 도중에 WSL Ubuntu의 이름을 지정하는 단계가 없다. 정해진 이름이 있고, 아무리 여러개 설치해봤자 이름은 다 같아서, `wsl -l`하면 그냥 뻘짓 했다는게 보인다. wsl로 접속하면 user이름이 다르지 않는 이상 어느 커널에 접속했는지 구분하기 힘들다... 그래서 저자는 무한한 삽질 끝에 닿은 지혜를 밑에 공유한다..!

   ```bash
   wsl --export Ubuntu-20.04 ubuntu2004.tar # 설치됬던 WSL Ubuntu를 .tar파일로 추출한다.
   wsl --import CustomUbuntu d:\wsl ubuntu2004.tar # 설치할 WSL Ubuntu의 이름을 지정하고, 대상경로를 지정하고, 설치파일 .tar를 지정한다.
   ```

11. 기본 WSL 커널 외에 다른 커널에 접속하고 싶은 경우 `wsl -l`로 커널 이름을 찾고, `wsl -d 커널이름`으로 실행해주면 된다.

12. WSL 커널 삭제하고자 하면 `wslconfig /u 커널이름` 해주면 된다. 물론 파일은 직접 지워주면 끝이다. 여기서 u는 unregister라는 뜻. 

## ZSH (& Oh My Zsh) 설정

그냥 bash사용하는 것도 괜찮지만 리눅스를 뽀대나게 사용하려면 zsh와 테마/플러그인 관리기능 oh my zsh도 깔아주면 좋다.

1. zsh 테마들을 사용하려면 powerline 폰트가 설치되어야 한다.

   ```bash
   sudo apt install fonts-powerline
   ```

2. zsh를 깔아주고 기본 Shell로 지정한다.

   ```bash
   sudo apt install zsh
   zsh --version # 제대로 깔렸으면 5.x 이상 버전으로 확인된다.
   chsh -s $(which zsh) # 기본 Shell 설정
   exec zsh # 기존 세션을 새 세션으로 대체한다
   echo $SHELL # /bin/zsh라고 비스므래 떠야 정상.
   ```

3. oh my zsh를 깔아주고 테마를 바꿔준다.

   ```zsh
   sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
   vim ~/.zshrc # zsh 설정파일이니 잘 참고하자
   ```
   .zshrc 파일 내에 `ZSH_THEME="robbyrussell"`로 되어있는 영역이 있다. robbyrussell 대신 agnoster로 대체하고 `exec zsh` 해준다.

## 파이썬 기본 설정

WSL Ubuntu 20.04에 `which python3` 해주면 기본적으로 python3.8버전이 설치되어 있는 것을 확인할 수 있다 (2020.09.16 기준). 파이썬 가상환경 하나 만들어서 테스트까지 해주자.

1. 리눅스에서 파이썬 사용하기 전에 매번 뭔지 뭐르지만 매번 하듯이, 파이썬 창시자 Guido van Rossum신님께도 기도문을 드리자.

   ```bash
   sudo apt install build-essential checkinstall libffi-dev python-dev
   sudo apt install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
   sudo apt install python3-venv # 사실 이거만 필요할 듯한데 
   ```

2. 이제 받을수 있는 축복은 다 받았으니 가상환경 깔아주자. 일단 WSL 환경안에 프로젝트 폴더가 있으면 윈도우 환경에서 찾기 귀찮아지니 윈도우 환경에서 쉽게 접근할 수 있는 경로에 프로젝트 폴더 하나 생성하고 들어가주자. 저자는 D 드라이브에 pyjects/pyject_01 폴더를 사용한다.

   ```bash
   cd /mnt/d/pyjects/pyject_01 # 윈도우 드라이브는 /mnt/드라이브/ 경로로 접속하면 된다.
   ```

3. 파이썬 3버전에서 가상환경 만드는 것은 무조건 venv다. env라는 이름의 가상환경 만들어주고 활성화까지 하자.

   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

4. 가상환경 활성화가 제대로 됬는지 확인한다.

   ```bash
   which python
   which pip
   python
   ```
   ```python
   print('hello world')
   ```

## NGROK 설정

내부망을 외부망으로 공유하는 NGROK을 설정해보자.

1. [NGROK 다운로드 페이지](https://ngrok.com/download)에 접속하여 MORE OPTIONS 버튼을 눌러 리눅스 버전 다운로드 [링크](https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip)를 복사한다. 그냥 다운로드해서 WSL에서 그냥 찾아가는 것도 일종의 방법이지만.. 리눅스는 리눅스 답게 코맨드라인으로 해결해보자!

2. curl로 NGROK 다운로드 압축파일을 가져온 후 압축해제 해준다. NGROK 코맨드를 사용하기 위해선 $PATH에 등록된 경로에 NGROK이 있어야 하니 /usr/bin으로 옮겨주기까지 해준다.

   ```bash
   cd /tmp
   curl -o ngrok.zip https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
   unzip ngrok.zip # ngrok 파일이 나온다.
   rm ngrok.zip # 아무리 tmp폴더라도 뭔가 들어있는게 싫다. 깨끗이 제거한다.
   mv ngrok /usr/bin/ # 그냥 아무대나 옮겨서 해당 폴더 경로 내에서 ngrok을 사용할 수도 있지만.. 개발자는 편리성을 추구한다.
   ```

3. authtoken 설정해주고 그냥 사용하면 된다. 자세한 구현방법은 ngrok 사이트를 참고하자.
