#-*- coding: utf-8 -*-
from ThomasAlgorithm import thomas_algorithm

# диагональ над главной
b = [1, -5, 2]
# главная диагональ
c = [2, 10, -5, 4]
# диагональ под главной
a = [1, 1, 1]
# b
f = [-5, -18, -40, -27]

# правильное решение
right_X = [-3., 1., 5., -8.]

# решаем систему
x = thomas_algorithm(a, b, c, f)

print "Наши решения:"
for n, i in enumerate(x):
    print "X_%s = %s" % (n+1, i)

print "\nПравильные решения:"
for n, i in enumerate(right_X):
    print "X_%s = %s" % (n+1, i)
