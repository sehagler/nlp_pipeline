# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 16:03:49 2022

@author: haglers
"""

#
import collections

#
from base_lib.manager_base_class import Manager_base
    
#
def _compare_lists(x, y, display_flg, manual_review):
    if x is not None and manual_review in x:
        x = manual_review
    if x is not None and len(x) == 0:
        x = None
    if x != manual_review:
        if y is not None:
            if x is not None:
                if collections.Counter(x) == collections.Counter(y):
                    result = 'true positive'
                else:
                    result = 'false positive + false negative'
            else:
                result = 'false negative'
        else:
            if x is not None:
                result = 'false positive'
            else:
                result = 'true negative'
    else:
        if y is not None:
            if manual_review in y:
                result = 'true positive'
            else:
                result = 'false positive + false negative'
        else:
            result = 'false positive'
    if display_flg and 'true positive' not in result and 'true negative' not in result:
        print(result)
        print(x)
        print(y)
        print('')
    return result
    
#
def _compare_values(x, y, display_flg, manual_review):
    if x is not None and manual_review in x:
        x = manual_review
    if x != manual_review:
        if y is not None:
            if x is not None:
                if str(x) == str(y):
                    result = 'true positive'
                else:
                    result = 'false positive + false negative'
            elif x is None:
                result = 'false negative'
        else:
            if x is not None:
                result = 'false positive'
            else:
                result = 'true negative'
    else:
        if y is not None:
            if manual_review in y:
                result = 'true positive'
            else:
                result = 'false positive + false negative'
        else:
            result = 'false positive'
    if display_flg and 'true positive' not in result and 'true negative' not in result:
        print(result)
        print(x)
        print(y)
        print('')
    return result

#
def _compare_values_range(x, y, display_flg, value_range,
                          manual_review):
    if x is not None and manual_review in x:
        x = manual_review
    if x != manual_review:
        if y is not None:
            if x is not None:
                if abs(float(x) - float(y)) <= value_range:
                    result = 'true positive'
                else:
                    result = 'false positive + false negative'
            elif x is None:
                result = 'false negative'
        else:
            if x is not None:
                result = 'false positive'
            else:
                result = 'true negative'
    else:
        if y is not None:
            if manual_review in y:
                result = 'true positive'
            else:
                result = 'false positive + false negative'
        else:
            result = 'false positive'
    if display_flg and 'true positive' not in result and 'true negative' not in result:
        print(result)
        print(x)
        print(y)
        print('')
    return result

#
class Evaluation_manager(Manager_base):
    
    #
    def __init__(self, static_data_object):
        Manager_base.__init__(self, static_data_object)
        
    #
    def evaluation(self, x, y, display_flg, value_range=None):
        if value_range is None:
            if (isinstance(x, list) or isinstance(x, tuple) or x is None) and \
               (isinstance(y, list) or isinstance(y, tuple) or y is None):
                result = _compare_lists(x, y, display_flg, self.manual_review)
            else:
                result = _compare_values(x, y, display_flg, self.manual_review)
        else:
            result = _compare_values_range(x, y, display_flg, value_range, self.manual_review)
        return result