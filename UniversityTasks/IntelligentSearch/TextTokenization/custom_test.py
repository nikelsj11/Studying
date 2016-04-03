# coding=utf-8
import pprint
from simple_tokenizer import Tokenizer, Grouper, Segmenter
from simple_tokenizer import NameChecker, MeasureNormalizer

text = '''
Mr. Samon de-Citten don Pomidor SanEdnes la'Fam Monceporskiy la'Pompadur
has work in FBI corp. and his leg is almost 0.5 t. ...That'a fine!!!
my email is nikelsj11@gmail.com :) ;) Where is MIT. Cha-Cha-Cha!! 0.55546
kilometer

'''

tokens = Tokenizer().tokenize(text)

print "\n===TOKENS\n\n"
pprint.pprint(tokens)

groups = Grouper(
    abbreviations=['FBI', 'MIT'],
    cp_abbreviations=['corp', 'etc'],
    cp_maps=[['.', '.', '.'], ['!', '!'], [':', ')'], [';', ')']],
    custom_maps=[NameChecker, MeasureNormalizer]
).group(tokens)

print "\n===GROUPS\n\n"
pprint.pprint(groups)

segmented = Segmenter(splitter='.').make_segmented(groups)

print "\n===SEGMENTS\n\n"
pprint.pprint(segmented)
