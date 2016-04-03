# coding=utf-8
import re


class MeasureNormalizer(object):
    CHECK_TOKEN = re.compile(r'^[0-9]*(.[0-9]+)?$')
    CHECK_TYPE = 'WORD'

    _weight = [['g', 'kg', 'hwt', 't'], ['gram', 'kilogram', 'hundredweight', 'ton']]
    _distance = [['mm', 'cm', 'km'], ['millimeter', 'centimeter', 'meter', 'kilometer']]

    def get_token(self, index, tokens):
        if index + 1 >= len(tokens) or not tokens[index]['type'] is 'WORD':
            return False

        value = tokens[index]
        measure = tokens[index + 1]
        is_abb = measure in self._weight[0] + self._distance[0]
        ignore = 1

        if measure['token'] in self._distance[0]:
            is_abb = True
            func = self._get_normalized_distance
        elif measure['token'] in self._distance[1]:
            func = self._get_normalized_distance
        elif measure['token'] in self._weight[0]:
            is_abb = True
            func = self._get_normalized_weight
        elif measure['token'] in self._weight[1]:
            func = self._get_normalized_weight
        else:
            return False

        token = self._wrap(func(value['token'], measure['token']))

        if is_abb:
            try:
                next_item = tokens[index + 2]
                if next_item['token'] is '.' and next_item['is_nd']:
                    ignore = 2
            except IndexError:
                pass

        return ignore, token

    @staticmethod
    def _get_normalized_distance(value, measure):
        float_value = float(value)
        if measure in ['meter', 'm']:
            return float_value, 'meter', None
        elif measure in ['millimeter', 'mm']:
            return float_value / 1000, 'meter', 'millimeter'
        elif measure in ['centimeter', 'cm']:
            return float_value / 100, 'meter', 'centimeter'
        elif measure in ['kilometer', 'km']:
            return float_value * 1000, 'meter', 'kilometer'

    @staticmethod
    def _get_normalized_weight(value, measure):
        float_value = float(value)
        if measure in ['kilogram', 'kg']:
            return float_value, 'kilogram', None
        elif measure in ['gram', 'g']:
            return float_value / 1000, 'kilogram', 'gram'
        elif measure in ['hundredweight', 'hwt']:
            return float_value * 100, 'kilogram', 'hundredweight'
        elif measure in ['ton', 't']:
            return float_value * 1000, 'kilogram', 'ton'

    @staticmethod
    def _wrap(params):
        return {
            'type': 'GROUP',
            'grouper': 'MeasureNormalizer',
            'container': {
                'value': params[0],
                'measure': params[1],
                'normalized_from': params[2]
            }
        }


class NameChecker(object):
    CHECK_TOKEN = re.compile(r'.*')
    CHECK_TYPE = 'WORD'

    _title = [
        ['mr', 'mrs', 'ms'],
        ['miss', 'mister']
    ]

    _pre_name = re.compile(r'^((%s)[-\'])*[A-Z][a-z]+[A-z]*$' % '|'.join(
        [
            'de', 'la'
        ]
    ))

    _in_name = ['don', 'fon']

    def get_token(self, index, tokens):
        if index + 1 >= len(tokens) or not tokens[index]['type'] is 'WORD':
            return False

        title = tokens[index]['token'].lower()
        is_abb = False
        ignore = 1

        if title in self._title[0]:
            is_abb = True
        elif title in self._title[1]:
            pass
        else:
            return False

        if is_abb:
            try:
                next_item = tokens[index + 2]
                if next_item['token'] is '.' and next_item['is_nd']:
                    ignore += 1
            except IndexError:
                pass

        token = self._get_name_part(index + 1 + ignore, tokens)

        if not token:
            return False

        return ignore+len(token), self._wrap((title, token,))

    def _get_name_part(self, index, tokens):
        name_part = []

        for item in tokens[index:]:
            token = item['token']
            if item['type'] is 'WORD' \
               and (re.match(self._pre_name, token) or token in self._in_name):
                name_part.append(token)
            else:
                break
        return name_part

    @staticmethod
    def _wrap(params):
        return {
            'type': 'GROUP',
            'grouper': 'NameChecker',
            'container': {
                'title': params[0],
                'name': params[1],
            }
        }
