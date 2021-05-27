#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author  : east
# @time    : 2021/5/22 19:10
# @file    : adams.py
# @project : FDE

import numpy as np
import scipy as sp

from scipy.special import gamma
from scipy.optimize import root

from fde.timespace.one import TimeSpace


# Functions
# ---------

def _get_a_list(h, k0, dn):
    r"""Create a list

    .. math::

        a_{j, k+1} = \begin{cases}
        \frac{h^n}{n(n+1)} \left(k^{n+1}-(k-n)(k+1)^{n}\right)
            & \text{ if } j=0, \\
        \frac{h^n}{n(n+1)} \left((k-j+2)^{n+1}+(k-j)^{n+1}-2(k-j+1)^{n+1}\right)
            & \text{ if } 1\leq j\leq k, \\
        \frac{h^n}{n(n+1)}
            & \text{ if } j=k+1 \\
        \end{cases}

    Parameters
    ----------
    h : float
        time-step period, with equisapce.
    k0 : int
        k_n.
    dn : float
        the order of differention n.

    Returns
    -------
    list
        $a_{k+1}$ list, length is $k_{n+1}$

    Raises
    ------
    ValueError
        j out of (0, kn+1)
    """
    temp = h**dn / (dn * (dn + 1))
    temp_a_list = list()
    for j in range(0, k0 + 2):
        if j == 0:
            temp_a_list.append(
                temp * (k0**(dn + 1) - (k0 - dn) * (k0 + 1)**dn)
            )
        elif 0 < j < k0 + 1:
            temp_a_list.append(
                temp * (
                    (k0 - j + 2)**(dn + 1) +
                    (k0 - j)**(dn + 1) -
                    2 * (k0 - j + 1)**(dn + 1))
            )
        elif j == k0 + 1:
            temp_a_list.append(temp)
        else:
            raise ValueError
    return temp_a_list


def _get_b_list(h, k0, dn):
    r"""Create b list

    .. math::

        b_{j,k+1} = \frac{h^n}{n}((k+1-j)^n-(k-j)^n)

    Parameters
    ----------
    h : float
        time-step period, with equisapce.
    k0 : int
        k_n.
    dn : float
        the order of differention n.

    Returns
    -------
    list
        $a_{k+1}$ list, length is $k_{n}$
    """
    temp_b_list = list()
    for j in range(0, k0 + 1):
        temp_b_list.append(
            h**dn / dn * ((k0 + 1 - j)**dn - (k0 - j)**dn)
        )
    return temp_b_list


# Classes
# -------

class Adams(object):
    def __init__(self, func, dy0, dn, time_opt, mode='predictor'):
        """ABM method

        Adams-Bashforth-Moulton Method
        for single-term Fractional equations

        Parameters
        ----------
        func : Callable
            RHS function f(x, y(x)).
        dy0 : list
            Initial Partial D^{j}y(0).
        dn : float
            the order of differentiation n.
        time_opt : dict
            time options.
        mode: str
            mode of caculation, default is predictor.
        """
        # Function Options
        self.dn = dn
        self.func = func
        self.mode = mode.lower()
        self.dy0 = np.array(
            dy0 if isinstance(dy0, (list, tuple)) else [dy0]
        )
        self.m = int(np.ceil(dn))

        # Time Spliting
        self.t = TimeSpace(time_opt)

        # Temporary Variables
        self.k = 0
        self._a_list = []
        self._b_list = []
        self.y = [self.dy0[0]]

    @property
    def a(self):
        n_a = len(self._a_list)
        if n_a < self.k + 1:
            self._a_list = _get_a_list(
                h=self.t.h,
                k0=self.k - 1,
                dn=self.dn
            )
        return self._a_list

    @property
    def b(self):
        """
        equispaced case.
        """
        n_b = len(self._b_list)
        if n_b < self.k:
            self._b_list = _get_b_list(
                h=self.t.h,
                k0=self.k - 1,
                dn=self.dn
            )
        return self._b_list

    @property
    def yp_rectangle(self):
        k = self.k
        expr1 = np.sum([
            self.t[k]**j / gamma(j + 1) * self.dy0[j]
            for j in range(0, self.m)
        ], axis=0)
        expr2 = np.sum([
            self.b[j] * self.func(self.t[j], self.y[j])
            for j in range(0, k)
        ], axis=0)
        return expr1 + expr2 / gamma(self.dn)

    @property
    def yp_trapezoid(self):
        # TODO: to be continues
        raise NotImplementedError

    def y1_func(self, y1p):
        k = self.k
        expr1 = np.sum([
            self.t[k]**j / gamma(j + 1) * self.dy0[j]
            for j in range(0, self.m)
        ], axis=0)
        expr2 = np.sum([
            self.a[j] * self.func(self.t[j], self.y[j])
            for j in range(0, k)
        ], axis=0) + (
            self.a[k] * self.func(self.t[k], y1p)
        )
        return expr1 + expr2 / gamma(self.dn)

    @property
    def y1(self):
        if self.mode == 'predictor':
            yp = self.yp_rectangle
            return self.y1_func(yp)
        elif self.mode == 'implicit':
            sol = root(
                lambda x: x - self.y1_func(x),
                x0=self.y[self.k - 1],
                options={
                    'xtol': 1e-8
                }
            )
            if sol.success is False:
                raise ValueError(sol)
            return sol.x

    def iterator(self, parameter=False):
        temp_parameters = dict()
        for i in range(1, self.t.n + 1):
            self.k += 1
            self.y.append(self.y1)
            if parameter is True:
                temp_parameters[self.k] = {
                    'a': self.a,
                    'b': self.b
                }
        if parameter is True:
            return np.array(self.y).squeeze(), temp_parameters
        return np.array(self.y).squeeze()
