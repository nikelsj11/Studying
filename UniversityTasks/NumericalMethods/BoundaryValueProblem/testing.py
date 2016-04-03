#-*- coding: utf-8 -*-
from numpy import cosh, arange
from BoundaryValueProblem import BoundaryValueProblem

# начальные условия задачи
Qx = 1
Fx = 1

start_condition = [-1, 0]
end_condition = [1, 0]

# шаг
step = 0.5

analytical_solution = lambda t: 1-(cosh(t)/cosh(1))

# расчитываем r - решения через аналитическую функцию и u - нашим методом
r = [analytical_solution(x) for x in arange(start_condition[0], end_condition[0]+step, step)]
u = BoundaryValueProblem(Qx, Fx)(start_condition, end_condition, step)

# расчитываем погрешность апроксимации уравнения (Ψ)
fi = [(r[i-1]-2*r[i]+r[i+1])/step**2-r[i]*Qx+Fx for i in range(1, len(u)-1)]
fi = [0.] + fi + [0.]


print "На промежутке [-1..1] с шагом сетки 0.5"
print " Xi     ~U(Xi)   U(Xi)    Error         Ψi"
print "---------------------------------------------"
for out, right, error, f in zip(u, r, [(i[1]-j) for i, j in zip(u, r)], fi):
    print "%3.2f\t%3.4f\t%3.4f\t%3.6f\t%3.6f" % (out[0], out[1], right, error, f)


