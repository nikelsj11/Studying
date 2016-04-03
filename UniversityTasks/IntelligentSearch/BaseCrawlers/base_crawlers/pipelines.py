# -*- coding: utf-8 -*-
import sqlite3

DB_PATH = 'base_crawlers/storage/habrahabr.sqlite'
DB_FIELDS_WITH_TYPE = '''
    title TEXT,
    author CHAR(255),
    rating INTEGER,
    views INTEGER,
    comments INTEGER,
    stars INTEGER,
    tags TEXT,
    article_id INTEGER,
    article_text TEXT NOT NULL
'''
DB_FIELDS = "title,author,rating,views,comments,stars,tags,article_id,article_text"
DB_DROP = "DROP TABLE habrahabr_data"
DB_INIT = "CREATE TABLE IF NOT EXISTS habrahabr_data (%s)" % DB_FIELDS_WITH_TYPE
DB_INSERT = "INSERT INTO habrahabr_data(%s) values (?, ?, ?, ?, ?, ?, ?, ?, ?)" % DB_FIELDS


# Pipline to store values from responses
class HabrahabrMonthlyItemPipline(object):
    def __init__(self, *args, **kwargs):
        super(HabrahabrMonthlyItemPipline, self).__init__(*args, **kwargs)
        self.db_connector = sqlite3.connect(DB_PATH)
        self.db_connector.text_factory = str
        self.cursor = self.db_connector.cursor()

        self.cursor.execute(DB_DROP)
        self.cursor.execute(DB_INIT)
        self.db_connector.commit()

    def process_item(self, record, _):
        self._insert_into_db(
            # normalization
            (
                record['title'][0] if self._is_not_empty(record.get('title')) else 'no-title',
                record['author'][0] if self._is_not_empty(record.get('author')) else 'no-author',
                int(record['rating'][0]) if self._is_not_empty(record.get('rating')) else 0,
                int(record['views'][0]) if self._is_not_empty(record.get('views')) else 0,
                int(record['comments'][0]) if self._is_not_empty(record.get('comments')) else 0,
                int(record['stars'][0]) if self._is_not_empty(record.get('stars')) else 0,
                ','.join(record['tags']) if self._is_not_empty(record.get('tags')) else 'no-tags',
                int(record['article_id'][0]),
                record['article_text'][0],
            )
        )

    @staticmethod
    def _is_not_empty(item):
        return item and item[0]

    def _insert_into_db(self, fields):
        self.cursor.execute(DB_INSERT, fields)
        self.db_connector.commit()

    def __del__(self):
        self.cursor.close()
