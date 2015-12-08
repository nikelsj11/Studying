#!/usr/bin/env python
# coding=utf-8
import math


# определяем сколько представлений в форме x**2+y**3 имеет палиндром
def get_palindrome_representation_count(palindrome):
    # находим максимально возможный куб через который можно представить палиндром
    # (-4) т.к. учитываем также минимальный квадрат равный 2**2
    max_cubed_value = int(pow(palindrome - 4, 1 / 3.0))
    counter = 0

    # будем находить все вариации по кубу, для того, чтобы не считать квадраты
    # выполним преобразование p = x**2 + y**3 <=> p - y**3 = x**2, и будем проверять
    # действительно ли число является кубом
    for value in range(2, max_cubed_value):
        square_value = palindrome - pow(value, 3)
        root_value = int(math.sqrt(square_value))
        if (pow(root_value, 2) + pow(value, 3)) == palindrome:
            counter += 1

    return counter


# генерируем палиндромы нужной длинны (для общего случая)
def get_palindromes_in_range(min_length, max_length, take_zero=False):
    # если нужно учитывать ноль
    if take_zero:
        yield 0

    # берем минимальное число равное половине длинны палиндрома, увеличиваем до
    # минимального числа следующего разряда, переворачиваем и склеиваем
    for digits in range(min_length, max_length + 1):
        first_part = 10 ** ((digits - 1) // 2)
        for counter in map(str, range(first_part, 10 * first_part)):
            yield int(counter + counter[-(digits % 2) - 1::-1])


if __name__ == "__main__":
    resulting_palindromes = list()

    # выполняем поиск необходимых нам палиндромов
    # длину [7..12] установили эвристическим путем
    for palindrome in get_palindromes_in_range(7, 12):
        if get_palindrome_representation_count(palindrome) == 4:
            resulting_palindromes.append(palindrome)
            if len(resulting_palindromes) == 5:
                break

    # смотрим что вышло
    for n, item in enumerate(resulting_palindromes):
        print '%s:\t%s' % (n, item)

    print '---------------'
    print 'SUM = %s' % sum(resulting_palindromes)

    # >>> 0:	5229225
    # >>> 1:	37088073
    # >>> 2:	56200265
    # >>> 3:	108909801
    # >>> 4:	796767697
    # >>> ---------------
    # >>> SUM = 1004195061