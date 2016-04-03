##Отчет по лабораторной работе №1
&nbsp; | &nbsp;
 --------------------- | ---------------------------------- 
**Предмет**            | *Методы интеллектуального поиска*   
**Выполнил**           | *Красюк Никита*                    
**Группа**             | *НК-401*                           
**Студенческий билет** | *103111130*  
                      
---------------------------------------------------------------------
### Постановка задачи
1. Реализовать  функцию  токенизации  текста  на  Python:  разбиение  текста  на  слова, 
разделители и знаки препинания. Функция должна работать для текстов на русском и 
на  английском  языке.  Знаки  пунктуации  должны  распознаваться  отдельными 
токенами. Несколько  подряд  идущих знаков  пунктуации  должны  распознаваться  как 
единый токен. Продемонстрировать работу функции на 3 примерах для каждого языка. 
Необходимо  также  реализовать  распечатку  токенов  с  указанием  их  типа:  слово  или 
пунктуация.  
2. Реализовать функцию разбиения  списка  токенов на предложения. Процедура должна 
работать  для  русскоязычных  и  англоязычных  текстов.  Реализовать  распознавание 
аббревиатур  и  сокращений  с  точкой  (не  менее  4  аббревиатур  и  4  сокращений). 
Функция  разбиения  текста  на  предложения  должна  правильно  обрабатывать 
предложения  с  аббревиатурами  и  сокращениями.  Продемонстрировать  работу 
процедуры на 3 примерах для каждого языка.  
3. Реализовать  функцию  распознавания  в  тексте  типов  объектов,  которые  указаны  в 
Вашем варианте. Необходимо продемонстрировать работу функции на 5 примерах.

**Вариант №4:**

ФИО  на  русском  и  на  английском,  с  приставками (госп.,  сэр, sir,  г­жа,  д.т.н.  и  др.).
Распознавание количественных выражений и их типов (500 кг., м., м/с, 50 км/ч и др.) с 
нормализацией (например, необходимо преобразовать 50  г в 0,05 кг и 5 т в 5000 кг). 

---------------------------------------------------------------------
### Ход решения
В ходе решения задачи было разработано 5 классов в пакете ```simple_tokenizer```:

```python2.7
from simple_tokenizer import Tokenizer, Grouper, Segmenter
from simple_tokenizer import NameChecker, MeasureNormalizer
```

- Tokenizer - выполняет базовое разбиение на токены (слова и пунктуация).
- Grouper - групирует сложную пунктуацию, абревиатуры, сокращения + Имена с приставками (```NameChecker```) 
и количественные выражения (```MeasureNormalizer```). 
- Segmenter - Разбивает токены по предложениям.

Для базового функционала были написаны юниттесты - ```test.py```, эксперементы можно проводить в ```custom_test.py```. 

---------------------------------------------------------------------
#### Tokenizer

Выполняет базовое разбиение на 2 класса - *PUNCTUATION*, *WORD*. Пример использования:

```python2.7
text = 'Yesterday, all my troubles seemed so far away. !!!'
tokens = Tokenizer().tokenize(text)
```

Результат:

```Python2.7
[{'is_nd': False, 'token': 'Yesterday', 'type': 'WORD'},
 {'is_nd': False, 'token': ',', 'type': 'PUNCTUATION'},
 {'is_nd': True, 'token': 'all', 'type': 'WORD'},
 {'is_nd': True, 'token': 'my', 'type': 'WORD'},
 {'is_nd': True, 'token': 'troubles', 'type': 'WORD'},
 {'is_nd': True, 'token': 'seemed', 'type': 'WORD'},
 {'is_nd': True, 'token': 'so', 'type': 'WORD'},
 {'is_nd': True, 'token': 'far', 'type': 'WORD'},
 {'is_nd': False, 'token': 'away', 'type': 'WORD'},
 {'is_nd': False, 'token': '.', 'type': 'PUNCTUATION'},
 {'is_nd': False, 'token': '!', 'type': 'PUNCTUATION'},
 {'is_nd': False, 'token': '!', 'type': 'PUNCTUATION'},
 {'is_nd': False, 'token': '!', 'type': 'PUNCTUATION'}]
```

При инициализации можно определить что требуется считать за пунктуацию и разделители с помощью параметров -
```delimiter``` и ```punctuation```, что позволит работать с практически любым языком:

```Python2.7
text = '_______!走_进_福!_建_____'
tokens = Tokenizer(punctuation=re.compile(r'[!]'), delimiter=re.compile(r'[_]')).tokenize(text)
```

Результат:

```Python2.7
[{'is_nd': False, 'token': '!', 'type': 'PUNCTUATION'},
 {'is_nd': True, 'token': '\xe8\xb5\xb0', 'type': 'WORD'},
 {'is_nd': True, 'token': '\xe8\xbf\x9b', 'type': 'WORD'},
 {'is_nd': False, 'token': '\xe7\xa6\x8f', 'type': 'WORD'},
 {'is_nd': False, 'token': '!', 'type': 'PUNCTUATION'},
 {'is_nd': True, 'token': '\xe5\xbb\xba', 'type': 'WORD'}]
```

