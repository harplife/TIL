# Windows 10 WSL2 Ubuntu 가이드라인

## 개요

- Microsoft Store를 통해서 Ubuntu를 설치하는 경우 Ubuntu 설치 경로는 시스템 드라이브 (C)로 묶이며 변경이 *거의* 불가능하다. WSL Ubuntu이미지를 import해서 export하는 방안도 있긴 하나, 굳이 그렇게 까지 해야될까?
- Docker를 통해서 Ubuntu를 설치하는 경우 Ubuntu 이미지/콘테이너 설치 경로는 시스템 드라이브 (C)로 묶이며 이것도 또한 변경이 불가능하다. Stackoverflow 조차도 포기한 토픽이니 더한 삽질을 하지 말자. 물론 volume 또는 bind mount등의 솔루션이 있다고 하지만 이건 결국 Share 폴더 하나 만드는 작업으로, 시스템 구성 파일들은 결국 시스템 드라이브에 쌓인다.
- 저자는 시스템 드라이브 파티션 사이즈를 유난히 작게 해놔서 위에 조건들이 부적절함으로, 이를 극복하는 방안을 제시한다.
- 현재 기준 2020.09.22 으로 이후에 변경될 수 있다는 점 참고!

## 간단한 용어 정의

1. WSL -> Windows Subsystem for Linux의 약자이며, Windows 파일시스템에 접근이 가능한 리눅스 커널이라 보면 된다.
2. WSL 커널 -> WSL 자체 코어를 뜻한다.
3. WSL 배포 -> WSL 커널에 장착되는 OS Distro를 뜻한다.

## 잠깐만! 혼자 가기는 너무 위험하단다! 이걸 가져가렴.

