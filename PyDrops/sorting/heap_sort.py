#-*- coding: utf-8 -*-


def down_heap(array, _from, _to):
        left, right = _from*2+1, _from*2+2
        if left < _to and array[left] > array[_from]:
            greatest = left
        else:
            greatest = _from
        if right < _to and array[right] > array[greatest]:
            greatest = right
        if _from != greatest:
            array[greatest], array[_from] = array[_from], array[greatest]
            down_heap(array, greatest, _to)


def heap_sort(array):
    """Пирамидальная сортировка (Heap sort)

    Простой алгоритм пирамидальной сортировки.
    Сложность: O(n*log(n))

    -array - список который требуется отсортировать

    ~На выход отсортированный список.
    """
    array_length = len(array)

    for index in range((array_length/2)-1, -1, -1):
        down_heap(array, index, array_length)
    for index in range(array_length-1, 0, -1):
        array[index], array[0] = array[0], array[index]
        down_heap(array, 0, index)
    return array


print heap_sort([5,1,9,4,2,9,2,4,8,3,6,3,2,1,1,2,3-3999,0,0,0,0,0,0,0,7,6,5,4,3,2,1,15,6,8,9,0,-1000000])