# -*- coding: utf-8 -*-
from simple_tokenizer import Tokenizer, Grouper
import unittest
import string
import pprint

WORD, PUNCTUATION, C_PUNCTUATION = 'WORD', 'PUNCTUATION', 'COMPLEX_PUNCTUATION'
ABBREVIATION, C_ABBREVIATION = 'ABBREVIATION', 'COMPLEX_ABBREVIATION'


class TestStringMethods(unittest.TestCase):
    def test_base_tokenizer_easy(self):
        test = "ONE two milky way. ..."
        result = Tokenizer().tokenize(test)
        exception = ['ONE', 'two', 'milky', 'way', '.', '.', '.', '.']
        self.assertTrue(all(map(lambda a, b: a['token'] == b, result, exception)))

    def test_base_tokenizer_complex_test(self):
        test = "Sh.asha goes. 'to' the .river. nikelsj11@gmail.com"
        result = Tokenizer().tokenize(test)
        exception = ['Sh.asha', 'goes', '.', '\'', 'to', '\'', 'the', '.', 'river', '.', 'nikelsj11@gmail.com']
        self.assertTrue(all(map(lambda a, b: a['token'] == b, result, exception)))

    def test_base_tokenizer_punctuation(self):
        tokenizer = Tokenizer()
        for punctuation in string.punctuation:
            test = "%sWORD%s WO%sRD" % ((punctuation,) * 3)
            result = tokenizer.tokenize(test)
            exception = [punctuation, 'WORD', punctuation, 'WO%sRD' % punctuation]
            self.assertTrue(all(map(lambda a, b: a['token'] == b, result, exception)))

    def test_base_tokenizer_empty_string(self):
        tokenizer = Tokenizer()
        for test in [" ", "", "\n", "\t", "  \n \t \n   \n \t \t\t\t \n\n\n    "]:
            result = tokenizer.tokenize(test)
            self.assertTrue(0 == len(result))

    def test_base_tokenizer_english_text(self):
        test = "Palace of Westminster in London is often called Big Ben."
        result = Tokenizer().tokenize(test)
        exception = ['Palace', 'of', 'Westminster', 'in', 'London', 'is', 'often', 'called', 'Big', 'Ben', '.']
        self.assertTrue(all(map(lambda a, b: a['token'] == b, result, exception)))

    def test_base_tokenizer_spanish_text(self):
        test = "Universität oder Fachhochschule studieren möchten."
        result = Tokenizer().tokenize(test)
        exception = ['Universität', 'oder', 'Fachhochschule', 'studieren', 'möchten', '.']
        self.assertTrue(all(map(lambda a, b: a['token'] == b, result, exception)))

    def test_base_tokenizer_types(self):
        test = "word, wo.rd, funnel_text.? email@a.com"
        result = Tokenizer().tokenize(test)

        exception = [WORD, PUNCTUATION, WORD, PUNCTUATION, WORD, PUNCTUATION, PUNCTUATION, WORD]
        self.assertTrue(all(map(lambda a, b: a['type'] == b, result, exception)))

    def test_base_grouper_complex_punctuation(self):
        test = "Some ... Where... I!? You?!"
        tokens = Tokenizer().tokenize(test)
        result = Grouper(cp_maps=[['.', '.', '.'], ['?', '!'], ['!', '?']]).group(tokens)
        pprint.pprint(result)
        exception_tokens = ['Some', '...', 'Where', '...', 'I', '!?', 'You', '?!']
        exception_types = [WORD, C_PUNCTUATION, WORD, C_PUNCTUATION, WORD, C_PUNCTUATION, WORD, C_PUNCTUATION]
        self.assertTrue(all(map(lambda a, b: a['token'] == b, result, exception_tokens)))
        self.assertTrue(all(map(lambda a, b: a['type'] == b, result, exception_types)))

    def test_base_grouper_complex_abbreviation(self):
        test = "You me ... etc. ltd. BMW we... ?!FBI!? skp.."
        tokens = Tokenizer().tokenize(test)
        result = Grouper(
            abbreviations=['IAB', 'BMW', 'FBI'],
            cp_abbreviations=['etc', 'ltd', 'skp'],
            cp_maps=[['.', '.', '.'], ['?', '!'], ['!', '?']],
        ).group(tokens)
        pprint.pprint(result)
        exception_tokens = ['You', 'me', '...', 'etc', 'ltd', 'BMW', 'we', '...', '?!', 'FBI', '!?', 'skp', '.']
        exception_types = [
            WORD,
            WORD,
            C_PUNCTUATION,
            C_ABBREVIATION,
            C_ABBREVIATION,
            ABBREVIATION,
            WORD,
            C_PUNCTUATION,
            C_PUNCTUATION,
            ABBREVIATION,
            C_PUNCTUATION,
            C_ABBREVIATION,
            PUNCTUATION
        ]
        self.assertTrue(all(map(lambda a, b: a['token'] == b, result, exception_tokens)))
        self.assertTrue(all(map(lambda a, b: a['type'] == b, result, exception_types)))


if __name__ == '__main__':
    unittest.main()
