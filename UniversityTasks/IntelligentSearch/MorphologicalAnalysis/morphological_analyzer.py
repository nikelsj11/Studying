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


stat_pattern = u"""
CТАТИСТИКА:
    1: Общее количество токенов: %d.
    2: Количество токенов-пунктуации: %d.
    3: Количество токенов-словоупотреблений (не считая пунктуацию) : %d.
    4: Количество токенов-словоупотреблений, для которых не найдены признаки в словаре: %d.
    5: Количество токенов-словоупотреблений, для которых найдено более 1 варианта
                        нормализации или более 1 набора признаков (омонимичные токены): %d.
    6: Среднее количество омонимов из расчёта на 1 токен-словоупотребление
                                            (только для найденных в словаре словоформ): %d.
"""


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
    line_counter = 1

    token_counter = 0
    word_counter = 0
    punctuation_counter = 0
    not_found_counter = 0
    forms_counter = 0
    words_with_one_more_form = 0

    with open(file_name_output, 'w') as file_output:
        with open(file_name_input, 'r') as file_input:
            for line in file_input:
                progress(line_counter, total_line_count, ' %d / %d ' % (line_counter, total_line_count))

                tokenized = Tokenizer().tokenize(line.strip().replace('\n', '').decode('utf-8'))

                for token in tokenized:
                    token_counter += 1
                    if token['type'] is 'PUNCTUATION':
                        output = get_joined_line(token_counter, token['token'], token['type'])
                        punctuation_counter += 1
                    else:
                        specification = get_specification(finder, token['token'].lower())
                        if type(specification) is list:
                            len_specification = len(specification)
                            words_with_one_more_form += 1 if len_specification > 1 else 0
                            forms_counter += len_specification
                            word_counter += 1
                        else:
                            not_found_counter += 1
                            word_counter += 1

                        output = get_joined_line(
                            token_counter,
                            token['token'],
                            specification
                        )

                    file_output.write(output + '\n')

                line_counter += 1

            output = stat_pattern % (
                token_counter,
                word_counter,
                punctuation_counter,
                not_found_counter,
                words_with_one_more_form,
                forms_counter/(word_counter-not_found_counter),
            )

            file_output.write(output)

    print '\nDone.'
