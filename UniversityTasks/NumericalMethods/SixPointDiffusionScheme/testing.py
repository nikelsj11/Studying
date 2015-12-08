#-*- coding: utf-8 -*-
from math import sin, pi
import pylab
from NumericalMethods.SixPointDiffusionScheme.SixPointDiffusionScheme import SixPointDiffusionScheme

max_time = 50.
time_step_count = 600
conditions = [0, 0, lambda x: 1. * sin(pi*x/9.), lambda x, t: 0]
x_range = [0., 9.]
x_step_count = 18


# Нагрев t+1
# Сначало одно потом другое x/t
# Остывание -(t+5), 0

solver, steper = SixPointDiffusionScheme(
    max_time=max_time,
    time_step_count=time_step_count,
    conditions=conditions,
    x_range=x_range,
    x_step_count=x_step_count
).solve


colors = []

if solver[1][len(solver[1])/2] >= solver[-1][len(solver[-1])/2]:
    for i in range(256):
        colors.append('#%02x%02x%02x' % (255-i, 0, 0+i))
else:
    for i in range(256):
        colors.append('#%02x%02x%02x' % (0+i, 0, 255-i))

k = 0
step = len(solver)/255

for i in solver:
    if 0 == k % step:
        pylab.plot(steper, i, color=colors[k] if k < 256 else colors[len(colors)-1])

    k+=1

avr_0 = sum(solver[0]) / len(solver[0])
avr_n = sum(solver[-1]) / len(solver[-1])

if avr_0>avr_n:
    pylab.xlabel('Cooling: %s>%s'%(avr_0, avr_n))
else:
    pylab.xlabel('Heating: %s<%s'%(avr_0, avr_n))

pylab.show()
