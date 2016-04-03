#-*- coding: utf-8 -*-


def sedgwick_increment(length):
    """
    Последовательность Седжвика.

    -length - необходимое количество членов последовательности.

    ~На выход список последовательности длин приращения.
    """
    kof1 = kof2 = kof3 = 1
    increment = -1
    func_value = []
    while 1:
        increment += 1
        if increment % 2:
            func_value.append(8*kof1 - 6*kof2 + 1)
        else:
            func_value.append(9*kof1 - 9*kof3 + 1)
            kof2 *= 2
            kof3 *= 2
        kof1 *= 2
        if 3*func_value[increment] > length:
            return func_value[:-1]


def hibbard_increment(length, increment=0, inc_values=list()):
    """
    Последовательность Хиббарда.

    -length - необходимое количество членов последовательности.

    ~На выход список последовательности длин приращения.
    """
    inc_values.append(pow(2, increment+1)-1)
    return (inc_values[:-1] if inc_values[increment] > length else
            hibbard_increment(length, increment=increment+1, inc_values=inc_values))


def fibonacci_increment(length, increment=1, inc_values=list([1, 2])):
    """
    Последовательность основанная на числах Фибоначчи.

    -length - необходимое количество членов последовательности.

    ~На выход список последовательности длин приращения.
    """
    inc_values.append(inc_values[increment-1]+inc_values[increment])
    return (inc_values[:-2] if 3*inc_values[increment] > length else
            fibonacci_increment(length, increment=increment+1, inc_values=inc_values))


def marcin_tsiuri_increment(length):
    """
    Эмпирическая последовательность Марцина Циура (A102549), применяется для массивов длинны <4000.

    -length - необходимое количество членов последовательности.

    ~На выход список последовательности длин приращения.
    """
    inc_val = [1, 4, 10, 23, 57, 132, 301, 701, 1750]
    for num, item in enumerate(inc_val):
        if item > length:
            return inc_val[:num]


def shell_sort(array, increment=None):
    """Сортировка Шелла

    Cортировка вставками с предварительными «грубыми» проходами.
    Сложность: Зависит от выбора инкрементов. По умолчанию последовательность Седжвика O(n^(4/3))

    -array - список который требуется отсортировать.

    ~На выход отсортированный список.
    """
    if not increment:
        increment = sedgwick_increment(len(array))
    for inc in reversed(increment):
        for now_num in range(inc, len(array)):
            for search_for_num in xrange(now_num, inc-1, -inc):
                if array[search_for_num - inc] <= array[search_for_num]:
                    break
                array[search_for_num-inc], array[search_for_num] = array[search_for_num], array[search_for_num-inc]
    return array













