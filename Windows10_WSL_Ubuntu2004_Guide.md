# Windows 10 WSL Ubuntu 20.04 가이드라인

## 개요

- Microsoft Store를 통해서 Ubuntu를 설치하는 경우 Ubuntu 설치 경로는 시스템 드라이브 (C)로 묶이며 변경이 *거의* 불가능하다. WSL Ubuntu이미지를 import해서 export하고 뭐하는 복잡한 방안이 Stackoverflow에 제시되긴 했으나, 매우 귀찮고 안 될 것 같으니 사양한다.
- Docker를 통해서 Ubuntu를 설치하는 경우 Ubuntu 이미지/콘테이너 설치 경로는 시스템 드라이브 (C)로 묶이며 이것도 또한 변경이 불가능하다. Stackoverflow 조차도 포기한 토픽이니 더한 삽질을 하지 말자. 물론 volume 또는 bind mount등의 솔루션이 있다고 하지만 이건 결국 Share 폴더 하나 만드는 작업으로, 시스템 구성 파일들은 결국 시스템 드라이브에 쌓인다.
- 저자는 시스템 드라이브 파티션 사이즈를 유난히 작게 해놔서 위에 조건들이 부적절함으로, 이를 극복하는 방안을 제시한다.

## 설치 방법

1. WSL Ubuntu 이미지를 설치할 경로를 선택한다. 예를 들어, D:\\WSL 폴더를 선택한다.

   ```powershell
   cd D:\\WSL
   ```

2. Microsoft Store 사이트(aka.ms)에서 Ubuntu 설치 파일만 가져온다. Store를 통해서 설치하는게 아닌것 꼭 참고. Ubuntu 설치 파일은 MS에서 대놓고 공개하는게 아니기 때문에 재량껏 찾아봐야 된다. 일단 밑에 명령어는 Ubuntu 20.04버전 설치파일을 가져오는 거니 그냥 사용할 것.

   ```powershell
   Invoke-WebRequest -Uri https://aka.ms/wslubuntu2004 -OutFile Ubuntu.appx -UseBasicParsing
   ```

3. 설치파일이 .appx 형식으로 되어있어 zip파일로 변환해주고 압축 풀어준다.

   ```powershell
   move .\Ubuntu.appx .\Ubuntu.zip
   Expand-Archive .\Ubuntu.zip
   ```

4. 압축 풀어줘서 나온 Ubuntu 폴더에 들어가면 ubuntu2004.exe 파일이 있다. 실행해주자.

   ```powershell
   cd .\Ubuntu\
   .\ubuntu2004.exe
   ```

5. 실행하면 아주 간단하게 Ubuntu가 열린다. 초기설정으로 아이디/비밀번호 입력이 요구되니 간단히 해준다.

6. 여기서 끝! 하기 보다는 윈도우에 WSL 관리자 기능이 있으니 활용해주자. 밑에 명령어를 사용하면 현재 윈도우에 설치된 WSL 커널 리스트를 뽑을 수 있으며, 기본 (Default) WSL이 어느것으로 지정되어 있는지 확인이 가능하다. 기본 WSL 커널은 코맨드창에서 wsl 명령어를 실행하면 접속되는 WSL 커널이다.

   ```powershell
   wslconfig /l
   ```

7. 혹시 방금 설치한 Ubuntu 20.04가 기본으로 설정되어 있지 않으면 밑에 명령어 실행해주자.
   ```powershell
   wslconfig /setdefault Ubuntu-20.04
   ```

8. 여기까지 에러없이 됬다면 끝이다. 에러 났으면 스택신님과 구글신님께 여쭤볼것.

## 파이썬 기본 설정

WSL Ubuntu 20.04에 `which python3` 해주면 기본적으로 python3.8버전이 설치되어 있는 것을 확인할 수 있다 (2020.09.16 기준). 파이썬 가상환경 하나 만들어서 테스트까지 해주자.

1. Ubuntu에 뭔가 설치하기 전에 매번 하듯이, 리눅스 창시자 Linus Torvalds신님께 기도문을 드리자.

   ```bash
   sudo apt update
   sudo apt upgrade
   ```

2. 리눅스에서 파이썬 사용하기 전에 매번 뭔지 뭐르지만 매번 하듯이, 파이썬 창시자 Guido van Rossum신님께도 기도문을 드리자.

   ```bash
   sudo apt install build-essential checkinstall libffi-dev python-dev
   sudo apt install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
   ```

3. 이제 받을수 있는 축복은 다 받았으니 가상환경 깔아주자. 일단 WSL 환경안에 프로젝트 폴더가 있으면 윈도우 환경에서 찾기 귀찮아지니 윈도우 환경에서 쉽게 접근할 수 있는 경로에 프로젝트 폴더 하나 생성하고 들어가주자.

   ```bash
   cd D:\\Pyject
   ```

4. 파이썬 3버전에서 가상환경 만드는 것은 무조건 venv다. env라는 이름의 가상환경 만들어주고 활성화까지 하자.

   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

5. 가상환경 활성화가 제대로 됬는지 확인한다.

   ```bash
   which python
   which pip
   python
   ```
   ```python
   print('hello world')
   ```

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