---------------------------------------------------------------------
#### Grouper

Grouper умеет:

- сворачивать комплексную пунктуация например смайлики (:), ;)), многоточие и многое другое. Допустимые значения 
задаются списком при инициализации через параметр ```cp_maps```.  
- определять сокращения, задаются списком через параметр ```cp_abbreviations```.  
- определять аббревиатуры, задаются списком через ```abbreviations```.   
- использовать кастомные гроуперы, список классов подаваемый в параметр ```custom_maps```.    

Было разработанно 2 кастомных гроупера: *NameChecker*, *MeasureNormalizer*.

Пример использования.


```Python2.7
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
```

Результат:

```Python2.7
[{'container': {'name': ['Samon',
                         'de-Citten',
                         'don',
                         'Pomidor',
                         'SanEdnes',
                         "la'Fam",
                         'Monceporskiy',
                         "la'Pompadur"],
                'title': 'mr'},
  'grouper': 'NameChecker',
  'type': 'GROUP'},
 {'is_nd': True, 'token': 'has', 'type': 'WORD'},
 {'is_nd': True, 'token': 'work', 'type': 'WORD'},
 {'is_nd': True, 'token': 'in', 'type': 'WORD'},
 {'is_nd': True, 'token': 'FBI', 'type': 'ABBREVIATION'},
 {'is_nd': False, 'token': 'corp', 'type': 'COMPLEX_ABBREVIATION'},
 {'is_nd': True, 'token': 'and', 'type': 'WORD'},
 {'is_nd': True, 'token': 'his', 'type': 'WORD'},
 {'is_nd': True, 'token': 'leg', 'type': 'WORD'},
 {'is_nd': True, 'token': 'is', 'type': 'WORD'},
 {'is_nd': True, 'token': 'almost', 'type': 'WORD'},
 {'container': {'measure': 'kilogram',
                'normalized_from': 'ton',
                'value': 500.0},
  'grouper': 'MeasureNormalizer',
  'type': 'GROUP'},
 {'token': '...', 'type': 'COMPLEX_PUNCTUATION'},
 {'is_nd': False, 'token': '.', 'type': 'PUNCTUATION'},
 {'is_nd': True, 'token': "That'a", 'type': 'WORD'},
 {'is_nd': False, 'token': 'fine', 'type': 'WORD'},
 {'token': '!!', 'type': 'COMPLEX_PUNCTUATION'},
 {'is_nd': False, 'token': '!', 'type': 'PUNCTUATION'},
 {'is_nd': True, 'token': 'my', 'type': 'WORD'},
 {'is_nd': True, 'token': 'email', 'type': 'WORD'},
 {'is_nd': True, 'token': 'is', 'type': 'WORD'},
 {'is_nd': True, 'token': 'nikelsj11@gmail.com', 'type': 'WORD'},
 {'token': ':)', 'type': 'COMPLEX_PUNCTUATION'},
 {'token': ';)', 'type': 'COMPLEX_PUNCTUATION'},
 {'is_nd': True, 'token': 'Where', 'type': 'WORD'},
 {'is_nd': True, 'token': 'is', 'type': 'WORD'},
 {'is_nd': False, 'token': 'MIT', 'type': 'ABBREVIATION'},
 {'is_nd': False, 'token': '.', 'type': 'PUNCTUATION'},
 {'is_nd': False, 'token': 'Cha-Cha-Cha', 'type': 'WORD'},
 {'token': '!!', 'type': 'COMPLEX_PUNCTUATION'},
 {'container': {'measure': 'meter',
                'normalized_from': 'kilometer',
                'value': 555.4599999999999},
  'grouper': 'MeasureNormalizer',
  'type': 'GROUP'}]
```



---------------------------------------------------------------------
#### Segmenter

Обладает базовой функциональностью разбивает токены на предложения, при инициализации можно указать, что считать за 
окончание предложения:

```Python2.7
text = '1! 2! 3! 4! 5! 6!'
tokens = Tokenizer().tokenize(text)
tokens = Segmenter().make_segmented(tokens)
```

Результат:

```Python2.7
[[{'is_nd': False, 'token': '1', 'type': 'WORD'}],
 [{'is_nd': False, 'token': '2', 'type': 'WORD'}],
 [{'is_nd': False, 'token': '3', 'type': 'WORD'}],
 [{'is_nd': False, 'token': '4', 'type': 'WORD'}],
 [{'is_nd': False, 'token': '5', 'type': 'WORD'}],
 [{'is_nd': False, 'token': '6', 'type': 'WORD'}],
]
```

*Т.к. я сделал очень расширяемую конструкцию базово токенайзер умеет работать с английским, по даже на 
ините можно задать любые параметры и работать с любым языком.*
