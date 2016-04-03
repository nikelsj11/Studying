# coding=utf-8
import re
import string


class Tokenizer(object):
    _DELIMITER = re.compile("\s")
    _PUNCTUATION = re.compile("[%s]" % re.escape(string.punctuation))

    def __init__(self, delimiter=_DELIMITER, punctuation=_PUNCTUATION):
        self.delimiter = delimiter
        self.punctuation = punctuation

    def tokenize(self, text):
        return self._base_wrap(text)

    def _base_wrap(self, text):
        wrap = lambda lt, ltt: {'token': lt, 'type': ltt, 'is_nd': now_class is 'DELIMITER'}
        text += ' '
        tokens, token = [], ''
        index, length = -1, len(text) - 1
        next_atom, next_class = None, None

        while True:
            now_atom = next_atom
            now_class = next_class

            try:
                if index != length:
                    next_atom = text[index + 1]
                    next_class = self._get_class(next_atom)
            except IndexError:
                return tokens

            if now_class is 'PUNCTUATION':
                if not (token and next_class is 'LETTER'):
                    if token:
                        self._add_token([wrap(token, 'WORD')], tokens)
                    token = self._add_token([wrap(now_atom, 'PUNCTUATION')], tokens)
                else:
                    token += now_atom
            elif now_class is 'LETTER':
                token += now_atom
            elif token:
                token = self._add_token([wrap(token, 'WORD')], tokens)

            index += 1

    def _get_class(self, atom):
        if not atom:
            return
        if re.match(self.delimiter, atom):
            return 'DELIMITER'
        if re.match(self.punctuation, atom):
            return 'PUNCTUATION'
        return 'LETTER'

    @staticmethod
    def _add_token(tokens, result):
        [result.append(token) for token in tokens]
        return ''

