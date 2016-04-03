# coding=utf-8


class Segmenter(object):
    def __init__(self, splitter=['.', '!', '?']):
        self.splitter = splitter

    def make_segmented(self, tokens):
        result = [[]]

        for token in tokens:
            result[-1].append(token)
            if token['type'] is 'PUNCTUATION' and token['token'] in self.splitter:
                result.append([])


        return result
