# 도커(Docker)로 개발환경 구축하기



## 개요

도커(Docker)로 우분투(Ubuntu) 컨테이너 생성하는 것은 아주 쉽다. 간단히 `docker run -it ubuntu` 코맨드 넣어주면 곧바로 실행된다. 하지만 여기서 결정적인 문제가 있다. 도커허브에서 제공하는 우분투 이미지는 최소한의 환경설정만 유지된 우분투 이미지라서, 경량화 되어있지만 사용자가 따로 개발환경을 구축해야 한다는 번거로운 점이 있다.

이러한 이유 때문에 컨테이너를 생성하고 개발환경을 구축하려고 하는데, 사실 어디까지 설정을 수정해야 할지 몰라 그냥 개발하다가 에러 생기면 그 때 고치면 되지 하는 심정으로 진행하게 된다. 이것을 도미노스 이펙트라 하는지 버터프리 이펙트라 하는지 모르겠지만, 매번 에러 생길 때마다 설정해주고 이를 반복하다 보면 나중엔 이게 다 쓸데없는 짓이란 것을 알게되어 맨붕이 온다 (저자 경험담이니 참고하기를).

도커 컨테이너는 따로 persistent storage(지속성 저장소)를 지정하지 않아도 로컬 파일은 컨테이너 종료 시 유지되지만, 시스템 설정은 컨테이너 종료 시 리셋된다. 정확히 말하자면, 컨테이너는 시스템 설정을 저장하지 않는다. 시스템 설정을 그럼 어떻게 저장하는가라고 묻는다면, 

따라서, 저자는 도커의 정석을 따르는 방식으로 우분투 개발환경 구축하는 방안을 제시한다.



## 도커의 정석

도커는 기존에 사용되어 왔던 VM(가상머신)과는 다르다.  물론 OS 이미지를 갖고와서 실행시킨다(가상화한다)에는 변함이 없지만, 기존 VM에서는 작업내용이 OS 이미지 자체에 반영되는 반면, 도커에서는 로컬파일들만 컨테이너에 따로 저장되고 OS 이미지에는 아무런 영향을 끼치지 않는다. 컨테이너를 사용하는 동안, 또는 컨테이너 detach 하는 경우에도 변경된 시스템 설정들은 유지되지만, 완전히 컨테이너를 종료한 경우 변경된 시스템 설정은 없어진다. Stackoverflow 신 말씀으로는 `docker commit`을 해서 컨테이너를 새로운 이미지로 저장하면 된다고는 했는데, 결국 실행해보니 시스템 설정이 리셋됬다. 그나마 코멘트에서 좋은 조언을 얻었는데, 그것은 바로..

> Incrementally committing changes is not "the docker way". Use a Dockerfile.
> (번역: 변경사항을 하나하나 적용해나가는 것은 도커의 정석이 아니다. Dockerfile을 사용하라.)

정확히 이유도 안 밝히는, 뭔가 아는 사람만 알 수 있는 만한 조언이라 무시할 만 했지만, 투표수가 비교적 높아서 신빙성이 있어보인다.  그래서 도커의 정석이 무엇인지 삽질해보며, dockerfile이 무엇인지도 같이 톱질까지 해봤다.

도커의 정석을 알기 위해서는 먼저 dockerfile의 역할을 알아야 한다. 별로 설명할 것도 없다 (적어도 저자가 이해하는 범위 내에서는 ㅠ). Dockerfile은 변형된 도커 이미지를 생성하기 위한 도커 코맨드라인 스크립트 파일이라고 보면 된다. OS 이미지를 호출하고, 시스템 설정 변경하고, 패키지 설치하고. `docker build`만 해주면 개발환경이 적용된 OS 이미지가 생성이 되서, 이 이미지를 활용하여 개발환경이 미리 구축된 컨테이너를 쉽게, 여러 개 생성할 수 있다. 개발환경을 공유하려면 이미지를 복붗해서 주는게 아니라, dockerfile만 공유하면 된다.

Dockerfile을 알았다면 도커의 정석 또한 이미 다 알아낸 것이다. 변경사항을 하나하나 적용해나가는게 도커의 정석이 아니라면, 결국 변경사항을 한꺼번에 적용하는게 도커의 정석이라는 것인데, 이를 dockerfile로 이뤄내는 것이다. 이러한 방식이야 말로 언제 어디서나 쉽게 개발환경을 구축한다는 도커의 장점을 살릴수가 있는 것이다.

밑에 도커의 정식을 따른 예시를 하나 구현한다. 개발환경은 파이썬이다.



## Ubuntu + Python 개발환경 구축



### 개발환경 설정 목록

- Dockerfile로 생성할 이미지의 베이스는 도커허브에 올라온 `ubuntu:latest`이다 (2020.10.26 기준으로 우분투 20.04 버전).

