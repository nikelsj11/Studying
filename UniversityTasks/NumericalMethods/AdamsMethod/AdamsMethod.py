#-*- coding: utf-8 -*-
import numpy

# Красюка Никиты НК-301
# Численные Методы
# Лаб.№ 5.2
# Метод Адамса


class AdamsMethod(object):
    def __init__(self, function, initial_x, initial_y):
        # function - функция ОДУ
        self.function = function
        # initial_y, initial_x - списки нач. точек (метод 2-го порядка) => нужно 2 точки [x0, x1], [y0, y1]
        self.initial_y = initial_y
        self.initial_x = initial_x

    def __getitem__(self, key):
        # [start, end] - промежуток на кот. ищем решение; step - шаг; step_half - шаг/2 (часто используеться)
        start, stop, step, step_half = key.start+key.step*2, key.stop+key.step, key.step, key.step/2.
        x, y = []+self.initial_x, []+self.initial_y

        for i, x_item in enumerate(numpy.arange(start, stop, step)):
            x.append(x_item)
            # расчет Yi+2
            k1 = 3./2. * self.function(x[i+1], y[i+1])
            k2 = 0.5*self.function(x[i], y[i])
            y.append(y[i+1]+(k1-k2)*step)

        return zip(x, y)
