#-*- coding: utf-8 -*-

# Красюка Никиты НК-301
# Численные Методы
# Лаб.№ 6.1
# LU – разложение.


class LUDecomposition(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.length = len(a)
        self._make_decomposition()

    # произвести декомпозицию
    def _make_decomposition(self):
        # используем исходную матрицу для хранения LU декомпозированной
        for i in range(self.length):
            for j in range(self.length):
                if i >= j:
                    # для нижней треугольной матрицы (включая диагональ)
                    self.a[i][j] = self.a[i][j]-sum([self.a[i][s]*self.a[s][j] for s in range(j)])
                else:
                    # для верхней треугольной матрицы (не включая диагональ)
                    self.a[i][j] = (self.a[i][j]-sum([self.a[i][s]*self.a[s][j] for s in range(i)]))/self.a[i][i]

    # получить декомпозированную матрицу
    def get_matrix(self):
        return self.a

    # получить определитель (по свойтву определитель - произведение диагональных элементов)
    def get_det(self):
        return reduce(lambda res, x: res*x, [self.a[i][i] for i in range(self.length)], 1)

    # решаем систему; L*y=b  =>  U*x=y  => x - решение
    def solve(self):
        # решаем L*y=b
        y = []
        for i in range(self.length):
            y.append((self.b[i]-sum([item*self.a[i][j] for j, item in enumerate(y)]))/self.a[i][i])

        # решаем U*x=y
        x = []
        for i in range(self.length-1, -1, -1):
            x.append(y[i]-sum([item*self.a[i][self.length-1-j] for j, item in enumerate(x)]))
        return x