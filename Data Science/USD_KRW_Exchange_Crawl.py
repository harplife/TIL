from datetime import datetime as dt
import pandas as pd
from contextlib import contextmanager
import requests as re
from bs4 import BeautifulSoup
import time
from pathlib import Path


@contextmanager
def nested_break():
    '''
    Custom exception to break out of nested loops.
    '''
    class NestedBreakException(Exception):
        pass
    try:
        yield NestedBreakException
    except NestedBreakException:
        pass


def report_exchange(url, last_update):
    '''
    Exchange Rate crawler.
    url: any exchange page on finance.naver.com
    last_update: data will be crawled up to this date. Has to be datetime.date object.
    '''
    page = 1
    dataset = []

    cols = [
        '날짜', '매매기준율', '전일대비', '현찰 사실 때', '현찰 파실 때',
        '송금 보내실 때', '송금 받으실 때', 'T/C 사실 때', '외화수표 파실 때'
    ]

    with nested_break() as escape:
        while True:
            response = re.get(url+f'&page={page}')
            print(f'Processing page {page}')
            page += 1
            response_soup = BeautifulSoup(response.content, 'html.parser')
            tbody = response_soup.find('tbody')
            rows = tbody.find_all('tr')
            if len(rows) == 0:
                # if there is no data, then that's probably the end of data
                break

            for tr in rows:
                status = tr.attrs['class'][0]
                row = tr.find_all('td')
                row_parse = {}
                for i, (data, col) in enumerate(zip(row, cols)):
                    if i == 0:
                        date = data.text.replace('.', '-').strip()
                        date_dt = pd.to_datetime(date)
                        if date_dt == last_update:
                            raise escape
                        row_parse[col] = date
                    elif i == 2:
                        if status == 'down':
                            row_parse[col] = float('-' + data.text.replace(',', '').strip())
                        else:
                            row_parse[col] = float(data.text.replace(',', '').strip())
                    else:
                        row_parse[col] = float(data.text.replace(',', '').strip())
                dataset.append(row_parse)
    
    return dataset


USDKRW = 'https://finance.naver.com/marketindex/exchangeDailyQuote.nhn?marketindexCd=FX_USDKRW'

data_file = Path('exchange_rate.csv')

if data_file.is_file():
    print(f'{data_file} was found. Proceeding to UPDATE.')
    exchange_rate_df = pd.read_csv('exchange_rate.csv')
    exchange_rate_df['날짜'] = pd.to_datetime(exchange_rate_df['날짜'])
    last_update = exchange_rate_df['날짜'].max()
    #last_update = pd.to_datetime('2020-10-23')
    update_data = report_exchange(USDKRW, last_update)
    update_size = len(update_data)
    if update_size > 0:
        print(f'{update_size} number of updates available')
        update_data_df = pd.DataFrame(update_data)
        update_data_df['날짜'] = pd.to_datetime(update_data_df['날짜'])
        updated_df = pd.concat([exchange_rate_df, update_data_df], ignore_index=True)
        updated_df.drop_duplicates(subset=['날짜'], inplace=True)
        updated_df.sort_values(['날짜'], ascending=False, inplace=True)
        print('data updated. Now saving.')
        updated_df.to_csv('exchange_rate.csv', index=False)
    else:
        print('No Update Available')
else:
    print(f'{data_file} was NOT found. Proceeding to crawl ALL data.')
    last_update = None
    exchange_rate_data = report_exchange(USDKRW, last_update)
    exchange_rate_df = pd.DataFrame(exchange_rate_data)
    exchange_rate_df['날짜'] = pd.to_datetime(exchange_rate_df['날짜'])
    exchange_rate_df.sort_values(['날짜'], ascending=False, inplace=True)
    exchange_rate_df.to_csv('exchange_rate.csv', index=False)
