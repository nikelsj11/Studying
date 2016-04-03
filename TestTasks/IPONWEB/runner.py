#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
from creatives_selector import creatives_selector

if __name__ == "__main__":
    creatives_list = []

    file_path = sys.argv[1]
    winners_count = sys.argv[2]
    country_name = sys.argv[3]

    for line in open(file_path, 'r'):
        line_preprocessed = line.replace('\n', '').split(' ')
        creatives_list.append({'advertiser_id': int(line_preprocessed[0]),
                               'price': int(line_preprocessed[1]),
                               'country': line_preprocessed[2] if len(line_preprocessed) == 3 else None})


    result = creatives_selector(creatives=creatives_list,
                                number_of_winners=int(winners_count),
                                country=country_name)


    for item in result or []:
         print '%s\t%s\t%s' % (str(item['advertiser_id']),
                               str(item['price']),
                               '-' if item['country'] is None else item['country'])

    if result is None:
        print 'result is empty'