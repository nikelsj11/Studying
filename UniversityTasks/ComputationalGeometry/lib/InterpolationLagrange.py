#-*- coding: utf-8 -*-

# Красюка Никиты НК-301
# Численные Методы
# Лаб.№1.2
# Интерполяционный полином в форме Лагранжа. Оценка погрешности интерполяции.


class InterpolationLagrange(object):
    # принимаем и запоминаем массивы угловых точек
    def __init__(self, initial_x, initial_y):
        assert initial_x and initial_y
        self._x = initial_x
        self._y = initial_y

    # Считаем Q_n_i(x) (n смотрим по длинне массива)
    def _q(self, i, x):
        # находим отдельно numerator и denominator (числитель и знаменатель) по формуле Q
        numerator = 1.
        denominator = 1.
        # enumerate([x_0 .. x_n]) -> number=0, item=x_0; number=1, item=x_1; ...number=n, item=x_n;
        for number, item in enumerate(self._x):
            # пропускаем х_i
            if not number == i:
                numerator *= x - item
                denominator *= self._x[i] - item
        return numerator / denominator

    # рассчет самого полинома
    def _polynomial(self, x):
        # сумма произведений значений функций F(x_i) на Q_i_n(x)
        return sum([(self._y[number] * self._q(number, x)) for number, item in enumerate(self._x)])

    # интерполяция в одной точке
    def get_point(self, x):
        return self._polynomial(x)

    # интерполяция в списке точек
    def get_list(self, x_points_list):
        return [self._polynomial(item_x) for item_x in x_points_list]