- 도커 우분투는 경량화 되어 있기 때문에 한국어 설정이 되어 있지 않다. 우분투 언어 설정(locale)이 POSIX로 되어있어 영어를 제외한 다른 언어와 호환성이 전혀 없다. 사실 이 문제는 해결하기 ***아주*** 쉽다. 굳이 dockerfile로 안 하더라도, 컨테이너 내에서 또는 `docker run` 코맨드로 `LC_ALL` 환경변수의 값을 `C.UTF-8`로 지정해주면 된다. 그래도 dockerfile로 할 것이고, `C.UTF-8` 대신에 `ko_KR.UTF-8`로 값을 지정할 것이다.

- Python3, Python3-pip, Python3-venv도 설치해준다 (파이썬 3.8 버전)
- 저자가 애용하는 vim 에디터도 설치해준다. 참고로, vim을 설치하기 전에 파이썬이 먼저 설치되어 있어야 한다!
- git 설치해준다.
- curl 설치해준다.
- fonts-powerline 설치해준다 (zsh 쉘 사용하려면 필요하다).
- zsh 쉘 설치한다. oh-my-zsh (테마설정 도구)와 zsh-autosuggestions (코맨드 자동완성 플러그인)도 같이 설치한다.
  - *플러그인 사용하려면 zsh 설정파일에 추가해줘야 하는데, dockerfile로 문서 내 특정 자리에 글 넣는 방법은 아직 모르기 때문에 직접 해줘야 한다..ㅠ*
- 터미널 색상 설정을 변경한다. 환경변수 변경으로 `TERM` 값을 `xterm` 대신 `xterm-256color`로 대체해준다. 이거 안 해주면 파이썬 Syntax Highlighting 기능도 보기 흉하고 zsh-autosuggestions도 사용하기 어려워 진다.



### dockerfile 생성

폴더 하나 생성해주고, 폴더 안에 들어가서 밑에 내용으로 `dockerfile` 파일 하나 생성한다. 파일포맷은 없으니 `.txt`로 만들지 말것.

RUN은 명령어를 실행하고, ENV는 환경변수를 지정한다.

```dockerfile
FROM ubuntu:latest
RUN apt -y update && apt -y upgrade
RUN apt install -y build-essential
RUN apt install -y locales
RUN locale-gen ko_KR.UTF-8
ENV LC_ALL ko_KR.UTF-8
RUN apt install -y python3
RUN apt install -y python3-pip
RUN apt install -y python3-venv
RUN apt install -y vim
RUN apt install -y git
RUN apt install -y curl
RUN apt install -y fonts-powerline
RUN apt install -y zsh
RUN chsh -s $(which zsh)
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
RUN git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
ENV TERM xterm-256color
```



### 도커 이미지 생성

Dockerfile이 있는 위치에서 `docker build -t ubuntu:kr .` 코맨드 실행해주면 된다. `ubuntu`는 도커 이미지의 이름이고, `kr`은 도커 이미지의 태그가 된다. `ubuntu:latest`가 우분투 최신버전이라 본다면,  `ubuntu:kr`은 우분투 한국버전이라보니 이름을 이로 정했다.

`docker images` 코맨드 실행해주면 `ubuntu:kr`이라는 이미지가 생성된 것을 확인할 수가 있다.



### 도커 컨테이너 생성

`docker run -it -p 8001:8001 --name aicrm ubuntu:kr zsh` 코맨드 실행해주면 된다.

- `-it`는 interactive 모드로 컨테이너 생성과 동시에 터미널에 접속하는 설정이다. 원래 `-d` (detached/daemon 모드)가 통상적으로 사용되는데, 우분투는 `-d` 모드로 실행하면 절대 안 된다. 왜..인지는 SO신님께 문의 드릴것.
  - Interactive 모드에서 detached 모드로 전환하는 것은 `컨트롤+p & 컨트롤+q`이다.
- `-p 8001:8001`은 도커 컨테이너 8001 포트가 호스트 8001포트로 포트포워딩하는 설정이다. 굳이 필요한 것은 아니지만 네트워크 설정
- `--name aicrm`은 컨테이너 이름을 aicrm으로 지정해준다.
- `ubuntu:kr`은 컨테이너에 사용할 이미지를 지정한다. Dockerfile로 만들었던 이미지를 지정해주면 된다. 참고로, `docker run` 코맨드에서 위에 설정들이 앞으로 가야된다.
- `zsh`는 이미지 내에서 미리 zsh 쉘을 설치해줬으니 기본 쉘을 zsh로 지정해주는 것이다.



# FIN

끝내기전에 다시 한번 정리해보자면.. 도커의 정석은,

- Dockerfile로 개발환경 설정을 미리 구축한 이미지를 생성하여, 손쉽게 여러 컨테이너를 생성해서 사용하는 것이며,
- Dockerfile로 손쉽게 개발환경을 공유하는 것이다.



































![](https://media.giphy.com/media/U1rlk8zdcAwbm/giphy.gif)