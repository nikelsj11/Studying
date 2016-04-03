# -*- coding: utf-8 -*-
from math import pow
import numpy

# Красюка Никиты НК-301
# Численные Методы (2 семестр)
# Шеститочечная схема (явный случай) для одномерных уравнений теплопроводности с пост. коэффициентами


class SixPointDiffusionScheme(object):
    def __init__(self, **kwargs):
        self.max_time = kwargs['max_time']
        self.time_step_count = kwargs['time_step_count']
        self.x_range = kwargs['x_range']
        self.x_step_count = kwargs['x_step_count']

        self.fi = kwargs['conditions'][0]
        self.psi = kwargs['conditions'][1]
        self.u0 = kwargs['conditions'][2]
        self.F = kwargs['conditions'][3]

        self.tau = self.max_time / self.time_step_count
        self.h = (self.x_range[1] - self.x_range[0]) / self.x_step_count
        self.gamma = self.tau / pow(self.h, 2)

        if not self.tau / pow(self.h, 2) <= 0.5:
            raise BaseException("Violated the stability condition: τ/h²≤0.5")

        self.initial_state = [self.fi] + [self.u0(x) for x in numpy.arange(self.h, self.x_range[1], self.h)] + [
            self.psi]

    def _get_fi_factor(self, x, t):
        return self.F(x, t + 0.5 * self.tau)

    @property
    def solve(self):
        result = [self.initial_state]

        x_range = numpy.arange(1, self.x_step_count)

        for t in range(1, self.time_step_count+1):
            result_holder = [self.fi]
            for x in x_range:
                result_holder.append(
                    (1-2*self.gamma)*result[t-1][x]+self.gamma*(result[t-1][x-1]+result[t-1][x+1])
                    +
                    self.tau*self._get_fi_factor(x, t*self.tau-self.tau)
                )
            result.append(result_holder+[self.psi])

        return result, numpy.arange(self.x_range[0], self.x_range[1]+self.h, self.h)





















