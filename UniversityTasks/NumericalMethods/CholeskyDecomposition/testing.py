#-*- coding: utf-8 -*-
from CholeskyDecomposition import CholeskyDecomposition

# представляем матрицу в виде Ax=b
A = [[81., -45., 45.],
     [-45., 50., -15.],
     [45., -15., 38.]]

b = [531, -460, 193]

print "Исходная матрица:"
for n, i in enumerate(A):
    print i, '\t', b[n]
print '\n'

# производим декомпозицию
decomposition = CholeskyDecomposition(A, b)
matrix = decomposition.get_matrix()
matrix = [[round(j, 3) for j in i] for i in matrix]

print "Разложение Холесского:"
for n, i in enumerate(matrix):
    print i, '\t', b[n]
print '\n'

print "Корни:"
for n, x in enumerate(reversed(decomposition.solve())):
    print "X_%s = %s" % (n+1, x)