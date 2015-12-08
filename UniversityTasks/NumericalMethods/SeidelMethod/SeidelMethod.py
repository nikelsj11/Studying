#-*- coding: utf-8 -*-
from math import sqrt

# Красюка Никиты НК-301
# Численные Методы
# Лаб.№ 6.4
# Mетод Зейделя.


class SeidelMethod(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self, epsilon):
        # epsilon - погрешность которую необходимо достичь
        epsilon_reached = False
        size_a = len(self.a)
        result_x = [0.] * size_a

        while not epsilon_reached:
            check_sum = 0
            for i in range(size_a):
                # расчет Xi
                numerator_sum = sum([0 if i == j else self.a[i][j]*result_x[j] for j in range(size_a)])
                temp_x = (self.b[i] - numerator_sum) / self.a[i][i]
                # норма (прошлый X[i] - текущий X[i] )**2
                check_sum += pow(temp_x-result_x[i], 2)
                result_x[i] = temp_x
            # проверяем условие окончания

            epsilon_reached = sqrt(check_sum) < epsilon


        return result_x
