#-*- coding: utf-8 -*-
from math import sin, pi, cos, exp, log, tan
import matplotlib.pyplot as pyplot
from InterpolationLagrange import InterpolationLagrange


if __name__ == "__main__":
    # func_ - для генерации значений интерполяций, func_n - название функции (для вывода)
    func_ = lambda x: sin(x)
    func_n = 'Sin'

    # генерируем начальные значения для построения полинома
    start_x = [x * (pi/4) for x in range(0, 11)]
    start_y = [func_(i) for i in start_x]

    # инициализируем класс отвечающий за интерполяцию
    interpolate = InterpolationLagrange(start_x, start_y)

    print 'Интерполяция для функции %s(x):' % func_n
    print 'Значение в угловой точке %s(π/4) - Ρ(π/4): ' % func_n, func_(pi/4) - interpolate.get_point(pi/4)
    print 'Значение %s(π/6)' % func_n, func_(pi/6)
    print 'Значение Ρ(π/6): ', interpolate.get_point(pi/6)
    print 'Погрешность %s(π/6)-Ρ(π/6): ' % func_n, func_(pi/6) - interpolate.get_point(pi/6)
    print '\n--------------------------------------------\n'

    # генерируем массив начальных X
    end_point = int(round(start_x[-1]/0.5))+6
    in_x = [round(x * 0.5, 1) for x in range(-5, end_point)]
    # производим интерполяцию
    out_y = interpolate.get_list(in_x)

    # вообще т.к. функция переодична погрешность будет минимальной либо даже равной нулю
    pr = sum([abs(func_(item) - interpolate.get_point(item)) for item in start_x]) / (len(start_x) + 0.)
    print 'Погрешность для функции %s(x) x = 0 .. 8, step = 0.4: ' % func_n, pr

    # рисуем нашу интерполированную функцию
    pyplot.plot(in_x, out_y, color='black', linestyle='--', linewidth=1, marker='o', markersize=4,
                markeredgecolor='black', markerfacecolor='green', label=u'P(x)')

    # рисуем значения по которым проводили интерполяцию
    pyplot.plot(start_x, start_y, color='red', linestyle=':', linewidth=1, marker='s',  markersize=4,
                markeredgecolor='black', markerfacecolor='blue', markeredgewidth=1, label=u'interpolate values')

    #для интереса нарисуем саму функцию которую интерполируем
    in_v = [round(x * 0.08, 1) for x in range(0, 100)]
    pyplot.plot(in_v, [func_(i) for i in in_v], color='green', linestyle='-', linewidth=1, marker='s',  markersize=0,
                markeredgewidth=0, label=u'%s(x)' % func_n)

    #выводим график
    pyplot.legend(loc='best')
    pyplot.show()
