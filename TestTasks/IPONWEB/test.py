#!/usr/bin/python
# -*- coding: UTF-8 -*-
from random import randint
from creatives_selector import creatives_selector as tf
from _binary_heap import _heap_heapify, _heap_iter_max
import unittest


# [[1, 1, '1'], ...] => [{'advertiser_id': 1, 'price': 1, 'country': '1'},...]
def _input_producer(clst):
    return [{'advertiser_id': item[0], 'price': item[1], 'country': item[2]} for item in clst]


class TestCreativeSelector(unittest.TestCase):
    '''  Тестирование creatives_selector  '''

    # случаи с некорректным вводом
    def test_empty_creatives(self):
        self.assertIsNone(tf([], 0))
        self.assertIsNone(tf([], 5))
        self.assertIsNone(tf([], 5, 'R'))
        self.assertIsNone(tf([], 0, 'R'))

    # однозначность выбора - простые случаи с детерминированным исходом
    def test_unequivocal_choice(self):
        test_u_c = _input_producer([
            [1, 1, 'R'],
            [2, 2, 'I'],
            [3, 3, 'T']
        ])

        test_u_c_R = tf(test_u_c, 1, 'R')
        test_u_c_I = tf(test_u_c, 1, 'I')
        test_u_c_T = tf(test_u_c, 1, 'T')

        self.assertEqual(len(test_u_c_R), 1)
        self.assertEqual(len(test_u_c_R), 1)
        self.assertEqual(len(test_u_c_R), 1)

        self.assertDictEqual(test_u_c_R[0], _input_producer([[1, 1, 'R']])[0])
        self.assertDictEqual(test_u_c_I[0], _input_producer([[2, 2, 'I']])[0])
        self.assertDictEqual(test_u_c_T[0], _input_producer([[3, 3, 'T']])[0])

    # случаи когда невозможно сделать выбор основываясь на полученых данных
    def test_insufficient_information(self):
        test_i_i = _input_producer([
            [1, 1, 'R'],
            [2, 2, 'I'],
            [3, 3, 'T']
        ])

        self.assertIsNone(tf(test_i_i, 2, 'R'))
        self.assertIsNone(tf(test_i_i, 2, 'I'))
        self.assertIsNone(tf(test_i_i, 2, 'T'))

        test_i_i = _input_producer([
            [1, 1, 'R'],
            [2, 2, 'R'],
            [3, 3, 'I']
        ])

        self.assertIsNone(tf(test_i_i, 3, 'R'))

        test_i_i = _input_producer([
            [1, 1, 'I'],
            [2, 2, 'I'],
            [3, 3, 'I']
        ])

        self.assertIsNone(tf(test_i_i, 1, 'R'))

    # все advertiser_id в результатирующей выборке должны быть уникальны - 1 cond.
    def test_unique_advertiser_ids(self):
        test_u_a_i = _input_producer([
            [1, 5, 'R'],
            [1, 5, 'R'],
            [2, 4, 'R'],
            [2, 4, 'R'],
            [3, 3, 'R'],
            [3, 3, 'R']
        ])

        test_pull = tf(test_u_a_i, 3, 'R')

        test_ids_pull = []

        for item in test_pull:
            ids = item['advertiser_id']
            self.assertNotIn(ids, test_ids_pull)
            test_ids_pull.append(ids)

    # результатиющая выборка должна содержать только сущности с установленным country
    # либо вообще без него - 2 cond.
    def test_country_correctness(self):
        test_c_c = _input_producer([
            [1, 5, 'T'],
            [1, 5, 'R'],
            [2, 4, 'R'],
            [2, 4, 'I'],
            [2, 3, 'R'],
            [3, 3, None],
            [4, 1, None]
        ])

        test_pull = tf(test_c_c, 4, 'R')

        self.assertEqual(len(test_pull), 4)

        for item in test_pull:
            country = item['country']
            self.assertTrue(country is None or country == 'R')

    # произвольность выбора - 3 cond.
    def test_ambiguity_choice(self):
        test_a_c = _input_producer([
            [1, 2, 'R'],
            [2, 2, 'R'],
            [3, 2, 'R']
        ])

        test_pull = [tf(test_a_c, 2, 'R') for _ in range(100)]

        test_pull_1 = [item[0]['advertiser_id'] == 1 for item in test_pull]
        test_pull_2 = [item[0]['advertiser_id'] == 2 for item in test_pull]
        test_pull_3 = [item[0]['advertiser_id'] == 3 for item in test_pull]

        self.assertFalse(all(test_pull_1))
        self.assertFalse(all(test_pull_2))
        self.assertFalse(all(test_pull_3))


class TestBinaryHeap(unittest.TestCase):
    '''  Тестирование _heap_iter_max  '''

    # тестируем сортировку методом последовательного извлечения максимальных элементов списка
    def test_max_heap(self):

        test_m_h = [randint(0, 30) for _ in range(100)]

        test_pull = []

        for max_item in _heap_iter_max(_heap_heapify(list(test_m_h))):
            test_pull.append(max_item)

        test_pull.reverse()

        test_m_h = sorted(test_m_h)

        self.assertListEqual(test_pull, test_m_h)



if __name__ == '__main__':
    unittest.main()
