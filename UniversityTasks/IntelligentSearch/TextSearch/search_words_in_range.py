# -*- coding: utf-8 -*-
import os
import sys
from colorama import Fore, Back, Style, init
import time

init(autoreset=True)

# instance to simple_tokenizer
sys.path.append(os.path.dirname(os.getcwd() + '/../TextTokenization/simple_tokenizer'))
from simple_tokenizer import Tokenizer, Segmenter


def log(message, color=Fore.WHITE, limiter=False):
    print('%s%sLOG: %s' % (limiter and '-' * limiter or '', color, message))


def search(text, search_query, max_distance, indexer):
    assert max_distance > 0 and search_query

    if not text:
        return None

    segmented_text = Segmenter().make_segmented(Tokenizer().tokenize(text))

    query_counter = list(search_query)

    position, result_scopes, scope, margin = 0, list(), list(), None

    for segment in segmented_text:
        for item_holder in segment:
            if item_holder['type'] is 'WORD':
                if indexer:
                    indexer(item_holder['token'])
                position += 1
                if item_holder['token'] in search_query:
                    if item_holder['token'] in query_counter:
                        query_counter.remove(item_holder['token'])
                    scope.append([position, item_holder['token'], segment])
                    if not query_counter:
                        result_scopes.append(scope)
                        query_counter = list(search_query)
                        scope = list()
                    margin = max_distance
                if not (margin is None):
                    margin -= 1
                    if margin < 0:
                        scope = list()
                        margin = None
                item_holder['position'] = position

    if not result_scopes:
        return None

    min_len, min_scope = float('Inf'), None

    for scope in result_scopes:
        scope_len = len(scope)
        if scope_len < min_len:
            min_len = scope_len
            min_scope = scope

    query_counter, scope = list(search_query), list()

    for item_holder in reversed(min_scope):
        token = item_holder[1]
        if token in query_counter:
            query_counter.remove(token)
        scope.insert(0, item_holder)
        if not query_counter:
            return scope


def get_invariant_indexer():
    index_scope = {}

    def get_file_indexer(file_name_in):
        def _index(word):
            word_in = u'%s' % word
            word_index_scope = index_scope.get(word_in)
            if word_index_scope is None:
                index_scope[word_in] = [file_name_in]
            elif not (file_name_in in word_index_scope):
                index_scope[word_in].append(file_name_in)
        return _index

    def has_intersection(file_name_in, words):
        for word in words:
            index_holder = index_scope.get(word)
            if index_holder is None:
                return False

            if not (file_name_in in index_holder):
                return False

        return True

    return {
        'get_file_indexer': get_file_indexer,
        'has_intersection': has_intersection,
        '_A': index_scope
    }


if __name__ == "__main__":
    is_indexed = False
    invariant_indexer = get_invariant_indexer()
    while True:
        print Back.GREEN + u'Начать поиск (Д/н)?'
        print Back.RED + u'-> ',
        answer = raw_input().decode('utf8').lower()
        if answer == u'н':
            break
        if not (answer == u'д'):
            continue

        print Back.GREEN + u'Максимальное расстояние между 2мя словами из поискового запроса:'
        print Back.RED + u'-> ',
        max_len = int(input())

        print Back.GREEN + u'Слова поискового запроса (через пробел):'
        print Back.RED + u'-> ',
        words = raw_input().decode('utf8').split(' ')

        print

        log(u'Запрос состоит из %d слов, максимальное расстояние между словами = %d' % (len(words), max_len))

        startTime = time.time()
        raw_files = os.listdir('raw')

        log(u'Загружено %s файлов для поиска' % len(raw_files))

        print

        log(u'Начинаем поиск:')

        result_counter = 1

        for file_name in raw_files:
            indexer = None
            if not is_indexed:
                indexer = invariant_indexer['get_file_indexer'](file_name)
            elif not invariant_indexer['has_intersection'](file_name, words):
                continue
            with open('raw/%s' % file_name) as file_instance:
                raw = file_instance.read().decode('utf8').split('\n')
                article_name = raw[0].strip()
                results = search(' '.join(raw[2:]), words, max_len, indexer)

                if results:
                    log(u'Результат = %d' % result_counter, color=Fore.RED, limiter=5)
                    log(u'Поиск по файлу: %s' % file_name, color=Fore.CYAN, limiter=2)
                    log(u'%s' % article_name, color=Fore.YELLOW, limiter=2)

                    for result in results:
                        output = []
                        for item in result[2]:
                            output.append(
                                Back.GREEN + "<%s>" % item['position'] + item['token'] +
                                Back.RESET if item.get('position') == result[0] else item['token']
                            )

                        print u'%s%s%s %s' % (
                            Fore.GREEN,
                            '=>',
                            Fore.RESET,
                            ' '.join(output)
                        )

                    print

                    result_counter += 1
        is_indexed = True

        log("Длительность поиска: {:.3f} сек.".format(time.time() - startTime), color=Fore.YELLOW, limiter=5)

        print

    print Style.RESET_ALL

    # for key in invariant_indexer['_A'].keys():
    #     files = invariant_indexer['_A'][key]
    #
    #     print "\n --- ", key
    #     for file_instance in files:
    #         print "\t\t > ", file_instance
