#-*- coding: utf-8 -*-

# Красюка Никиты НК-301
# Численные Методы
# Лаб.№ 6.2
# Метод прогонки для системы линейных алгебраических уравнений с трехдиагональной матрицей. (Алгоритм Томаса)


# Алгоритм Томаса
# c - главная диагональ
# b - диагональ над главной
# a - диагональ под главной
# f - b свободные члены
def thomas_algorithm(a, b, c, f):
    length = len(f)
    alpha, beta = [0.], [0.]
    x_result = [0.] * length

    # вычисление прогоночных кэффициентов α и β
    for i in range(length-1):
        alpha.append(-b[i] / (a[i] * alpha[i] + c[i]))
        beta.append((f[i] - a[i]*beta[i])/(a[i]*alpha[i]+c[i]))

    # находим Xn
    x_result[-1] = (f[-1] - a[-2]*beta[-1])/(c[-1] + a[-2]*alpha[-1])

    # находим Xn-1..1, обратный ход
    for i in range(length-2, -1, -1):
        x_result[i] = alpha[i+1] * x_result[i+1] + beta[i+1]

    return x_result