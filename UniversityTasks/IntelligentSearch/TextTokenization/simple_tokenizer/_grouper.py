# coding=utf-8
import re


class Grouper(object):
    COMPLEX_PUNCTUATION_MAPS = [['.', '.', '.']]

    def __init__(self, cp_maps=COMPLEX_PUNCTUATION_MAPS, abbreviations=None, cp_abbreviations=None, custom_maps=False):
        self.abbreviations = abbreviations
        self.cp_abbreviations = cp_abbreviations
        self.cp_maps = cp_maps
        self.custom_maps = custom_maps and [custom_map() for custom_map in custom_maps]

    def group(self, tokens):
        reprocessed_tokens = []
        ignore_next = 0

        for index, item in enumerate(tokens):
            is_untouched = True
            if ignore_next:
                ignore_next -= 1
                continue

            if self.custom_maps:
                for mapper in self.custom_maps:
                    if (mapper.CHECK_TYPE and mapper.CHECK_TYPE is item['type'] and mapper.CHECK_TOKEN and re.match(
                            mapper.CHECK_TOKEN, item['token'])):
                        map_result = mapper.get_token(index, tokens)

                        if map_result:
                            is_untouched = not is_untouched
                            ignore_next = map_result[0]
                            reprocessed_tokens.append(map_result[1])
                            break

            if is_untouched and item['type'] is 'PUNCTUATION':
                for mapper in self.cp_maps:
                    if item['token'] is mapper[0]:
                        is_mapper = True
                        mapper_len = len(mapper)

                        for map_item, self_item in map(None, mapper, tokens[index:index + mapper_len]):
                            if not (self_item and self_item['token']) is map_item:
                                is_mapper = not is_mapper
                                break
                        if is_mapper:
                            reprocessed_tokens.append(self._complex_punctuation_map(mapper))
                            ignore_next = mapper_len - 1
                            is_untouched = not is_untouched
                            break
            else:
                if self.abbreviations and item['token'] in self.abbreviations:
                    self._abbreviation_map(item)
                elif self.cp_abbreviations and item['token'] in self.cp_abbreviations:
                    if self._is_complex_abbreviations(index, tokens):
                        self._abbreviation_map(item, is_cp=True)
                        ignore_next = 1

            if is_untouched:
                reprocessed_tokens.append(item)

        return reprocessed_tokens

    @staticmethod
    def _is_complex_abbreviations(index, tokens):
        if index + 1 < len(tokens):
            if tokens[index + 1]['token'] is '.':
                return True
        return False

    @staticmethod
    def _abbreviation_map(token, is_cp=False):
        token['type'] = 'COMPLEX_ABBREVIATION' if is_cp else 'ABBREVIATION'

    @staticmethod
    def _complex_punctuation_map(token_map):
        return {'token': ''.join(token_map), 'type': 'COMPLEX_PUNCTUATION'}