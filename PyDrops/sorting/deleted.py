#-*- coding: utf-8 -*-


def swap(arr, frm, to):
    """Функция меняющая 2 элемента местами в списке."""
    arr[frm], arr[to] = arr[to], arr[frm]


def select_bubble_sort(array):
    """Объединенный алгоритм сортировки пузырьком и сортировки выбором

    Сортируем пузырьком от элемента i, попутно находя наименьший элемент и ставим на место i, повторяем далее от i+1
    из плюсов - мы не проходим пузырьком весь массив на всех итерациях, проходим только от i, если небыло сделано
    ни одной перестановки пузырьком, завершаем работу.

    -array - список который требуеться отсортировать.

    ~На выход отсортированный список.
    """
    for now_num, now_item in enumerate(array):
        end = True
        min_num = now_num
        for num in range(now_num, len(array)-now_num-1):
            if array[num+1] < array[num]:
                swap(array, num, num+1)
                end = False
            if array[min_num] > array[num]:
                min_num = num
        if end:
            return array
        if now_num != min_num:
            swap(array, min_num, now_num)


#Just For Fun Быстрая сортировка в 4 строки)
_left = lambda arr, mid: filter(lambda item: item <= mid, arr)
_right = lambda arr, mid: filter(lambda item: item > mid, arr)
_quick_sort_ = lambda arr: arr if len(arr) <= 1 else _do_sort(arr, arr.pop(len(arr)/2))
_do_sort = lambda arr, mid: _quick_sort_(_left(arr, mid)) + [mid] + _quick_sort_(_right(arr, mid))


#Just For Fun Cортировка Слиянием в 4 строки)
#функция отвечает за рекурсивное слияние 2х списков, в результате получаем список отсортированый по возрастанию значений
def merge(right, left, result):
    result.append((left if left[0] < right[0] else right).pop(0))
    return merge(right=right, left=left, result=result) if left and right else result+left+right


#сама функция сортировки слиянием, рекурсивно разбивает список на 2 подсписка и отдает их сама себе и так пока не дойдет
#до списков длинною в единицу, потом поочередно каждая пара списков отдается на слияние.
merge_sort = (lambda arr: arr if len(arr) == 1 else merge(merge_sort(arr[len(arr)/2:]),
                                                          merge_sort(arr[:len(arr)/2]), []))


#рекурсивный вариант сортировки выбором=================================================================================
def select_sort_recursive(arr, frm_index=0):
    if frm_index != (len(arr)-1):
        swap(arr, get_min_element_index(arr, frm_index), frm_index)
        select_sort_recursive(arr, frm_index+1)

#рекурсивный поиск наименьшего элемента
def get_min_element_index(arr, frm_index):
    min_index = frm_index-1
    if frm_index < len(arr)-1:
        min_index = get_min_element_index(arr, frm_index+1)
    if arr[min_index] > arr[frm_index]:
        min_index = frm_index
    return min_index


#пирамидальная сортировка
def heap_sort_(arr):
    length = len(arr)
    get_max = lambda first, second: first if arr[first] > arr[second] else second
    swap_max = lambda frm, to: (to, (arr[to] > arr[frm] and swap(arr, frm, to)))
    down_heap = (lambda frm, to: down_heap(swap_max(frm, get_max(frm*2+1, frm*2+2) if frm*2+2 < to else frm*2+1)[0], to)
                 if frm*2+1 < to else None)
    for item in range((length/2) - 1, -1, -1):
        down_heap(item, length)
    for item in range(length-1, 0, -1):
        swap_max(item, 0), down_heap(0, item)
    return arr