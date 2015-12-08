#!/usr/bin/env python
# coding=utf-8
from random import randint

# n-число строк, m-число столбцов
m = 5
n = 4

# заполняем матрицу произвольными значениями, возьмем промежуток [-100..100]
array = [[randint(-100, 100) for __ in range(m)] for _ in range(n)]

# список - суммы положительных элементов строк матрицы
positive_items = [sum(filter(lambda x: x > 0, row)) for row in array]

# список - разности сумм четных и нечетных элементов строк матрицы
array_residual_even_odd = list()
for row in array:
    even_sum = 0
    odd_sum = 0
    for i in range(m):
        if i % 2 == 0:
            even_sum += row[i]
        else:
            odd_sum += row[i]
    array_residual_even_odd.append(even_sum-odd_sum)

# вывод исходной матрицы
for row in array:
    for item in row:
        print '{0:3d}'.format(item),
    print '\n'

# вывод суммы положительных элементов строк матрицы
for item in positive_items:
    print '{0:3d}'.format(item),
print '\n'

# вывод списков разности сумм четных и нечетных элементов строк матрицы
for item in array_residual_even_odd:
    print '{0:3d}'.format(item),
