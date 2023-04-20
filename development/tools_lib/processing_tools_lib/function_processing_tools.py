# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 16:10:08 2022

@author: haglers
"""

#
from functools import reduce

#
def sequential_composition(*func):
    def compose(f, g):
        return lambda x : f(g(x))
    return reduce(compose, func, lambda x : x)

#
def sequential_composition_new(f_list, x):
    for i in range(len(f_list)):
        f = f_list[i]
        x = f(x)
    return x

#
def parallel_composition(f_list, x):
    y = {}
    if x is None:
        for i in range(len(f_list)):
            f = f_list[i]
            y[f.__name__] = f()
    else:
        for i in range(len(f_list)):
            f = f_list[i]
            y[f.__name__] = f(x)
    return y