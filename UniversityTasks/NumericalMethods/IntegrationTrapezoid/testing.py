#-*- coding: utf-8 -*-
from math import sin, cos, pi
from IntegrationTrapezoid import IntegrationTrapezoid

# Работает следующим образом:
# IntegrationTrapezoid( интегрируемая функция )[ начало : конец : шаг сетки ]
# обратите внимание что тут задаеться шаг сетки, а не количество иттераций n (шаг сетки = (конец - начало) / n)
# но учитывая особенности языка и удобство, задавать тут кол-во итераций нецелесообразно

print '-----------------> F(x) = SIN(x)'

print '∫ sin(x), x=0..2pi, step=0.5 ~ ', IntegrationTrapezoid(sin)[0:2*pi:0.5], '  !=  0.0'
print '∫ sin(x), x=0..2pi, step=0.1 ~ ', IntegrationTrapezoid(sin)[0:2*pi:0.1], '  !=  0.0'
print '∫ sin(x), x=pi/2..pi, step=0.01 ~ ', IntegrationTrapezoid(sin)[pi/2:pi:0.01], '  !=  1'
print '∫ sin(x), x=pi/2..pi, step=0.0001 ~ ', IntegrationTrapezoid(sin)[pi/2:pi:0.0001], '  !=  1'

print '\n', '-----------------> F(x) = 5'

print '∫ 5, x=0..5, step=0.01 ~ ', IntegrationTrapezoid(lambda x: 5)[5:10:0.01], '  !=  25'
print '∫ 5, x=5..10, step=0.001 ~ ', IntegrationTrapezoid(lambda x: 5)[5:10:0.001], '  !=  25'
print '∫ 5, x=5..10, step=0.00001 ~ ', IntegrationTrapezoid(lambda x: 5)[5:10:0.00001], '  !=  25'

print '\n', '-----------------> F(x) = x^2'

print '∫ x^2, x=0..50, step=0.1 ~ ', IntegrationTrapezoid(lambda x: pow(x, 2))[0:50:0.1], '  !=  41 667'
print '∫ x^2, x=0..50, step=0.0001 ~ ', IntegrationTrapezoid(lambda x: pow(x, 2))[0:50:0.0001], '  !=  41 667'
print '∫ x^2, x=-10..10, step=0.05 ~ ', IntegrationTrapezoid(lambda x: pow(x, 2))[-10:10:0.1], '  !=  666.67'
print '∫ x^2, x=-10..10, step=0.0001 ~ ', IntegrationTrapezoid(lambda x: pow(x, 2))[-10:10:0.0001], '  !=  666.67'

print '\n', '-----------------> F(x) = x*(cos(x)-sin(x))/pi'

print '∫ x*(cos(x)-sin(x))/pi, x=0..100, step=0.1 ~ ', \
    IntegrationTrapezoid(lambda x: (x*(cos(x)-sin(x))/pi))[0:100:0.1], '  !=  11.448'
print '∫ x*(cos(x)-sin(x))/pi, x=0..100, step=0.01 ~ ', \
    IntegrationTrapezoid(lambda x: (x*(cos(x)-sin(x))/pi))[0:100:0.01], '  !=  11.448'
print '∫ x*(cos(x)-sin(x))/pi, x=0..100, step=0.001 ~ ', \
    IntegrationTrapezoid(lambda x: (x*(cos(x)-sin(x))/pi))[0:100:0.001], '  !=  11.448'

