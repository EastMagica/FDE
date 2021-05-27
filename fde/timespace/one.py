#!/usr/bin/python3
# -*- encoding:utf-8 -*-
# @author    : EastMagica
# @time      : 2021/05/27 12:15:47
# @file      : oned.py
# @project   : FDE
# @software  : VSCode

import numpy as np


# Classes
# -------

class TimeSpace:
    r"""TimeSpace Mesh

    with equispace.

    Options
    -------
    opt : {
        'domain': [start, end],
        'n': step_n
    }
    """
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
