#-*- coding: utf-8 -*-
import time


def merge(right, left):
    result = []
    while left and right:
        result.append((left if left[0] < right[0] else right).pop(0))
    return result+left+right


def merge_sort(array):
    """Сортировка слиянием (Merge sort)

    Простой алгоритм сортировки слиянием.
    Средняя сложность: O(n*log(n))

    -array - список который требуется отсортировать

    ~На выход отсортированный список.
    """
    array_len = len(array)
    if array_len <= 1:
        return array
    middle = array_len/2
    return merge(merge_sort(array[middle:]), merge_sort(array[:middle]))