1. 버전이 높다고 무조건 좋은게 아니다. WSL도 마찬가지로 1과 2버전이 있지만 2버전이 1버전보다 떨어지는 치명적인 약점이 하나 있다.. 이 사항은 프로젝트 개발에 많은 영향을 끼치니 아주 잘 기억해둬야 하는 사항이다! 그게 무엇인가 하면은 바로 Windows File System 활용 속도이다. WSL2는 분명 WSL1 보다는 빠르지만 Linux File System 안에서만 훨씬 빠른거지 Windows File System 내에서는 훨씬 뒤쳐진다는 것이다 (이게 바로 유리대포라는 것일까). 이 사항에 대해서는 Microsoft사가 공개적으로 [발표](https://docs.microsoft.com/en-us/windows/wsl/compare-versions#exceptions-for-using-wsl-1-rather-than-wsl-2)했으며.. 이런거는 문제가 되지 않다고 주장하는 이유가 바로 VS Code로 원격 프로젝트 개발이 가능하다는 점. `wsl --set-version`으로 WSL 배포의 WSL 커널 버전을 바꿀수 있다고 하니 참고해둘것.
    - 참고로 저자는 WSL2로 Windows File System 상에 Angular 프로젝트 개발을 진행하려다 `ng serve`가 너무 느려 원인을 파악하려다 위 사항을 알게됬다. Stackoverflow 말로는 WSL2에 Windows File System 활용 속도가 너무 느리기에 `ng serve`의 compiling 속도가 느려지는 것이라고 하니 이해가 된다.

2. WSL2에선 GPU 연동이 된다는 소식이 있다. 사실 이것은 Windows 체험판 (Insider Preview) 개발자 채널 버전에서만 가능하고, 최신 업데이트가 WSL과 Docker를 못 쓰게 만드는 버그가 있어 지금 당장은 불가능하다.

3. 리눅스에서 되는 모든게 WSL 리눅스 배포에도 무조건 될거라는 기대는 버리자. 스택신님께 문의를 드릴때 이런 구분이 중요하니 참고할 것.

## WSL2 Ubuntu 설치 및 

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

6. 여기서 끝! 이라기 보다는 윈도우에 WSL 관리자 기능이 있으니 활용해주자. 밑에 명령어를 사용하면 현재 윈도우에 설치된 WSL 배포 리스트를 뽑을 수 있으며, 기본 (Default) WSL이 어느것으로 지정되어 있는지 확인이 가능하다. 기본 WSL 베포는 코맨드창에서 wsl 명령어를 실행하면 접속되는 WSL 배포이다.

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
    sudo sh -c 'apt update && apt upgrade'
    ```

10. 여기서 동일한 버전의 WSL Ubuntu를 어떻게 여러개 설치할까 고민해본다. 그냥 똑같이 다시 반복하면 되지 않냐~라고 할 수도 있겄지만, 사실 그렇게 간단하지 않은게 WSL Ubuntu의 이름 때문이다. 그렇다, 위와 같이 설치하는 도중에 WSL Ubuntu의 이름을 지정하는 단계가 없다. 정해진 이름이 있고, 아무리 여러개 설치해봤자 이름은 다 같아서, `wsl -l`하면 그냥 뻘짓 했다는게 보인다. wsl로 접속하면 user이름이 다르지 않는 이상 어느 배포에 접속했는지 구분하기 힘들다... 그래서 저자는 무한한 삽질 끝에 닿은 지혜를 밑에 공유한다..!

    ```bash
    # 설치됬던 WSL Ubuntu를 .tar파일로 추출한다.
    wsl --export Ubuntu-20.04 ubuntu2004.tar
    # 설치할 WSL Ubuntu의 이름을 지정하고, 대상경로를 지정하고, 설치파일 .tar를 지정한다.
    wsl --import CustomUbuntu d:\wsl\CustomUbuntu ubuntu2004.tar
    ```

11. 기본 WSL 배포 외에 다른 배포에 접속하고 싶은 경우 `wsl -l`로 배포 목록을 보고, `wsl -d 배포이름`으로 실행해주면 된다.

12. WSL 배포 삭제하고자 하면 `wslconfig /u 배포이름` 해주면 된다. 물론 파일은 직접 따로 지워주면 끝이다. 여기서 u는 unregister라는 뜻. 

13. import한 WSL Ubuntu는 접속하면 root계정으로 곧바로 들어간다. Export했던 WSl Ubuntu에 초기 접속시 생성된 user는 있되, default 설정까지는 안 되어있다. 저자는 리눅스에 대해 잘 모르지만 일단 삽질한 결과 WSL에서 default user 설정하는 방법이 약간 다르다는것을 느껴 밑에와 같이 진행할 것을 추천한다.

    ```powershell
    # 윈도우 코맨드창에서 choco 깔아준다. choco는 리눅스 apt과 같은 윈도우 전용 패키지 매니저라 생각하면 된다.
    Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
    # choco를 사용해서 LxRunOffline이라는 WSL 유틸리티를 설치해준다.
    choco install lxrunoffline
    # default 설정해주려는 우분투 유저의 uid를 찾아야 된다.
    cat /etc/passwd | grep user01 # 초기 설정시 user01라고 이름 지었었다. user01:x:1000:1000라고 뜨는데, 여기 1000가 uid다.
    # LxRunOffline을 사용해서 default 유저를 지정해준다.
    LxRunOffline set-uid -n CustomUbuntu -v 1000
    ```

## WSL2 GPU 설정 (진행중)

1. 경고: 2020.09.22 기준으로 현재 Windows 10 Home/Pro Stable 버전에서는 지원되지 않는다. Windows Insider Preview (한마디로 윈도우 Edge 개발 버전)으로 업데이트 되어야 한다.
2. 경고: 2020.09.22 기준으로 현재 Windows 10 Insider Preview 업데이트 KB4571756 자체에 버그가 있어 WSL2 기능을 못 사용하게 되며, Docker 또한 못 사용하게 된다.
    - ref: [버그에 관한 Article](https://www.windowslatest.com/2020/09/09/windows-10-wsl-element-not-found-error/)
    - ref: [관련 깃헙 이슈](https://github.com/microsoft/WSL/issues/5880)
3. 적어도 위에 문제만 아니라면 [Microsoft 문서](https://docs.microsoft.com/en-us/windows/win32/direct3d12/gpu-cuda-in-wsl)와 같이 그냥 따라하면 될듯하다..

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

    ```bash
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
    vim ~/.zshrc # zsh 설정파일이니 잘 참고하자
    ```
    .zshrc 파일 내에 `ZSH_THEME="robbyrussell"`로 되어있는 영역이 있다. robbyrussell 대신 agnoster로 대체하고 `exec zsh` 해준다.

4. zsh에는 기본적으로 fish shell과 같은 autosuggestion 기능은 없지만, plugin 설치해서 무난하게 사용할 수 있다.

    ```bash
    # 플러그인 설치
    git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
    ```
    zsh 설정파일 내에 plugins 부분 수정(`vim ~/.zshrc`) => `plugins=(zsh-autosuggestions)`

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

## ElasticSearch 설치 및 구동

언제나 자세한 사항은 [Official Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/deb.html)을 보는 것이지만, 일단 밑에 되는것/핵심만 정리한다.

1. 밑에 명령들 그냥 복붗하면 설치 완료. 간단히 설명하자면 elasticsearch가 들어있는 apt repository를 먼저 등록해서 거기를 통해 설치파일 가져온다는 것.

    ```bash
    wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
    sudo apt install apt-transport-https
    echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-7.x.list
    sudo apt update && sudo apt install elasticsearch
    ```

2. [로컬 9200포트](http://localhost:9200/)에 접속해서 elasticseach가 제대로 돌아가는지 확인. 대강 밑에와 같이 나온다.

    ```json
    {
      "name" : "ZION-AI",
      "cluster_name" : "elasticsearch",
      "cluster_uuid" : "4n4VZbgYQNKDf_h7EaqCdw",
      "version" : {
        "number" : "7.9.1",
        "build_flavor" : "default",
        "build_type" : "deb",
        "build_hash" : "083627f112ba94dffc1232e8b42b73492789ef91",
        "build_date" : "2020-09-01T21:22:21.964974Z",
        "build_snapshot" : false,
        "lucene_version" : "8.6.2",
        "minimum_wire_compatibility_version" : "6.8.0",
        "minimum_index_compatibility_version" : "6.0.0-beta1"
      },
      "tagline" : "You Know, for Search"
    }
    ```

3. WSL 리붓하면 elasticsearch는 죽고 다시 시작하지 않는다.. 원래 리눅스에 startup script 로딩하는 방법이 따로 있긴 하지만, 일단 간단히 테스트한 결과 WSL에서는 잘 안되는 것 같다. 그렇기 때문에, WSL startup이 아닌, Shell(ZSH) startup script에 elasticsearch 시작 명령어를 박아넣어야 한다. `vim ~/.zshrc` 해주고, `sudo -i service elasticsearch start` 추가해주자. 이미 elasticsearch가 실행되고 있는 경우 탈이 생기는게 아니니 이 평법은 무난하다.

4. 데이터 입력 및 호출 : 한 줄 씩 추가

    ```bash
    # customer라는 인덱스가 자동으로 생성되며, 인덱스 1의 필드 'name'에 값이 추가된다.
    curl -X PUT "localhost:9200/customer/_doc/1?pretty" -H 'Content-Type: application/json' -d'
    {
      "name": "John Doe"
    }
    '
    # 방근 넣은 데이터 1개 확인하기.
    curl -X GET "localhost:9200/customer/_doc/1?pretty"
    ```

5. 데이터 입력 및 호출 : JSON 파일 추가 (예: [accounts.json](https://github.com/elastic/elasticsearch/blob/master/docs/src/test/resources/accounts.json?raw=true))

    ```bash
    # accounts.json 파일이 있는 경로로 먼저 가고.
    # bank라는 인덱스에 데이터를 집어 넣는다.
    curl -H "Content-Type: application/json" -XPOST "localhost:9200/bank/_bulk?pretty&refresh" --data-binary "@accounts.json"
    # 넣은 데이터 확인하기.
    curl -X GET "localhost:9200/bank/_doc/1?pretty"
    ```

## REFERENCE

- [wsl config 가이드](https://docs.microsoft.com/en-us/windows/wsl/wsl-config)
- [wsl FAQ](https://docs.microsoft.com/en-us/windows/wsl/faq)
