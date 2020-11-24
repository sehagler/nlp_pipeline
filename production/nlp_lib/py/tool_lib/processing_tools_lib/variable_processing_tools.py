# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 15:25:14 2020

@author: haglers
"""

#
def delete_key(dictionary, key):
    try:
        del dictionary[key]
    except:
        pass