# -*- coding: utf-8 -*-
import sqlite3
import codecs
import re
import shutil
import os

TAG_REGEXP = re.compile(r'<.*?>')
DB_PATH = '../BaseCrawlers/base_crawlers/storage/habrahabr.sqlite'
PWD = os.getcwd()

shutil.rmtree(PWD + '/raw')
os.mkdir(PWD + '/raw')


def remove_tags(text):
    return TAG_REGEXP.sub('', text)

db_connector = sqlite3.connect(DB_PATH)
bd_cursor = db_connector.cursor()

bd_cursor.execute("SELECT title,article_text FROM habrahabr_data")

records = bd_cursor.fetchall()

for record in records:
    title = u'#TITLE:%s\n' % record[0]
    raw = record[1]

    with codecs.open(u'raw/%s' % hash(title), 'w', 'utf-8-sig') as raw_file:
        raw_file.write(title + remove_tags(raw))

bd_cursor.close()
