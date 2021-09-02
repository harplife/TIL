# Context Manager로 에러 핸들링하기

수정일자: 2021-09-02

프로그래밍을 하며 모든 Exception을 파악하고 미리 잡는 것은 불가능하다.
어느 정도 선에 특정 케이스에 대한 예외 처리를 해주고, 함수 전체에 try-except 를 걸어주는 것이 일단 최선이다.

하지만 여러 함수가 있으면, 각 함수에 대하여 예외 처리 해주는 것은 번거롭고,
특히 각 함수에 생기는 예외가 반복되는 경우가 있고,
또는 모든 함수에 공통적으로 처리되어야 하는 예외가 있을 수 있다.

위와 같은 이유로, 함수 내에 각 케이스별로 예외 처리하는 것을 대신하여
Context Manager를 활용하여 예외 처리해주는 방안을 제시한다.

## 이 방안을 찾게된 계기

파이썬으로 APM(Application Performance Management, 앱 성능 관리)를 구현하는 프로젝트를 진행 중이다.

특정 서비스를 모니터링하고, 서비스에 특정 장애가 발생하면 이메일/문자 발신을 하는 로직이 있다.

모니터링되는 서비스는 실제로 운영하고 있는 서비스로, 특정 장애가 실제로 발생되지 않는한은 테스트가 불가능하다. 이에 더불어, 코드에 에러가 있으면 특정 장애가 발생하지 않는 이상 확인하기가 어렵다.

위와 같은 이유로, 특정 장애 처리를 하는 코드에 에러가 발생될 경우, 이에 대한 예외 처리가 되어 "최소한"의 기능을 구현하여야 한다 - 여기서 최소한은 개발자 이메일로 코드에러가 발생했음을 알려주는 것이다.

## Context Manager의 기초지식

Context Manager는 지정된 코드를 "감싸주는" 기능을 구현한다.
(with 선언 또는 @decorator로 사용이 가능하다.)

지정된 코드가 실행되기 전에 실행되는 코드를 정의하고,
지정된 코드가 실행 중에 발생되는 예외에 대한 처리를 해주고,
지정된 코드가 실행된 후에 실행되는 코드를 정의한다.

Context Manager는 직접 만들 수 있지만,
기본 라이브러리인 contextlib 에서 contextmanager를 불러와 기본구조를 구성할 수 있다.
(저자는 후자를 선택했다.)

## 코드

### Context Manager 함수

Context Manager를 만드는 기본 코드는 밑에와 같다.
여기서 중요시 해야 할 부분은 `yield` 이다.

```python
from contextlib import contextmanager

@contextmanager
def session():
    try:
        print('세션 시작.')
        yield
    except Exception as e:
        print(f'세션 실패: {e}')
    else:
        print('세션 성공.')
    finally:
        print('세션 종료.')
```

### 테스트 1

Context Manager를 테스트 해보기 위해 함수를 하나 만든다.

```python
def division(x, y):
    print(x/y)
```

with 선언으로 함수를 감싸줘서 테스트 해본다.

```python
>>> with session():
...    division(2/4) # 정상
...    division(3/0) # 비정상
...
세션 시작.
0.5
세션 실패: division by zero
세션 종료.
```

위와 같이 예외 처리를 Context Manager가 대신해주는 것을 확인할 수 있다.

### 테스트 2

이번에는 Context Manager를 함수 안에 넣어서 테스트 해본다.

```python
def div_all():
    with session():
        division(2,4)
        division(3,0)
```

```python
>>> div_all()
세션 시작.
0.5
세션 실패: division by zero
세션 종료.
```

테스트 1과 결과가 동일하다. 코드상으로는 실제로 큰 차이도 나지 않는다.

저자는 테스트 2와 같은 사용 방안을 선호한다.
그 이유는, 여러 모듈들이 있는 경우, 메인 모듈에서 여러 모듈들에 대하여 예외처리 해주는 것보다는
각 모듈에서 알아서 처리 해주는게 더 편리하기 때문이다.

## 참고

Context Manager에 대하여 좀 더 자세한 사항은 저자가 작성한 글([링크](https://github.com/harplife/TIL/blob/master/Python/Decorated_Context_Managers.ipynb)) 또는 이 튜토리얼([링크](https://realpython.com/primer-on-python-decorators/))이 있다.