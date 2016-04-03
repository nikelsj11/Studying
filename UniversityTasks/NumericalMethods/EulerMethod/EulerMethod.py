#-*- coding: utf-8 -*-
import numpy

# Красюка Никиты НК-301
# Численные Методы
# Лаб.№ 4.1
# Метод Эйлера


class EulerMethod(object):
    def __init__(self, function, initial_y):
        # initial_y - начальное условие, function - функция ОДУ
        self.function = function
        self.initial_y = initial_y

    def __getitem__(self, key):
        # [start, end] - промежуток на кот. ищем решение; step - шаг
        start, stop, step = key.start, key.stop+key.step, key.step
        x, y = [], [self.initial_y]

        for i, x_item in enumerate(numpy.arange(start, stop, step)):
            x.append(x_item)
            # расчет Yi+1
            y.append(y[i]+step*self.function(x_item, y[i]))

        return zip(x, y)
