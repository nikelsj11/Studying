#-*- coding: utf-8 -*-
from math import sin, cos, pi
from IntegrationPolygons import IntegrationPolygons

# Работает следующим образом:
# IntegrationPolygons( интегрируемая функция )[ начало : конец : шаг сетки ]
# обратите внимание что тут задаеться шаг сетки, а не количество иттераций n (шаг сетки = (конец - начало) / n)
# но учитывая особенности языка и удобство, задавать тут кол-во итераций нецелесообразно

print '-----------------> F(x) = SIN(x)'

print '∫ sin(x), x=0..2pi, step=0.5 ~ ', IntegrationPolygons(sin)[0:2*pi:0.5], '  !=  0.0'
print '∫ sin(x), x=0..2pi, step=0.1 ~ ', IntegrationPolygons(sin)[0:2*pi:0.1], '  !=  0.0'

print '\n', '-----------------> F(x) = 5'

print '∫ 5, x=0..5, step=1 ~ ', IntegrationPolygons(lambda x: 5)[0:5:1], '  ==  25'

print '\n', '-----------------> F(x) = x^2'

print '∫ x^2, x=0..50, step=0.001 ~ ', IntegrationPolygons(lambda x: pow(x, 2))[0:50:0.001], '  !=  41 667'
print '∫ x^2, x=0..50, step=0.0001 ~ ', IntegrationPolygons(lambda x: pow(x, 2))[0:50:0.0001], '  !=  41 667'
print '∫ x^2, x=0..50, step=0.00001 ~ ', IntegrationPolygons(lambda x: pow(x, 2))[0:50:0.00001], '  !=  41 667'
