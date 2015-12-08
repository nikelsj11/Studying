#-*- coding: utf-8 -*-


def bubble_sort(array):
    """Сортировка пузырьком (Bubble sort)

    Оптимизированный алгоритм сортировки пузырьком.
    Сложность: О(n**2)

    -array - список который требуется отсортировать.

    ~На выход отсортированный список.
    """
    array_len = len(array)
    for already_sorted in range(array_len):
        array_sorted = True
        for num in range(1, array_len-already_sorted):
            if array[num] < array[num-1]:
                array[num], array[num-1] = array[num-1], array[num]
                array_sorted = False
        if array_sorted:
            return array



