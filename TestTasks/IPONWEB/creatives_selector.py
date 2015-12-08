#!/usr/bin/python
# -*- coding: UTF-8 -*-
from _binary_heap import _heap_heapify, _heap_iter_max
import random


def creatives_selector(creatives, number_of_winners, country=None):
    creatives_holder, number_of_creatives, counter = dict(), dict(), number_of_winners

    # прохидимся по всем creatives, фильтруя по стране
    for creative in creatives:
        if creative['country'] is None or creative['country'] == country:
            price = creative['price']
            # creatives_holder - hash-table / key - уникальная стоимость
            # value - список creatives соответствующей стоимости
            try:
                creatives_holder[price].append(creative)
            except KeyError:
                creatives_holder[price] = [creative]

    # поочередно извлекаем максимумы из массива ключей creatives_holder
    for max_price in _heap_iter_max(_heap_heapify(creatives_holder.keys())):
        creatives_selection = creatives_holder[max_price]

        # формируем произвольный порядок обхода creatives текущей стоимости
        order = sorted([_ for _ in range(len(creatives_selection))], key=lambda k: random.random())

        #проходимся по creatives с необходимой стоимостью
        for number in order:
            creative = creatives_selection[number]

            # creatives_holder - результатирующая выборка
            # hash-table / key - уникальный advertiser_id, value - единственный выбранный creative
            if number_of_creatives.get(creative['advertiser_id']) is None:
                number_of_creatives[creative['advertiser_id']] = [creative]
                counter -= 1
                if counter == 0:
                    # необходимы размер выборки достигнут => объединение number_of_creatives values
                    return reduce(lambda x, y: x + y, number_of_creatives.values(), [])

    # в случае если данных недостаточно либо они некорректны - None
    return None

