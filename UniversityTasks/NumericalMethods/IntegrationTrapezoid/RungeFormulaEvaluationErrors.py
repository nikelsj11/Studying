#-*- coding: utf-8 -*-
from math import sin, pi
from IntegrationTrapezoid import IntegrationTrapezoid

# [start, end] - промежуток интегрирования
start = pi/2.
end = pi

# для решения найдем решения с разными погрешностями 0.1, 0.001, 0.00001
for epsilon in [0.1, 0.001, 0.00001]:
    epsilon_reached = False
    n1 = 2
    n2 = 2*n1
    while not epsilon_reached:
        # расчитываем новые N и 2N
        n1 *= 2
        n2 = 2*n1
        # интегрируем
        I_n = IntegrationTrapezoid(sin)[start:end:(end-start)/n1]
        I_n2 = IntegrationTrapezoid(sin)[start:end:(end-start)/n2]
        # проверяем условие окончания
        epsilon_reached = (abs(I_n2-I_n)*1/3) < epsilon

    print "Интегрируем до достижения {0:.5f} <= ε".format(epsilon)
    print "∫ sin(x), x=pi/2..pi"
    print 'n = ', n1, '\t∫.. = ', I_n
    print 'n = ', n2, '\t∫.. = ', I_n2
    print 'Погрешность = {0:.10f}'.format(abs(I_n2-I_n)*1/3)
    print '\n'