#-*- coding: utf-8 -*-

import numpy as np
from scipy.interpolate import PiecewisePolynomial

class HermiteInterpolation(PiecewisePolynomial):
    def __init__(self, x, y, axis=0):
        x = np.asarray(x)
        y = np.asarray(y)

        axis = axis % y.ndim

        xp = x.reshape((x.shape[0],) + (1,)*(y.ndim-1))
        yp = np.rollaxis(y, axis)

        data = np.empty((yp.shape[0], 2) + yp.shape[1:], y.dtype)
        data[:,0] = yp
        data[:,1] = self._get_derivatives(xp, yp)

        s = list(range(2, y.ndim + 1))
        s.insert(axis, 1)
        s.insert(axis, 0)
        data = data.transpose(s)

        PiecewisePolynomial.__init__(self, x, data, orders=3, direction=None,
                                     axis=axis)

    @staticmethod
    def _set_edge_case(m0, d1, out):
        m0 = np.atleast_1d(m0)
        d1 = np.atleast_1d(d1)
        mask = (d1 != 0) & (m0 != 0)
        out[mask] = 1.0/(1.0/m0[mask]+1.0/d1[mask])

    def _get_derivatives(self, x, y):
        y_shape = y.shape
        if y.ndim == 1:
            x = x[:,None]
            y = y[:,None]

        hk = x[1:] - x[:-1]
        mk = (y[1:] - y[:-1]) / hk
        smk = np.sign(mk)
        condition = ((smk[1:] != smk[:-1]) | (mk[1:] == 0) | (mk[:-1] == 0))

        w1 = 2*hk[1:] + hk[:-1]
        w2 = hk[1:] + 2*hk[:-1]
        whmean = 1.0/(w1+w2)*(w1/mk[1:] + w2/mk[:-1])

        dk = np.zeros_like(y)
        dk[1:-1][condition] = 0.0
        dk[1:-1][~condition] = 1.0/whmean[~condition]

        HermiteInterpolation._set_edge_case(mk[0],dk[1], dk[0])
        HermiteInterpolation._set_edge_case(mk[-1],dk[-2], dk[-1])

        return dk.reshape(y_shape)

    def get_list(self, x_points_list):
        return self.__call__(x_points_list)