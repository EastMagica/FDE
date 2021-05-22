#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author  : east
# @time    : 2021/5/22 19:10
# @file    : adams.py
# @project : FDE

import numpy as np
import scipy as sp

from scipy.special import gamma


# Functions
# ---------

def _get_a_list(h, k0, dn):
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
    temp_b_list = list()
    for j in range(0, k0 + 1):
        temp_b_list.append(
            h**dn / dn * ((k0 + 1 - j)**dn - (k0 - j)**dn)
        )
    return temp_b_list


# Classes
# -------

class TimeSpace:
    domain: np.ndarray
    seq: np.ndarray
    n: int
    h: float
    
    def __init__(self, opt):
        self.init(opt)

    def init(self, opt):
        self.domain = opt["domain"]
        self.n = opt["n"]
        self.h = (self.domain[1] - self.domain[0]) / self.n
        self.seq = np.linspace(*self.domain, self.n + 1)
        
    def __getitem__(self, key):
        return self.seq[key]


class Adams(object):
    def __init__(self, func, dy0, dn, time_opt):
        self.func = func
        self.dy0 = dy0 if isinstance(dy0, (list, tuple)) else [dy0]
        self.dy0 = np.array(self.dy0)
        self.dn = dn
        
        self.m = int(np.ceil(dn))
        
        self.t = TimeSpace(time_opt)
        
        self._a_list = [None]
        self._b_list = []
        self.y = [self.dy0[0]]
        
        self.k = 0

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
    def yp(self):
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
    def y1(self):
        k = self.k
        expr1 = np.sum([
            self.t[k]**j / gamma(j + 1) * self.dy0[j]
            for j in range(0, self.m)
        ], axis=0)
        expr2 = np.sum([
            self.a[j] * self.func(self.t[j], self.y[j])
            for j in range(0, k)
        ], axis=0) + (
            self.a[k] * self.func(self.t[k], self.yp)
        )
        return expr1 + expr2 / gamma(self.dn)
    
    def iterator(self):
        for i in range(1, self.t.n + 1):
            self.k += 1
            self.y.append(self.y1)
        return np.array(self.y).squeeze()
