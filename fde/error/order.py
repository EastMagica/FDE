#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author  : east
# @time    : 2021/5/22 19:15
# @file    : fde/error/order.py
# @project : FDE

import numpy as np
from prettytable import PrettyTable


# Functions
# ---------

def iter_error_order(module, parameters, iter_name, iter_step, iter_func, collect_func):
    r"""Iteration to get OrderTable

    Parameters
    ----------
    module : Class
        caculate module.
    parameters : dict
        parameters for init module.
    iter_name : str
        iter variable name.
    iter_step : int
        iter variable step.
    iter_func : Callable
        functions to process initial options.
    collect_func : Callable
        functions to metric output data.

    Returns
    -------
    list
        error list.
    """
    data_collection = []

    for i in range(iter_step):
        m = module(**parameters)
        data = m.iterator()
        data_collection.append(
            collect_func(
                parameters[iter_name],
                data,
            )
        )
        parameters[iter_name] = iter_func(
            parameters[iter_name]
        )

    return data_collection



def _calc_error_order(step_error_list):
    r"""Caculate Error Order

    Parameters
    ----------
    step_error_list : list
        list of iter step errors.

    Returns
    -------
    list
        order list.
    """
    order_info = list()

    for i, (step_n, error) in enumerate(step_error_list):
        order_info.append([step_n, error])
        if i == 0:
            order_info[i].append(0)
        else:
            order_info[i].append(
                np.log2(order_info[i-1][1] / order_info[i][1])
            )

    return order_info


def error_table(step_error_list):
    r"""Generate Error Table

    Parameters
    ----------
    step_error_list : list
        list of iter step errors.

    Returns
    -------
    PrettyTable, list
        table and order list.
    """
    order_info = _calc_error_order(step_error_list)

    order_info_table = PrettyTable()

    order_info_table.field_names = ["step size", "Error of Adams scheme", "Error Order"]
    order_info_table.add_rows([
        [item[0], f"{item[1]: .6e}", f"{item[2]: .4f}" if i != 0 else ""]
        for i, item in enumerate(order_info)
    ])

    return order_info_table, order_info
