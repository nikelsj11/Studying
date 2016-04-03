#-*- coding: utf-8 -*-
from random import shuffle


def _is_not_sorted(array):
    """Функция проверяет отсортирован ли массив"""
    return any(array[i] < array[i-1] for i in xrange(1, len(array)))


def bogo_sort(array):
    """Bogosort

    Неэффективный алгоритм сортировки. Случайным образом перемешивает массив и проверяет отсортирован ли он.
    Средняя сложность: О(n*n!)

    -array - список который требуеться отсортировать.

    ~На выход отсортированный список.
    """
    while _is_not_sorted(array):
        shuffle(array)
    return array