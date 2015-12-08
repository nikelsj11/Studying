#!/usr/bin/env python
# coding=utf-8


# известная задача, знаю 2 решения:
# первый вариант
def dict_from_lists(keys, values):
    return dict(
        map(None, keys, values)
        if len(keys) > len(values) else
        zip(keys, values)
    )


# второй вариант
def dict_from_lists2(keys, values, default_value=None):
    result = dict()
    values_iterator = iter(values)
    stop_iteration = False

    for key in keys:
        try:
            result[key] = values_iterator.next() if not stop_iteration else default_value
        except StopIteration:
            result[key] = default_value
            stop_iteration = True

    return result


if __name__ == "__main__":
    tkeys, tvalues = [1, 2, 3], [1, 2, 3]
    print dict_from_lists(tkeys, tvalues) == dict_from_lists2(tkeys, tvalues) == {1: 1, 2: 2, 3: 3}
    # >>> True

    tkeys, tvalues = [1, 2], [1, 2, 3]
    print dict_from_lists(tkeys, tvalues) == dict_from_lists2(tkeys, tvalues) == {1: 1, 2: 2}
    # >>> True

    tkeys, tvalues = [1, 2, 3], [1, 2]
    print dict_from_lists(tkeys, tvalues) == dict_from_lists2(tkeys, tvalues) == {1: 1, 2: 2, 3: None}
    # >>> True

    tkeys, tvalues = [None, 1, 2, 3], [1, 2, 3]
    print dict_from_lists(tkeys, tvalues) == dict_from_lists2(tkeys, tvalues) == {None: 1, 1: 2, 2: 3, 3: None}
    # >>> True

    tkeys, tvalues = [None, 1, 1, 3], [1, 2, 3]
    print dict_from_lists(tkeys, tvalues) == dict_from_lists2(tkeys, tvalues) == {None: 1, 1: 3, 3: None}
    # >>> True

