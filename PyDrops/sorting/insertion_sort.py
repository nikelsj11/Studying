#-*- coding: utf-8 -*-


def insert_sort(array):
    """Сортировка вставками (Insertion sort)

    Оптимизированный алгоритм сортировки вставками.
    Средняя сложность: O(n**2)

    -array - список который требуется отсортировать

    ~На выход отсортированный список.
    """
    array.insert(0, None)
    for now_num in range(1, len(array)):
        search_for_num = now_num - 1
        while array[search_for_num] > array[now_num]:
            search_for_num -= 1
        array.insert(search_for_num+1, array.pop(now_num))
    return array[1:]
