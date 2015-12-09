#!/usr/bin/python
# -*- coding: utf-8 -*-
from pymongo import MongoClient, ASCENDING
from _dist import DB_COLLECTION, DB_NAME, progress, get_line_count
import sys


def parse_line(line_item):
    is_root = not line_item[:2] == '  '
    separated = line_item.strip().split(' | ')
    is_archaic = separated[0][0] == '*'

    if is_archaic:
        separated[0] = separated[0][1:]

    record = {
        '_id': int(separated[2]),
        'word': separated[0],
        'details': separated[1],
        'is_archaic': is_archaic
    }

    return is_root, record


if __name__ == "__main__":
    try:
        file_name_input = sys.argv[1]
    except IndexError:
        print "Dictionary filename is not defined: python dict_to_mongo.py <dict_name>"
        exit(1)

    client = MongoClient()
    db = client[DB_NAME]
    db.drop_collection(DB_COLLECTION)
    collection = db[DB_COLLECTION]

    total_line_count = get_line_count(file_name_input)
    line_counter = 0

    last_root = None

    with open(file_name_input) as file_input:
        for line in file_input:
            line_counter += 1
            progress(line_counter, total_line_count, '%d / %d ' % (line_counter, total_line_count))

            process_item = line.replace('\n', '')
            if process_item == ' ':
                continue

            is_root, parsed_item = parse_line(process_item)

            if not is_root:
                parsed_item['prior'] = last_root
                collection.insert_one(parsed_item)
            else:
                last_root = collection.insert_one(parsed_item).inserted_id



    collection.create_index([('_id', ASCENDING)], unique=True)
    collection.create_index([('word', ASCENDING)], unique=False)

    print '\nDone.'
