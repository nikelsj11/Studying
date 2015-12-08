#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import xml.etree.ElementTree as etree
import json
import pymongo
import requests
import time


try:
    PATH_TO_XML = sys.argv[1]
except IndexError:
    print 'Error: no input file'
    exit(1)


HOST = "http://test.webjet.pro/api.php"

DB_NAME = "sender"
DB_COLLECTION = "results"

# подключаемся к бд на стандартный порт
conn = pymongo.MongoClient('localhost', 27017)
collection = conn['sender']['results']


# отправка письма
def send_email(email_id, email_to, email_subject):
    massage_json = json.dumps({'to': email_to, 'subject': email_subject})
    play_load = {'id': email_id, 'message': massage_json}

    try:
        response = requests.post(HOST, data=play_load)
    except requests.exceptions.Timeout:
        # обработка timeout
        return None, None

    return response.status_code, response.text


# сохранение результата в базу
def save_result_to_db(email_id, delivery_status):
    data_holder = {'id': email_id, 'delivery_status': delivery_status}
    collection.insert_one(data_holder)


parsed_id, parsed_to, parsed_subject = None, None, None
send_delayed = []

# итерируем записи XML фийла
for event, elem in etree.iterparse(PATH_TO_XML, events=('start', 'end')):
    # читаем внутри тега email: start + email = id / start + to = email address / start + subject = subject text
    if event == 'start':
        if elem.tag == 'email':
            parsed_id = elem.attrib.get('id')
        elif elem.tag == 'to':
            parsed_to = elem.text
        elif elem.tag == 'subject':
            parsed_subject = elem.text
    else:
        # конец чтения </email>  end + email => отправляем email
        if elem.tag == 'email':
            status_code, result = send_email(parsed_id, parsed_to, parsed_subject)

            # status = 200 пишем в базу, 503 либо timeout=None добавляем в стек на повторную отправку
            if status_code == 200:
                save_result_to_db(parsed_id, result)
            elif status_code == 503 or status_code is None:
                send_delayed.append([parsed_id, parsed_to, parsed_subject])

# повторная отправка
while len(send_delayed) > 0:
    for num, email_item in enumerate(send_delayed):
        status_code, result = send_email(email_item[0], email_item[1], email_item[2])

        # если письмо отправлено - удаляем из очереди + пишем в базу
        if status_code == 200:
            send_delayed.pop(num)
            save_result_to_db(parsed_id, result)





