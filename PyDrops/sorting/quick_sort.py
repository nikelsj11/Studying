#-*- coding: utf-8 -*-


def quick_sort(array):
    """Быстрая сортировка (Quick sort)

    Простой алгоритм быстрой сортировки.
    Средняя сложность: O(n*log(n))

    -array - список который требуется отсортировать

    ~На выход отсортированный список.
    """
    if len(array) <= 1:
        return array
    pivot = array[0]
    left, right = [], []
    for item in array[1:]:
        if item < pivot:
            left.append(item)
        else:
            right.append(item)
    return quick_sort(left)+[pivot]+quick_sort(right)




