#!/usr/bin/python
# -*- coding: utf-8 -*-
from pymongo import MongoClient, ASCENDING
from _dist import DB_COLLECTION, DB_NAME, progress, get_line_count
import sys
import os

reload(sys)
sys.setdefaultencoding('utf8')

# instance to simple_tokenizer
sys.path.append(os.path.dirname(os.getcwd() + '/../TextTokenization/simple_tokenizer'))
from simple_tokenizer import Tokenizer

def get_finder(db_name, db_collection):
    client = MongoClient()
    db = client[db_name]
    collection = db[db_collection]

    return {
        "find": lambda word: collection.find({"word": word}),
        "get_prior": lambda prior_id: collection.find_one({"_id": prior_id})
    }


def get_specification(finder, word):
    resulting_scope = []

    for record in finder['find'](word):
        prior = record.get('prior')
        if prior:
            resulting_scope.append(finder['get_prior'](prior))
        else:
            resulting_scope.insert(0, record)

    return resulting_scope or 'NOT FOUND'


def get_joined_line(token_number, word, obj):
    # print obj
    return u"%-*s %-*s %s" % (
        20,
        token_number,
        20,
        word,
        ''.join([u"[%s / %s / %s] " % (
            item['word'],
            item['details'],
            item['_id']
        ) for item in obj]) if type(obj) is list else obj
    )

if __name__ == "__main__":
    try:
        file_name_input = sys.argv[1]
        file_name_output = sys.argv[2]
    except IndexError:
        print "python morphological_analyzer.py <filename:input> <filename:output>"
        exit(1)

    finder = get_finder(DB_NAME, DB_COLLECTION)

    total_line_count = get_line_count(file_name_input)
    line_counter = 0

    token_counter = 0

    with open(file_name_output, 'w') as file_output:
        with open(file_name_input, 'r') as file_input:
            for line in file_input:
                progress(line_counter, total_line_count, ' %d / %d ' % (line_counter, total_line_count))

                tokenized = Tokenizer().tokenize(line.strip().replace('\n', '').decode('utf-8'))

                for token in tokenized:
                    token_counter += 1
                    if token['type'] is 'PUNCTUATION':
                        output = get_joined_line(token_counter, token['token'], token['type'])
                    else:
                        output = get_joined_line(
                            token_counter,
                            token['token'],
                            get_specification(finder, token['token'].lower())
                        )

                    file_output.write(output + '\n')

                line_counter += 1


