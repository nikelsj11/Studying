#-*- coding: utf-8 -*-
import bisect

# Красюка Никиты НК-301
# Численные Методы
# Лаб.№ 1.4
# Сплайн интерполяция.


#Структура предназначена для описания сплайна на каждом сегменте сетки
class _SplineStruck(object):
    def __init__(self, x, y):
        self.x, self.a, self.b, self.c, self.d = [x, y, 0., 0., 0.]


#Интерполяция сплайнами
class InterpolationSpline(object):
    def __init__(self, initial_x, initial_y):
        self._x = initial_x
        self.splines = [_SplineStruck(x, y) for x, y in zip(initial_x, initial_y)]

        length = len(self.splines)

        alpha, beta = [[0. for _ in self.splines], [0. for _ in self.splines]]

        for i in range(1, length-1):
            h = abs(self.splines[i-1].x - self.splines[i].x)
            c = 4. * h
            f = 6. * ((self.splines[i+1].a - self.splines[i].a)/h - (self.splines[i].a - self.splines[i-1].a)/h)
            z = (h * alpha[i-1] + c)
            alpha[i] = -h/z
            beta[i] = (f-h*beta[i-1])/z

        for i in range(length-2, 0, -1):
            self.splines[i].c = alpha[i]*self.splines[i+1].c+beta[i]

        for i in range(length-1, 0, -1):
           h = self.splines[i].x-self.splines[i-1].x
           self.splines[i].d = (self.splines[i].c - self.splines[i-1].c)/h
           self.splines[i].b = h*(2.*self.splines[i].c+self.splines[i-1].c)/6.+(self.splines[i].a-self.splines[i-1].a)/h

    def _interpolate(self, x):
        distribution = sorted([t.x for t in self.splines])
        index = bisect.bisect_left(distribution, x)
        if index == len(distribution):
            return 0
        dx = x - self.splines[index].x
        return (self.splines[index].a +
                self.splines[index].b * dx +
                self.splines[index].c * dx**2 / 2. +
                self.splines[index].d * dx**3 / 6.)

    def get_point(self, x):
        return self._interpolate(x)

    def get_list(self, x_points_list):
        return [self._interpolate(x_item) for x_item in x_points_list]