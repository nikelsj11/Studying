#-*- coding: utf-8 -*-


def cocktail_sort(array):
    """Шейкерная сортировка (Cocktail sort)

    Оптимизированный алгоритм шейкерной сортировки.
    Худшая сложность: O(n**2)

    -array - список который требуется отсортировать

    ~На выход отсортированный список.
    """
    right_bound, left_bound, swapped = len(array)-1, 0, False

    while not swapped:
        swapped = False
        for item in range(right_bound, left_bound, -1):
            if array[item] < array[item-1]:
                array[item], array[item-1] = array[item-1], array[item]
                swapped = True
        left_bound += 1
        if not swapped:
            break
        swapped = False
        for item in range(left_bound, right_bound, 1):
            if array[item] > array[item+1]:
                array[item], array[item+1] = array[item+1], array[item]
                swapped = True
        right_bound -= 1
    return array
