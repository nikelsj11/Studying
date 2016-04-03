#-*- coding: utf-8 -*-
from decimal import Decimal
from SeidelMethod import SeidelMethod

# представляем матрицу в виде Ax=b
A = [[-1, 2,   -1,  -1],
     [1,  1, -1,  -2],
     [2,  1,   1,  1],
     [1,  1,   1,   -1]]

b = [22, -14, -10, -20]

# привильные значения Х
right_X = [1, 2, -1, -2]

# находим значения Х с погрешностью 0.1
x = SeidelMethod(A, b)(0.01)

print "Наши решения:"
for n, i in enumerate(x):
    print "X_%s = %s" % (n+1, i)

print "\nПравильные решения:"
for n, i in enumerate(right_X):
    print "X_%s = %s" % (n+1, i)

print "\nПогрешность:"
for n, i in enumerate(zip(right_X, x)):
    print "for X_%s = %s" % (n+1, abs(Decimal(i[0])-Decimal(i[1])))