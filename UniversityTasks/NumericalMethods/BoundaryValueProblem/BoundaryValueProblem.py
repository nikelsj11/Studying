#-*- coding: utf-8 -*-
import numpy

# Красюка Никиты НК-301
# Численные Методы
# Лаб.№ 5.3
# Решение граничных задач для обыкновенных дифференциальных уравнений


class BoundaryValueProblem(object):
    def __init__(self, boundary_q, boundary_f):
        # начальные условия q(x) - boundary_q, f(x) - boundary_f
        self.q = boundary_q
        self.f = boundary_f

    def __call__(self, start_condition, stop_condition, step):
        # start_condition - [x, u1(x)]; stop_condition - [x, u2(x)]; step - шаг
        start, stop = start_condition[0], stop_condition[0]
        # находим количество фрагментов на которых нужно найти решение (N)
        length = int((stop-start)/step)-1
        # Yi-1 и Yi+1 равны 1 по определению
        y1 = y3 = 1
        # расчитываем Y
        y2 = -(2+self.q*pow(step, 2))
        # расчитываем свободный член
        b = -self.f*step**2
        # заполняем векторы значений нашей 3-х диагональной матрицы -> решаем методом прогонки
        y = self.thomas_algorithm([y1]*length,  [y2]*length, [y3]*length, [b]*length)
        return zip(numpy.arange(start, stop+step, step), [start_condition[1]] + y + [stop_condition[1]])

    # метод прогонки (алгоритм томаса, есть в репозитории)
    @staticmethod
    def thomas_algorithm(a, c, b, f):
        length = len(f)
        alpha, beta = [0.], [0.]
        x_result = [0.] * length

        for i in range(length-1):
            alpha.append(-b[i] / (a[i] * alpha[i] + c[i]))
            beta.append((f[i] - a[i]*beta[i])/(a[i]*alpha[i]+c[i]))

        x_result[-1] = (f[-1] - a[-2]*beta[-1])/(c[-1] + a[-2]*alpha[-1])

        for i in range(length-2, -1, -1):
            x_result[i] = alpha[i+1] * x_result[i+1] + beta[i+1]

        return x_result