#-*- coding: utf-8 -*-

# Красюка Никиты НК-301
# Численные Методы
# Лаб.№ 2.3
# Формула Симпсона.


# Формула Cимсона ( Составная формула (формула Котеса) )
class IntegrationSimpson(object):
    def __init__(self, function):
        # задаем интегрируемую функцию
        self.function = function

    def __getitem__(self, key):
        # start, stop, step - начало, конец, кол-во промежутков -> промежутка интегрирования
        start, stop, iterations_count = key.start, key.stop, key.step
        # величина шага
        step = (stop - start) / (iterations_count + 0.)
        # прибавляем к конечной сумме F(X_0)+F(X_n)
        f_sum = self.function(start) + self.function(stop)
        # прибавляем сумму от всех четных значений функции *4 (F(x_2)+...F(x_(n-1)))*4 (1 и n - элементы не трогаем)
        for i in range(1, iterations_count, 2):
            f_sum += self.function(start+i*step) * 4.
        # прибавляем сумму от всех не четных значений функции *2 (F(x_3)+...F(x_(n-2)))*2 (1 и n - элементы не трогаем)
        for i in range(2, iterations_count-1, 2):
            f_sum += self.function(start+i*step) * 2.
        # умножаем на шаг/3
        return f_sum * step / 3
