#!/usr/bin/python
# -*- coding: UTF-8 -*-

# восстановление свойств узла бинарной кучи
def _heap_siftdown(lst, start, end):
    root = start
    while True:
        child = root * 2 + 1
        if child > end:
            break
        if child + 1 <= end and lst[child] < lst[child + 1]:
            child += 1
        if lst[root] < lst[child]:
            lst[root], lst[child] = lst[child], lst[root]
            root = child
        else:
            break


# перестройка списка в бинарную кучу
def _heap_heapify(lst):
    for start in range((len(lst) - 2) / 2, -1, -1):
        _heap_siftdown(lst, start, len(lst) - 1)
    return lst


# итератор - посути пошаговый heapsort
def _heap_iter_max(lst):
    for end in range(len(lst) - 1, 0, -1):
        yield lst[0]
        lst[0] = lst.pop()
        _heap_siftdown(lst, 0, end - 1)
    if lst:
        yield lst[0]