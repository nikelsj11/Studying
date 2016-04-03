#-*- coding: utf-8 -*-
from math import sin, cos, pi, sinh, exp
from IntegrationGauss import IntegrationGauss

# интегрируемая функция
in_function = lambda x: exp(x)

# аналитически-выведенное значения интеграла
right_value = 2*sinh(1)
# находим значение интеграла нашим способом на промежутке [-1:1] с полиномом 2й степени
out_value = IntegrationGauss(in_function)[-1:1:2]

print '∫ e^(x), x=-1..1, n=2 ~ %5.10f' % out_value
print 'Точное значение = %5.10f' % right_value
print 'Погрешность = %5.10f' % (right_value-out_value), '\n'

# аналитически-выведенное значения интеграла
right_value = 54.598
# находим значение интеграла нашим способом на промежутке [-15:4] с полиномом 7й степени
out_value = IntegrationGauss(in_function)[-15:4:7]

print '∫ e^(x), x=-15..10, n=7 ~ %5.10f' % out_value
print 'Точное значение = %5.10f' % right_value
print 'Погрешность = %5.10f' % (right_value-out_value)



