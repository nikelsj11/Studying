#-*- coding: utf-8 -*-
from LUDecomposition import LUDecomposition

# представляем матрицу в виде Ax=b
A = [[2., 1., 4.],
     [3., 2., 1.],
     [1., 3., 3.]]

b = [16, 10, 16]

print "Исходная матрица:"
for n, i in enumerate(A):
    print i, '\t', b[n]
print '\n'

# производим декомпозицию
decomposition = LUDecomposition(A, b)

print "LU - разложенная матрица:"
for n, i in enumerate(decomposition.get_matrix()):
    print i, '\t', b[n]
print '\n'


print "Определитель: ", decomposition.get_det(), '\n'

print "Корни:"
for n, x in enumerate(reversed(decomposition.solve())):
    print "X_%s = %s" % (n+1, x)