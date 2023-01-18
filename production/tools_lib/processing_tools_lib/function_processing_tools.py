# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 16:10:08 2022

@author: haglers
"""

#
from functools import reduce

#
def composite_function(*func):
    def compose(f, g):
        return lambda x : f(g(x))
    return reduce(compose, func, lambda x : x)