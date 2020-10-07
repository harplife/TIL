from fastapi import FastAPI, Request
import requests
import uvicorn
from pydantic import BaseModel  # pylint: disable=no-name-in-module
import json

app = FastAPI()

es_addr = 'http://localhost:9200'

class Data(BaseModel):
    name: str


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


@app.get('/{index}/alias/create/{alias}')
def alias_create(
    index: str,
    alias: str,
    key: str = None,
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
    headers = {
        'Content-Type': 'application/json',
        'charset': 'UTF-8'
        }

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

        resp = requests.put(req_url, params=params, json=req_body, headers=headers)

    print('HTTP code:', resp.status_code, '-- response:', resp)

    resp_json = json.loads(resp.text)

    return resp_json


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
    headers = {
        'Content-Type': 'application/json',
        'charset': 'UTF-8'
        }

    if did:
        req_url = es_addr + '/' + index + '/_doc/' + req_body['did']
        del req_body['did']
    else:
        req_url = es_addr + '/' + index + '/_doc/'

    resp = requests.post(req_url, params=params, json=req_body, headers=headers)

    print('HTTP code:', resp.status_code, '-- response:', resp)

    resp_json = json.loads(resp.text)

    return resp_json


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
    headers = {
        'Content-Type': 'application/json',
        'charset': 'UTF-8'
        }

    resp = requests.get(req_url, params=params, headers=headers, json=req_body)

    print('HTTP code:', resp.status_code, '-- response:', resp)

    resp_json = json.loads(resp.text)

    return resp_json


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
    headers = {
        'Content-Type': 'application/json',
        'charset': 'UTF-8'
        }

    resp = requests.post(req_url, params=params, json=req_body, headers=headers)

    print('HTTP code:', resp.status_code, '-- response:', resp)

    resp_json = json.loads(resp.text)

    return resp_json


if __name__ == '__main__':
    uvicorn.run("curly:app", host='0.0.0.0', port=5002, reload=True)