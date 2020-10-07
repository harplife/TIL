# FastAPI + ElasticSearch

ElasticSearch를 FastAPI 웹 프레임워크와 연동하여 문자열 데이터 CRUD 기능들을 활용한다.

Ubuntu 20.04 환경 (정확히는 WSL)에서 진행한다는 점 참고.



## FastAPI 기본 설정

파이썬 3.8 버전의 가상환경을 이미 구축했다는 가정하에 진행

1. `pip install fastapi` and `pip install uvicorn`

2. `vim main.py` 해주고 밑에와 같이 내용물 채워주기.

    ```Python
    from fastapi import FastAPI
    import uvicorn
    
    app = FastAPI()
    
    @app.get('/')
    def home():
        return {'hello': 'world'}
    
    if __name__ == '__main__':
        uvicorn.run('main:app', host='0.0.0.0', port=5002, reload=True)
    ```

3. `python main.py`로 실행해주고 localhost:5000에 정상 접속되는지 확인



## ElasticSearch 기본 설정

ElasticSearch 7.9버전 기준으로 진행. 좀 더 상세한 내용은 [링크](https://www.elastic.co/guide/en/elasticsearch/reference/current/deb.html) 참고.

1. 아주 간단. 밑에 명령어들만 갈겨준다.

    ```bash
    wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
    sudo apt install apt-transport-https
    echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-7.x.list
    sudo apt update && sudo apt install elasticsearch
    ```

2. `curl -X GET "localhost:9200/?pretty"`로 접속해서 대강 밑에와 같은 결과를 보면 정상적으로 실행됬다는 것을 확인할 수 있다.

    ```json
    {
      "name" : "Cp8oag6",
      "cluster_name" : "elasticsearch",
      "cluster_uuid" : "AT69_T_DTp-1qgIJlatQqA",
      "version" : {
        "number" : "7.9.1",
        "build_flavor" : "default",
        "build_type" : "tar",
        "build_hash" : "f27399d",
        "build_date" : "2016-03-30T09:51:41.449Z",
        "build_snapshot" : false,
        "lucene_version" : "8.6.2",
        "minimum_wire_compatibility_version" : "1.2.3",
        "minimum_index_compatibility_version" : "1.2.3"
      },
      "tagline" : "You Know, for Search"
    }
    ```

3. (Optional) 리붓시 ElasticSearch 자동 실행 설정. 참고로 WSL에선 안 됬다..

    ```bash
    sudo update-rc.d elasticsearch defaults 95 10
    ```

4. (참고) ElasticSearch 시작 및 종료

    ```bash
    sudo -i service elasticsearch start
    sudo -i service elasticsearch stop
    ```



## 사전 지식

- __인덱스 (index)__: 데이터베이스의 테이블하고 동일하다고 보면 된다.
  - 문서 생성할 시에 인덱스가 존재하지 않은 경우, 인덱스는 저절로 생성된다.
- __문서 (document)__: RDBMS 기준으로 봤을때 하나의 행(row)이라고 보면 된다. 물론 NoSQL 기준에선 하나의 JSON 파일로 보면 된다.
  - document를 생성할 시 id를 지정해줄수 있으며, 지정하지 않은 경우 자동 생성된다. auto-increment는 elasticsearch 기준으로 봤을때 anti-pattern으로서 기본적으로 사용되지 않는다.
- __문서번호 (id)__: 말 그대로 문서의 고유한 번호이다. 문서 CRUD 작업에 사용된다.
- __데이터필드 (field)__: RDBMS 기준으로 봤을때 하나의 열(column)이라고 보면 된다. 인덱스 설정(setting)에서 데이터필드에 대한 데이터 타입 등을 정의할 수 있다.
- __가명 (alias)__: 특정 조건에 따른 데이터의 뭉치라고 본다. 하나 또는 여러 인덱스에 대한 문서 조회가 가능하며, 검색 조건을 부여할 수 있다.
- __샤드(shard)__: elasticsearch와 같은 분산 db의 경우 데이터 저장소가 여러 조각으로 나뉘어져 있고, 이러한 조각을 샤드라고 칭한다. RAID 시스템과 유사한 점이 있다.
- __루트(route)__: 인덱스/가명에 특정 샤드에 대한 경로를 지정해줄 수 있다. 이로서 유사한 문서들을 하나의 저장소로 모을 수 있어 검색기능 최적화에 도움이 된다.
- __필터 (filter)__: 검색 조건 선언 영역이다. 검색 기능(search API)에 사용될 수 있으며, 가명 생성시 필터를 적용하여 검색기능 최적화에 도움이 된다.
- elasticsearch 조작은 기본적으로 HTTP Request를 보내는 형식으로 되기 때문에 공식문서 예제는 모두 cURL 기준으로 되어있다.
- Python에서 elasticsearch 조작하려면 3가지 방법이 있다.
  - SQLAlchemy 라이브러리 활용 (DB 조작 전용)
  - ElasticSearch 라이브러리 활용 (공식은 아닌것으로 알고 있다)
  - Request 라이브러리 활용 (Curl 방식을 추구하는 경우..)



## 디자인 패턴

[SO에서 따온 참된 정보](https://stackoverflow.com/questions/23123203/elasticsearch-routing-vs-indexing-for-query-performance)

ElasticSearch 창시자 Shay Banon이 말하기를, elasticsearch를 제대로 사용하는 디자인 패턴은 다음과 같다.
- Index by time range (시간단위로 인덱스 생성)
- Route by user (사용자 단위로 루트 생성)
- Alias for time windows (시간범위로 가명 생성)

### 예시

1. 매일 (또는 주기적으로) 인덱스를 생성한다. 이로서 오래된 인덱스들은 close 상태(데이터는 유지하되 인덱싱 대상에서 제외)로 전환할 수 있다. 루트를 user필드로 지정함으로서 user 필드 쿼리에 쓸데없는 샤드가 사용되지 않기 때문에 쿼리 속도가 비교적 빠르다.

    ```bash
    curl -X POST localhost:9200/user_logs_20140418 -d '{
      "mappings" : {
        "user_log" : {
          "_routing": {
            "required": true,
            "path": "user"
          },
          "properties" : {
            "user" : { "type" : "string" },
            "log_time": { "type": "date" }
          }
        }
      }
    }'
    ```

2. 가명을 생성하여 각 user에 대한 필터와 루트를 적용해 준다. 각 user 데이터가 여러 샤드로 나누어지지 않고 하나의 샤드로 묶이기 때문에 쿼리 속도가 비교적 빠르다. 더불어, 특정 user의 데이터가 상대적으로 너무 커지면 인덱스로 전환해줄 수 가 있다.

    ```bash
    curl -X POST localhost:9200/_aliases -d '{
      "actions": [{
        "add": {
          "alias": "user_foo",
          "filter": {"term": {"user": "foo"}},
          "routing": "foo"
        }
      }]
    }'
    ```

3. 특장 시간 범위에 따라 가명을 생성해준다. 일일(Day) 단위로 생성된 인덱스를 1주일로 합해서 본다.

    ```bash
    curl -X POST localhost:9200/_aliases -d '{
      "actions": [{
        "add": {
          "index": ["user_logs_20140418", "user_logs_20140417", "user_logs_20140416", "user_logs_20140415", "user_logs_20140414"],
          "alias": "this_week"
        }, 
        "remove": {
          "index": ["user_logs_20140413", "user_logs_20140412", "user_logs_20140411", "user_logs_20140410", "user_logs_20140409", "user_logs_20140408", "user_logs_20140407"],
          "alias": "this_week"
        }
      }]
    }'
    ```



## 코맨드라인 데이터 조작 : cURL 활용



### 인덱스 CRUD

#### Create index

1. 인덱스 유무를 확인한다. HEAD 타입의 request이기 때문에 HTTP CODE 200 또는 404 형식으로 대답이 온다. [HEAD vs GET](https://stackoverflow.com/questions/16539269/http-head-vs-get-performance)

    ```bash
    # bank 인덱스 유무 확인
    curl -I "localhost:9200/bank?pretty"
    ```

2. 인덱스를 생성한다. 가명도 같이 생성해준다. PUT 타입 request임으로 json 형식의 request body를 같이 보내준다.

    ```bash
    # bank 인덱스 생성,
    # accounts 가명(alias) 생성,
    # 인덱스에 lastname이 duke인 document만 필터해서 보는 dukes 가명 생성.
    curl -X PUT "localhost:9200/bank?pretty" -H 'Content-Type: application/json' -d '
    {
      "aliases": {
        "accounts": {},
        "dukes": {
          "filter": {
            "term": { "lastname": "duke" }
          }
        }
      }
    }
    '
    ```


#### Read index

1. GET 방식으로 인덱스 정보를 호출한다. Alias도 사용 가능하다.

    ```bash
    # bank 인덱스 정보 호출
    curl -X GET "localhost:9200/bank?pretty"
    # alias도 마찬가지로 호출 가능
    curl -X GET "localhost:9200/accounts?pretty"
    curl -X GET "localhost:9200/dukes?pretty"
    ```

2. GET 방식으로 인덱스의 document 총 개수를 센다. Alias도 사용 가능하다. 심지어 query기능도 엮어서 할 수 있다.

    ```bash
    # bank　인덱스 document 개수
    curl -X GET "localhost:9200/bank/_count"
    # 필드 firstname 값이 duke인 document 개수
    curl -X GET "localhost:9200/bank/_count?q=firstname:duke"
    ```

3. GET 방식으로 인덱스의 ***아주*** 상세한 정보를 호출한다. Alias도 사용 가능하다.

    ```bash
    curl -X GET "localhost:9200/bank/_stats?pretty"
    ```
    
4. 인덱스 명을 지정하지 않고 현재 elasticsearch에 어느 인덱스들이 있는지 조회 가능하다.
    cat API는 JSON 형식의 response를 주지 않기 때문에 앱 개발에는 사용되지 않는다..

    ```bash
    curl "localhost:9200/_cat/indices?v"
    ```

#### Update index

인덱스에서 업데이트 할 수 있는 영역은 인덱스설정(Settings), 필드정의(Mapping), 가명(Alias)이 있다.

1. 가명 추가
    - 가명 수정/삭제 방법은 [링크](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices.html#alias-management) 참고.
    - 가명 추가 방식은 3 가지로 나뉜다;
        - 인덱스 생성시 지정 - [바로가기](#Create index)
        - index alias API로 생성 및 업데이트
        
        ```bash
        # bank 인덱스에 필드 gender 값이 M인 문서만 호출하는 가명 gentlemen
        curl -X PUT "localhost:9200/bank/_alias/gentlemen?pretty" -H 'Content-Type: application/json' -d'
        {
          "filter" : {
            "term" : {
              "gender.keyword" : "M"
            }
          }
        }
        '
        ```
        
        - aliases API로 생성. 여러 인덱스에 묶어서 사용하는 방법도 있으니 [참고](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-aliases.html#indices-aliases-api-example).
        
        ```bash
        # bank 인덱스에 필드 gender 값이 F인 문서만 호출하는 가명 ladies
        curl -X POST "localhost:9200/_aliases?pretty" -H 'Content-Type: application/json' -d'
        {
          "actions": [
            {
              "add": {
                "index": "bank",
                "alias": "ladies",
                "filter": { "term": { "gender.keyword": "F" } }
              }
            }
          ]
        }
        '
        ```

2. Settings 추가 [링크](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices.html#index-settings) 참고.

3. Mapping 추가 [링크](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices.html#mapping-management) 참고.

#### Delete index

1. 엄청 간단! alias로 인덱스를 제거하는 것은 불가. 인덱스 삭제하면 인덱스에 등록된 alias들도 제거된다.

    ```bash
    curl -X DELETE "localhost:9200/bank?pretty"
    ```



### 문서 CRUD

#### Create document (+Bulk)

1. 문서 생성 시 인덱스가 없으면 인덱스가 자동 생성되며, 필드가 없으면 필드도 자동 생성된다. 굳이 Type을 지정할 필요도 없다.
참고: 밑에 명령어를 실행하면 json 형식에 response가 오고 id값이 자동생성 된 것을 볼 수 있다. (id 자동생성은 auto-increment가 아니니 내용물 확인하고 싶으면 id 따로 적어놓는게 좋다..)
   
    ```bash
   # bank 인덱스에 document 추가.
   curl -X POST "localhost:9200/bank/_doc/?pretty" -H 'Content-Type: application/json' -d'
   {
     "firstname": "kimchy",
     "lastname": "kang",
     "gender": "M"
   }
   '
    ```
   
2. 대량의 document에 대한 생성/업데이트/삭제는 _bulk API를 활용하여 가능하다. 자세한 사항은 [문서](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html) 참고. 대량의 document 생성 문항들을 포함한 json 파일을 인덱스로 업로드 할 수 있다. 다운로드 -> [accounts.json](https://raw.githubusercontent.com/elastic/elasticsearch/master/docs/src/test/resources/accounts.json)

    ```bash
    wget -O accounts.json https://raw.githubusercontent.com/elastic/elasticsearch/master/docs/src/test/resources/accounts.json
    curl -H "Content-Type: application/json" -X POST "localhost:9200/bank/_bulk?pretty&refresh" --data-binary "@accounts.json"
    ```

#### Read document (+Search)

1. 간단한 GET 방식의 데이터 호출. id를 사용하여 추가한 문서의 내용물을 확인할 수 있다.

    ```bash
    # 문서
    curl -X GET "localhost:9200/bank/_doc/94"
    ```

2. search API로 인덱스에 있는 ***여러*** 문서들 호출

    ```bash
    # bank 인덱스에서 document 20개 불러온다.
    curl -X GET 'localhost:9200/bank/_search?size=20' -d '{"query":{"match_all":{}}}' -H 'Content-type: application/json'
    
    # 가명을 통해 특정 조건에 맞게 조회가 가능하다. 위에 만들었던 gentlemen 가명은 gender 필드 값이 M인 document만 호출한다.
    curl -X GET 'localhost:9200/gentlemen/_search?size=20' -d '{"query":{"match_all":{}}}' -H 'Content-type: application/json'
    ```

3. search API로 특정 조건에 맞는 문서들 호출

    ```bash
    # bank 인덱스의 모든 필드를 상대로 duke라는 키워드가 있는 document 찾기
    curl -X GET 'localhost:9200/bank/_search?q=duke'
    # bank 인덱스에 gender 필드 값이 M인 document 찾기
    curl -X GET 'localhost:9200/bank/_search?q=gender:M'
    ```

#### Update document

1. update API를 활용한다. create API와 혼동되지 않게 조심해야 한다.

    ```bash
    # 94번 문서를 업데이트 한다.
    curl -X POST "localhost:9200/bank/_update/94" -H 'Content-Type: application/json' -d '
    {
      "doc" : {
        "lastname": "jerry",
        "employer": "benny"
        }
    }
    '
    ```

#### Delete document

1. 아주 간단하게 문서를 지운다.

    ```bash
    curl -X DELETE "localhost:9200/bank/_doc/94"
    ```



## 파이썬 데이터 조작 : Requests 패키지 활용

밑에 예시 코드는 [여기](https://github.com/harplife/TIL/blob/master/Python/requests_es.py)에 있으니 직접 실행해볼 수 있음.

### 인덱스 CRUD

#### Create index

1. 인덱스 유무 확인 - [링크](http://localhost:5002/index/exist/bank)

    ```python
    @app.get('/index/exist/{index}')
    def index_exist(
        index: str
        ):
        '''
        curl -I "localhost:9200/bank?pretty=true"
        '''
    
        params = {'pretty': 'true'}
        req_url = es_addr + '/' + index
    
        resp = requests.head(req_url, params=params)
    
        print('HTTP code:', resp.status_code, '-- response:', resp)
    
        result = {'index': index}
    
        if resp.status_code == 200:
            result['exists'] = True
            return result
        elif resp.status_code == 404:
            result['exists'] = False
            return result
        else:
            raise Exception(f'UNKNOWN STATUS CODE: {resp.status_code}')
    ```

2. 인덱스 생성 - [링크](http://localhost:5002/index/create/bank)

    ```python
    @app.get('/index/create/{index}')
    def index_create(
        index: str
        ):
        '''
        curl -X PUT "localhost:9200/bank?pretty"
        '''
    
        params = {'pretty': 'true'}
        req_url = es_addr + '/' + index
    
        resp = requests.put(req_url, params=params)
    
        print('HTTP code:', resp.status_code, '-- response:', resp)
    
        resp_json = json.loads(resp.text)
    
        return resp_json
    ```

#### Read index

1. 인덱스 정보 호출 - [링크](http://localhost:5002/index/read/bank)

    ```python
    @app.get('/index/read/{index}')
    def index_read(
        index: str
        ):
        '''
        curl -X GET "localhost:9200/bank?pretty"
        '''
    
        params = {'pretty': 'true'}
        req_url = es_addr + '/' + index
    
        resp = requests.get(req_url, params=params)
    
        print('HTTP code:', resp.status_code, '-- response:', resp)
    
        resp_json = json.loads(resp.text)
    
        return resp_json
    ```

#### Update index

1. 가명 생성 - [링크](http://localhost:5002/bank/alias/create/gentlemen?key=gender&value=M)

    ```python
    @app.get('/{index}/alias/create/{alias}')
    def alias_create(
        index: str,
        name: str,
        key: str = None,  # key/value pair for filter
        value: str = None
        ):
        '''
        curl -X PUT "localhost:9200/bank/_alias/gentlemen?pretty" -H 'Content-Type: application/json' -d'
        {
            "filter" : {
                "term" : {
                    "gender.keyword" : "M"
                }
            }
        }
        '
        '''
    
        params = {'pretty': 'true'}
        req_url = es_addr + '/' + index + '/_alias/' + alias
    
        if key is None:
            resp = requests.put(req_url, params=params)
        else:
            req_body = {
                'filter': {
                    'term': {
                        f'{key}.keyword': value
                    }
                }
            }
    
            resp = requests.put(req_url, params=params, json=req_body, headers={'Content-Type': 'application/json'})
    
        print('HTTP code:', resp.status_code, '-- response:', resp)
    
        resp_json = json.loads(resp.text)
    
        return resp_json
    ```

#### Delete index

1. 인덱스 삭제  - [링크](http://localhost:5002/index/delete/bank)

    ```python
    @app.get('/index/delete/{index}')
    def index_delete(
        index: str
        ):
        '''
        curl -X DELETE "localhost:9200/bank?pretty"
        '''
    
        params = {'pretty': 'true'}
        req_url = es_addr + '/' + index
    
        resp = requests.delete(req_url, params=params)
    
        print('HTTP code:', resp.status_code, '-- response:', resp)
    
        resp_json = json.loads(resp.text)
    
        return resp_json
    ```

### 문서 CRUD

#### Create document

1. 문서 생성 - [링크](http://localhost:5002/customers/document/create?gender=M&firstname=John)

    ```python
    @app.get('/{index}/document/create')
    def document_create(
        index: str,
        request: Request,
        did: str = None,
        ):
        '''
        curl -X POST "localhost:9200/bank/_doc/?pretty" -H 'Content-Type: application/json' -d '
        {
            "firstname": "kimchy",
            "lastname": "kang",
            "gender": "M"
        }
        '
        '''
    
        params = {'pretty': 'true'}
    
        req_body = request.query_params._dict
    
        if did:
            req_url = es_addr + '/' + index + '/_doc/' + req_body['did']
            del req_body['did']
        else:
            req_url = es_addr + '/' + index + '/_doc/'
    
        resp = requests.post(req_url, params=params, json=req_body, headers={'Content-Type': 'application/json'})
    
        print('HTTP code:', resp.status_code, '-- response:', resp)
    
        resp_json = json.loads(resp.text)
    
        return resp_json
    ```

2. Bulk insert는 일단 생략! 이건 html로 파일을 업로드 

#### Read document

1. 문서 번호로 문서 조회 - [링크](http://localhost:5002/customers/document/read/8sotAXUBL5jx-Q-4ifQ0)

    ```python
    @app.get('/{index}/document/read/{did}')
    def document_read(
        index: str,
        did: str
        ):
        '''
        curl -X GET "localhost:9200/customers/_doc/8sotAXUBL5jx-Q-4ifQ0"
        '''
    
        params = {'pretty': 'true'}
        req_url = es_addr + '/' + index + '/_doc/' + did
    
        resp = requests.get(req_url, params=params)
    
        print('HTTP code:', resp.status_code, '-- response:', resp)
    
        resp_json = json.loads(resp.text)
    
        return resp_json
    ```

2. 인덱스 내 여러 문서 조회 - [링크](http://localhost:5002/customers/document/scan)

    ```python
    @app.get('/{index}/document/scan')
    def document_scan(
        index: str,
        size: int = 20
        ):
        '''
        curl -X GET 'localhost:9200/customers/_search?size=20' -d '
        {
            "query":{"match_all":{}}
        }
        ' -H 'Content-type: application/json'
        '''
        params = {'pretty': 'true', 'size': size}
        req_url = es_addr + '/' + index + '/_search'
        req_body = {
            'query': {
                'match_all': {}
            }
        }
        headers = {'Content-Type': 'application/json'}
    
        resp = requests.get(req_url, params=params, headers=headers, json=req_body)
    
        print('HTTP code:', resp.status_code, '-- response:', resp)
    
        resp_json = json.loads(resp.text)
    
        return resp_json
    ```

3. 인덱스 내 키워드로 문서 검색 - [링크](http://localhost:5002/bank/document/search?keyword=M&field=gender)

    ```python
    @app.get('/{index}/document/search')
    def document_search(
        index: str,
        keyword: str,
        field: str = None,
        size: int = 20
        ):
        '''
        curl -X GET 'localhost:9200/bank/_search?q=duke'
        또는
        curl -X GET 'localhost:9200/bank/_search?q=gender:M'
        '''
        params = {
            'pretty': 'true',
            'size': size
            }
        if field is not None:
            params['q'] = field + ':' + keyword
        else:
            params['q'] = keyword
        req_url = es_addr + '/' + index + '/_search'
    
        resp = requests.get(req_url, params=params)
    
        print('HTTP code:', resp.status_code, '-- response:', resp)
    
        resp_json = json.loads(resp.text)
    
        return resp_json
    ```

#### Update document

1. 문서 업데이트 - [링크](http://localhost:5002/bank/document/update/94?lastname=jerry&employer=benny)

    ```python
    @app.get('/{index}/document/update/{did}')
    def document_update(
        index: str,
        did: str,
        request: Request
        ):
        '''
        curl -X POST "localhost:9200/bank/_update/94" -H 'Content-Type: application/json' -d '
        {
        "doc" : {
            "lastname": "jerry",
            "employer": "benny"
            }
        }
        '
        '''
    
        params = {'pretty': 'true'}
    
        req_body = {
            'doc': request.query_params._dict
            }
    
        req_url = es_addr + '/' + index + '/_update/' + did
    
        resp = requests.post(req_url, params=params, json=req_body, headers={'Content-Type': 'application/json'})
    
        print('HTTP code:', resp.status_code, '-- response:', resp)
    
        resp_json = json.loads(resp.text)
    
        return resp_json
    ```

#### Delete document

1.  문서 삭제 - [링크](http://localhost:5002/bank/document/delete/94)

    ```python
    @app.get('/{index}/document/delete/{did}')
    def document_delete(
        index: str,
        did: str
        ):
        '''
        curl -X DELETE "localhost:9200/bank/_doc/94"
        '''
    
        params = {'pretty': 'true'}
        req_url = es_addr + '/' + index + '/_doc/' + did
    
        resp = requests.delete(req_url, params=params)
    
        print('HTTP code:', resp.status_code, '-- response:', resp)
    
        resp_json = json.loads(resp.text)
    
        return resp_json
    ```

## 파이썬 데이터 조작 : SQLAlchemy 패키지 활용

### 인덱스 CRUD

### 문서 CRUD

