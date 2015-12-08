#-*- coding: utf-8 -*-
from math import cos, pi

# Красюка Никиты НК-301
# Численные Методы
# Лаб.№ 3.2
# Формулы Гаусса-Кристофеля, оценки погрешностей, составные формулы


class IntegrationGauss(object):
    def __init__(self, function):
        self.function = function

    def __getitem__(self, key):
        # start, stop, step - начало, конец, степень полинома Лежандра
        start, stop, n = key.start, key.stop, key.step
        # вычисляем коэффициенты
        c1, c2 = (stop + start)/2.0, (stop - start)/2.0
        # находим корни многочлена Лежандра и соответствующие веса
        roots, weights = self.gauss_nodes(n)
        # вычисляем сумму произведений весов на значения функций в найденных корнях
        return c2*sum([weights[i]*self.function(c1 + c2*roots[i]) for i in range(len(roots))])

    # ф-я нахождения значения корней многочлена Лежандра m и соответствующих весов
    @staticmethod
    def gauss_nodes(m, tol=10e-9):
        # нахождение полинома степени M и его значения в точке V
        def legendre(v, m):
                p0, p1, tmp = 1.0, v, None
                for k in range(1, m):
                    tmp = ((2.0*k + 1.0)*v*p1 - k*p0)/(1.0 + k)
                    p0 = p1
                    p1 = tmp
                dp = m*(p0 - v*p1)/(1.0 - v**2)
                return tmp, dp
        # a - веса, х - корни
        a = [0. for _ in range(m)]
        x = [0. for _ in range(m)]
        # кол-во корней
        roots_number = (m + 1)/2
        for i in range(roots_number):
            # аппроксимация начального значения корня
            t = cos(pi*(i + 0.75)/(m + 0.5))
            # дальнейшее нахождение корня по методу Ньютона-Рафсона
            for j in range(30):
                p, dp = legendre(t, m)
                dt = -p/dp
                t += dt
                if abs(dt) < tol:
                    x[i] = t
                    x[m-i-1] = -t
                    a[i] = 2.0/(1.0 - t**2)/(dp**2)
                    a[m-i-1] = a[i]
                    break
        return x, a