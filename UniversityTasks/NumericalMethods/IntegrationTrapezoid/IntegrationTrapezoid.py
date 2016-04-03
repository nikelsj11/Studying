#-*- coding: utf-8 -*-

# Красюка Никиты НК-301
# Численные Методы
# Лаб.№ 2.2
# Формула трапеций.
import numpy as np


# Метод трапеций (c использованием Формулы Котеса)
class IntegrationTrapezoid(object):
    def __init__(self, function):
        # задаем интегрируемую функцию
        self.function = function

    def __getitem__(self, key):
         # start, stop, step - начало, конец, шаг сетки -> промежутка интегрирования
        f_sum, start, stop, step = 0., key.start+key.step, key.stop, key.step
        # перебераем все значения (start .. stop) с шагом step | step=0.1, 0..1 => 0.1, 0.2, 0.3 .. 0.9
        for step_x in np.arange(start, stop, step):
            # суммируем значение функции от каждого шага step=0.1, 0..1, F(0.1)+F(0.2)+F(0.3)...+F(0.9)
            f_sum += self.function(step_x)
        # шаг * ( ( F(start) + F(stop) ) / 2  + посчитанная выше сумма )
        return step*( (self.function(start)+self.function(stop))/2. + f_sum )