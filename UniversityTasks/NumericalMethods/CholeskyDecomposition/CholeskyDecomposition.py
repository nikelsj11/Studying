#-*- coding: utf-8 -*-
from math import sqrt

# Красюка Никиты НК-301
# Численные Методы
# Лаб.№ 6.3
# Разложение Холесского для самосопряженной и положительно определенной матрицы.


class CholeskyDecomposition(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.length = len(a)
        self._make_decomposition()

    # произвести декомпозицию
    def _make_decomposition(self):
        for i in range(self.length):
            for j in range(i+1):
                if i == j:
                    # для диагональных элементов
                    self.a[i][j] = self.a[j][i] = \
                        sqrt(self.a[i][j] - sum([pow(self.a[i][k], 2) for k in range(i)]))
                else:
                    # для поддиагональных элементов
                    self.a[i][j] = self.a[j][i] = \
                        (self.a[i][j] - sum([self.a[i][k]*self.a[j][k] for k in range(j)])) / self.a[j][j]

    # получить декомпозированную матрицу
    def get_matrix(self):
        return self.a

    # решаем систему; L*y=b  =>  `L*x=y  => x - решение, (`L - транспонированная)
    def solve(self):
        # решаем L*y=b
        y = []
        for i in range(self.length):
            y.append((self.b[i]-sum([item*self.a[i][j] for j, item in enumerate(y)]))/self.a[i][i])

        # решаем `L*x=y
        x = []
        for i in range(self.length-1, -1, -1):
            x.append((y[i]-sum([item*self.a[i][self.length-1-j] for j, item in enumerate(x)]))/self.a[i][i])
        return x