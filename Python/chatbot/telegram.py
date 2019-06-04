import requests
from decouple import config
from bs4 import BeautifulSoup as BS
import operator
import collections

token = config('TOKEN')


def say_hello(sender_id, sender_name):
    text = f"Hello, {sender_name}. \nType HELP to get a list of all available functions!"
    chat_id = sender_id
    send_url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}"
    response = requests.get(send_url).json()
    print(response)


def repeat(sender_id, sender_msg):
    method = "sendMessage"
    chat_id = sender_id
    text = sender_msg
    api_url = f"https://api.telegram.org/bot{token}/{method}?chat_id={chat_id}&text={text}"
    response = requests.get(api_url)
    print(response)


def conversion(sender_id):
    url = 'https://finance.naver.com/marketindex/?tabSel=exchange#tab_section'
    html = requests.get(url).text
    soup = BS(html, 'html.parser')
    select = soup.select_one('#exchangeList > li.on > a.head.usd > div > span.value')

    # send result as telegram message
    method = "sendMessage"
    chat_id = sender_id
    text = '지금 원/달러 환율은 ' + select.text
    api_url = f"https://api.telegram.org/bot{token}/{method}?chat_id={chat_id}&text={text}"
    response = requests.get(api_url)
    print(response)


def naver(sender_id):
    url = 'https://www.naver.com/'
    response = requests.get(url).text
    soup = BS(response, 'html.parser')
    results = soup.select('.ah_roll_area.PM_CL_realtimeKeyword_rolling .ah_k')

    idx = 0
    text = ''
    for result in results:
        idx = idx + 1
        text = text + f"{idx}. {result.text}\n"

    # send result as telegram message
    method = "sendMessage"
    chat_id = sender_id
    api_url = f"https://api.telegram.org/bot{token}/{method}?chat_id={chat_id}&text={text}"
    response = requests.get(api_url)
    print(response)


def bitcoin(sender_id):
    url = 'https://www.bithumb.com/'
    html = requests.get(url).text
    soup = BS(html, 'html.parser')
    coins = soup.select('.coin_list tr')

    results = {}
    for coin in coins:
        name = coin.select_one('td:nth-of-type(1) p a strong').text.strip()
        price = float(coin.select_one('td:nth-of-type(2) strong').text.replace(',', '').replace('원', ''))
        price = round(price)
        results[name] = price

    sorted_results = sorted(results.items(), key=operator.itemgetter(1), reverse=True)
    text = ''
    for result in sorted_results:
        name, price = result
        text = text + '{} :: {:,d} 원\n'.format(name, price)

    # send result as telegram message
    method = "sendMessage"
    chat_id = sender_id
    api_url = f"https://api.telegram.org/bot{token}/{method}?chat_id={chat_id}&text={text}"
    response = requests.get(api_url)
    print(response)


def dusty(sender_id):
    opt = '&numOfRows=10&pageSize=10&pageNo=3&startPage=3&sidoName=서울&ver=1.6'
    key = 'serviceKey=QaGapZXPV5DTM72fy6lrf3hJnrJxhila1UVkPlUCo0N0g0F0RZ9WEngT8RkNjNo4IF%2BikV%2BthQLze39nK4IQjA%3D%3D'
    base = 'http://openapi.airkorea.or.kr'
    url = '{}/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?{}{}'.format(base, key, opt)
    request = requests.get(url).text
    # pip install lxml
    # beautifulsoup needs xml parser to parse xml
    soup = BS(request, 'lxml-xml')
    gangnam = soup('item')[7]
    location = gangnam.stationName.text
    time = gangnam.dataTime.text
    dust = int(gangnam.pm10Value.text)
    text = '{0} 기준 {1}의 미세먼지 농도는 {2}입니다.'.format(time, location, dust)
    # send result as telegram message
    method = "sendMessage"
    chat_id = sender_id
    api_url = f"https://api.telegram.org/bot{token}/{method}?chat_id={chat_id}&text={text}"
    response = requests.get(api_url)
    print(response)
