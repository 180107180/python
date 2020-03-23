"""
Парсер сайта "Белый ветер"
Создано на основе уроков 
https://www.youtube.com/watch?v=J5sqWAqDPyE
"""
import requests as rq
import csv
from bs4 import BeautifulSoup
#Константы
URL = 'https://shop.kz/smartfony/filter/nur_sultan-is-v_nalichii-or-ojidaem-or-dostavim/apply/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Mobile Safari/537.36','accept':'*/*'}
SITE = 'https://shop.kz'
FILE = 'phones.csv'
#Получение html кода страницы
def get_html(url,params=None):
    r = rq.get(url, headers=HEADERS,params=params)
    return r
#Парсинг контента
def get_content(html):
    #Наша html страница
    soup = BeautifulSoup(html, 'html.parser')
    #Ищем все эелементы с нужным названием класса
    items = soup.find_all('div',class_='bx_catalog_item_container gtm-impression-product')
    #Список где хранятся словари с параметрами
    phones =  []
    for item in items:
        #Цены
        prices = item.find_all('span',class_='bx-more-price-text')
        #В список добавляем словарь с 4 параметрами для каждого телефона
        phones.append({
            'model': item.find('div',class_='bx_catalog_item_title').findChild().get_text(),
            'link' : SITE + item.find('div',class_='bx_catalog_item_title').findChild().get('href'),
            'price' : prices[0].get_text()
        }) 
    return phones
#Подсчет количества страниц
def get_page_count(html):
    #Получаем страницы
    soup = BeautifulSoup(html,'html.parser')
    #Ищем все блоки кнопок индексации страниц
    pageCount = soup.find('div','bx-pagination-container row').find_all('li')
    #Возвращаем предпоследний элемент кнопки,содержащий количество страниц в данной категории
    return int(pageCount[-2].findChild().get_text())
#Сохранение данных в csv файле
def save_file(items, path):
    with open(path, 'w',newline='',encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',')
        #Инициирование первой строки определяющей названия стоблцов
        writer.writerow(['Model','Link','Price'])
        #Проходим по каждому блоку и 
        for item in items:
            #Проходим по списку со словарями и также записываем в новую строку
            writer.writerow([item['model'],item['link'],item['price']])
#Главная функция осуществляющая парсинг
def parse():
    #Получаем html
    html = get_html(URL)
    phones = []
    #Проверяем на наличие ответа от сервера
    if(html.status_code == 200):
        pages_count = get_page_count(html.text)
        #Проходим по страницам от 1 до 21 включительно
        for page in range(1,pages_count + 1):
            html = get_html(URL,params={'PAGES_1' : page})
            phones.extend(get_content(html.text))
        #После цикла сохраняем
        save_file(phones,FILE)
    else:
        print('Error')
    """
        Вывод списков
    print(phones)
    print(len(phones))
    """
parse()

