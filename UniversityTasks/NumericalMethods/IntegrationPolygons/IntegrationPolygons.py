#-*- coding: utf-8 -*-

# Красюка Никиты НК-301
# Численные Методы
# Лаб.№ 2.1
# Формула прямоугольников.
import numpy as np


# Метод средних треугольников
class IntegrationPolygons(object):
    def __init__(self, function):
        # задаем интегрируемую функцию
        self.function = function

    def __getitem__(self, key):
        # start, stop, step - начало, конец, шаг сетки -> промежутка интегрирования
        f_sum, start, stop, step = 0., key.start+key.step, key.stop+key.step, key.step
        # перебераем все значения (start .. stop] с шагом step | step=0.1, 0..1 => 0.1, 0.2, 0.3 .. 0.9, 1
        for step_number in np.arange(start, stop, step):
            # суммируем F( x_i - step/2 )
            f_sum += self.function(start+step_number-step/2)
        # умножаем конечную сумму на шаг сетки
        return f_sum*step


