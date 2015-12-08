#-*- coding: utf-8 -*-


def select_sort(array):
    """Сортировка выбором (Selection sort)

    Простой алгоритм сортировки выбором.
    Средняя сложность: O(n**2)

    -array - список который требуется отсортировать

    ~На выход отсортированный список.
    """
    arr_len = len(array)
    for now_index in range(arr_len):
        min_index = now_index
        for right_index in range(now_index+1, arr_len):
            if array[min_index] > array[right_index]:
                min_index = right_index
        array[now_index], array[min_index] = array[min_index], array[now_index]
    return array
