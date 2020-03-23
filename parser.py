import requests as rq
import csv
from bs4 import BeautifulSoup
import os

URL = 'https://shop.kz/smartfony/filter/nur_sultan-is-v_nalichii-or-ojidaem-or-dostavim/apply/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Mobile Safari/537.36','accept':'*/*'}
SITE = 'https://shop.kz'
FILE = 'phones.csv'

def get_html(url,params=None):
    r = rq.get(url, headers=HEADERS,params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div',class_='bx_catalog_item_container gtm-impression-product')
    phones =  []
    for item in items:
        phone_action = item.find_all('div',class_='bx-catalog-middle-part')
        prices = item.find_all('span',class_='bx-more-price-text')
        if phone_action:
            phone_action = ''
        else:
            phone_action = 'No action'

        phones.append({
            'model': item.find('div',class_='bx_catalog_item_title').findChild().get_text(),
            'link' : SITE + item.find('div',class_='bx_catalog_item_title').findChild().get('href'),
            'action': phone_action,
            'price' : prices[0].get_text()
        }) 
    return phones
def get_page_count(html):
    soup = BeautifulSoup(html,'html.parser')
    pageCount = soup.find('div','bx-pagination-container row').find_all('li')

    return int(pageCount[-2].findChild().get_text())
#Сохранение данных в csv файле
def save_file(items, path):
    with open(path, 'w',newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Model','Link','Action'])

        for item in items:
            writer.writerow([item['model'],item['link'],item['action']])
def parse():
    html = get_html(URL)
    phones = []
    if(html.status_code == 200):
        pages_count = get_page_count(html.text)
        for page in range(1,pages_count + 1):
            print
            html = get_html(URL,params={'PAGES_1' : page})
            phones.extend(get_content(html.text))
        save_file(phones,FILE)
    else:
        print('Error')

    print(phones)
    print(len(phones))
def start_file
parse()

