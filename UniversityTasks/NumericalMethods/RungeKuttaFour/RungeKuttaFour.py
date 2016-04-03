#-*- coding: utf-8 -*-
import numpy

# Красюка Никиты НК-301
# Численные Методы
# Лаб.№ 5.1
# Метод Рунге-Кутта четвертого порядка


class RungeKuttaFour(object):
    def __init__(self, function, initial_y):
        # initial_y - начальное условие, function - функция ОДУ
        self.function = function
        self.initial_y = initial_y

    def __getitem__(self, key):
        # [start, end] - промежуток на кот. ищем решение; step - шаг
        start, stop, step, step_half = key.start, key.stop+key.step, key.step, key.step/2.
        x, y = [], [self.initial_y]

        for i, x_item in enumerate(numpy.arange(start, stop, step)):
            x.append(x_item)
            # расчет Yi+1
            k1 = self.function(x_item, y[i])
            k2 = self.function(x_item+step_half, y[i]+step_half*k1)
            k3 = self.function(x_item+step_half, y[i]+step_half*k2)
            k4 = self.function(x_item+step, y[i] + step*k3)
            y.append(y[i]+step/6.*(k1+2*k2+2*k3+k4))

        return zip(x, y)
