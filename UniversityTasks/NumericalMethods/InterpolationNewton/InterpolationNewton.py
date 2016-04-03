#-*- coding: utf-8 -*-

# Красюка Никиты НК-301
# Численные Методы
# Лаб.№1.3
# Интерполяционный полином в форме Ньютона. Оценка погрешности интерполяции.


class InterpolationNewton(object):
    def __init__(self, initial_x, initial_y):
        # принимаем и запоминаем массивы угловых точек
        self._x = initial_x
        self._y = initial_y
        # Находим значения (констант) А
        self._factors = ([self._y[0]] + [self._build_factor(number)
                                         for number in range(1, len(self._x))] if len(self._x) > 1 else [])

    # нахождение значения одного А
    def _build_factor(self, i):
        # находим W_k_i | (x_k - x_0)...(x_k - x_k-1)(x_k - x_k+1)...(X_k - x_i)
        # reduce(lambda res, x: res*x, выражение, 1) - находит произведение указанного выражение
        get_denominator = lambda k: reduce(lambda res, x: res*x, [(self._x[k]-self._x[n]) if n != k else 1 for n in range(0, i+1)], 1)
        # находим сумму F(k) / W_k_i(k), k = [0 .. i]
        return sum([(self._y[k]/get_denominator(k)) for k in range(0, i+1)])

    # нахождение самого полинома P(x) для определенного значения x
    def _polynomial(self, x):
        get_factor = lambda x_, k: reduce(lambda res, x: res*x, [(x_-self._x[n]) for n in range(0, k+1)], 1)
        return sum([self._factors[0]]+[(a * get_factor(x, number)) for number, a in enumerate(self._factors[1:])]
                   if len(self._factors) > 1 else [])

    # значение полинома интерполяции в одной точке
    def get_point(self, x):
        return self._polynomial(x)

    # значение полинома интеполяции в списке точек
    def get_list(self, x_points_list):
        return [self._polynomial(item_x) for item_x in x_points_list]

    # добавить уловую точку
    def add_factor(self, x, y):
        self._x.append(x)
        self._y.append(y)
        self._factors.append(self._build_factor(len(self._x)-1))





