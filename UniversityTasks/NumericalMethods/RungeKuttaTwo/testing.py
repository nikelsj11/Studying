#-*- coding: utf-8 -*-
from math import exp
import numpy
from RungeKuttaTwo import RungeKuttaTwo

# функция нашего ОДУ
in_function = lambda t, y: 0.5*y+t

# функция - аналитическое решение
analytical_solution = lambda t: -2*(t+2)+4*exp(0.5*t)

# задаем начальные условия (функция ОДУ, начальное условие)
solver = RungeKuttaTwo(function=in_function, initial_y=0)

print "Решаем u` = 0.5 * u + x\n"

# находим список наших решений и список решений через аналитическую функцию ...
out_solution = solver[0:2:0.25]
right_solution = [analytical_solution(x) for x in numpy.arange(0, 2.25, 0.25)]
print "На промежутке [0..2] с шагом сетки 0.25"
print " Xi     ~U(Xi)   U(Xi)    Error"
print "--------------------------------"
for out, right, error in zip(out_solution, right_solution, [abs(i[1]-j) for i, j in zip(out_solution, right_solution)]):
    print "%3.2f\t%3.4f\t%3.4f\t%3.6f" % (out[0], out[1], right, error)


print "\n"

out_solution = solver[0:2:0.05]
right_solution = [analytical_solution(x) for x in numpy.arange(0, 2.05, 0.05)]
print "На промежутке [0..2] с шагом сетки 0.05"
print " Xi     ~U(Xi)   U(Xi)    Error"
print "--------------------------------"
for out, right, error in zip(out_solution, right_solution, [abs(i[1]-j) for i, j in zip(out_solution, right_solution)]):
    if out[0] % 0.25 == 0:
        print "%3.2f\t%3.4f\t%3.4f\t%3.6f" % (out[0], out[1], right, error)


print "\n"

out_solution = solver[0:2:0.01]
right_solution = [analytical_solution(x) for x in numpy.arange(0, 2.01, 0.01)]
print "На промежутке [0..2] с шагом сетки 0.01"
print " Xi     ~U(Xi)   U(Xi)    Error"
print "--------------------------------"
for out, right, error in zip(out_solution, right_solution, [abs(i[1]-j) for i, j in zip(out_solution, right_solution)]):
    if out[0] % 0.25 == 0:
        print "%3.2f\t%3.4f\t%3.4f\t%3.6f" % (out[0], out[1], right, error)