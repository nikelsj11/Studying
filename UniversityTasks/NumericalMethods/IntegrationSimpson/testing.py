#-*- coding: utf-8 -*-
from math import sin, cos, pi
from IntegrationSimpson import IntegrationSimpson

# Работает следующим образом:
# IntegrationSimpson( интегрируемая функция )[ начало : конец : кол-во фрагментов ]

print '-----------------> F(x) = SIN(x)'
print '∫ sin(x), x=pi/2..pi, step-count=2 ~ ', IntegrationSimpson(sin)[pi/2:pi:2], '  !=  1'
print '∫ sin(x), x=pi/2..pi, step-count=4 ~ ', IntegrationSimpson(sin)[pi/2:pi:4], '  !=  1'
print '∫ sin(x), x=pi/2..pi, step-count=6 ~ ', IntegrationSimpson(sin)[pi/2:pi:6], '  !=  1'
print '∫ sin(x), x=pi/2..pi, step-count=10 ~ ', IntegrationSimpson(sin)[pi/2:pi:10], '  !=  1'
print '∫ sin(x), x=0..pi*2, step-count=2 ~ ', IntegrationSimpson(sin)[0:pi*2:2], '  !=  0'
print '∫ sin(x), x=0..pi*2, step-count=4 ~ ', IntegrationSimpson(sin)[0:pi*2:4], '  !=  0'

print '\n', '-----------------> F(x) = 5'

print '∫ 5, x=0..5, step-count=7 ~ ', IntegrationSimpson(lambda x: 5)[5:10:7], '  !=  25'
print '∫ 5, x=0..5, step-count=10 ~ ', IntegrationSimpson(lambda x: 5)[5:10:100], '  !=  25'

print '\n', '-----------------> F(x) = x^2'

print '∫ x^2, x=0..50, step-count=1 ~ ', IntegrationSimpson(lambda x: pow(x, 2))[0:50:1], '  !=  41 667'
print '∫ x^2, x=-10..10, step-count=2 ~ ', IntegrationSimpson(lambda x: pow(x, 2))[-10:10:2], '  !=  666.67'

print '\n', '-----------------> F(x) = x*(cos(x)-sin(x))/pi'

print '∫ x*(cos(x)-sin(x))/pi, x=0..100, step-count=10 ~ ', \
    IntegrationSimpson(lambda x: (x*(cos(x)-sin(x))/pi))[0:100:10], '  !=  11.448'
print '∫ x*(cos(x)-sin(x))/pi, x=0..100, step-count=100 ~ ', \
    IntegrationSimpson(lambda x: (x*(cos(x)-sin(x))/pi))[0:100:100], '  !=  11.448'
print '∫ x*(cos(x)-sin(x))/pi, x=0..100, step-count=1000 ~ ', \
    IntegrationSimpson(lambda x: (x*(cos(x)-sin(x))/pi))[0:100:1000], '  !=  11.448'




