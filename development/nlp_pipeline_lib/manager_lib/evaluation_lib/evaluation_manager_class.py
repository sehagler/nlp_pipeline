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
                    performance = 'true positive'
                else:
                    performance = 'false positive + false negative'
            else:
                performance = 'false negative'
        else:
            if x is not None:
                performance = 'false positive'
            else:
                performance = 'true negative'
    else:
        if y is not None:
            if manual_review in y:
                performance = 'true positive'
            else:
                performance = 'false positive + false negative'
        else:
            performance = 'false positive'
    return performance
    
#
def _compare_values(x, y, display_flg, manual_review):
    if x is not None and manual_review in x:
        x = manual_review
    if x != manual_review:
        if y is not None:
            if x is not None:
                if str(x) == str(y):
                    performance = 'true positive'
                else:
                    performance = 'false positive + false negative'
            elif x is None:
                performance = 'false negative'
        else:
            if x is not None:
                performance = 'false positive'
            else:
                performance = 'true negative'
    else:
        if y is not None:
            if manual_review in y:
                performance = 'true positive'
            else:
                performance = 'false positive + false negative'
        else:
            performance = 'false positive'
    return performance

#
def _compare_values_range(x, y, display_flg, value_range,
                          manual_review):
    if x is not None and manual_review in x:
        x = manual_review
    if x != manual_review:
        if y is not None:
            if x is not None:
                if abs(float(x) - float(y)) <= value_range:
                    performance = 'true positive'
                else:
                    performance = 'false positive + false negative'
            elif x is None:
                performance = 'false negative'
        else:
            if x is not None:
                performance = 'false positive'
            else:
                performance = 'true negative'
    else:
        if y is not None:
            if manual_review in y:
                performance = 'true positive'
            else:
                performance = 'false positive + false negative'
        else:
            performance = 'false positive'
    return performance

#
class Evaluation_manager(Manager_base):
    
    #
    def __init__(self, static_data_object, directory_object, logger_object,
                 evaluator_registry):
        Manager_base.__init__(self, static_data_object, directory_object,
                              logger_object)
        
    #
    def evaluation(self, arg_dict, value_range=None):
        display_flg = arg_dict['display_flg']
        x = arg_dict['nlp_value']
        y = arg_dict['validation_value']
        if value_range is None:
            if (isinstance(x, list) or isinstance(x, tuple) or x is None) and \
               (isinstance(y, list) or isinstance(y, tuple) or y is None):
                performance = \
                    _compare_lists(x, y, display_flg, self.manual_review)
            else:
                performance = \
                    _compare_values(x, y, display_flg, self.manual_review)
        else:
            performance = \
                _compare_values_range(x, y, display_flg, value_range,
                                      self.manual_review)
        arg_dict['performance'] = performance
        if display_flg and 'true positive' not in performance and 'true negative' not in performance:
            self.logger_object.print_log(performance)
            self.logger_object.print_log(x)
            self.logger_object.print_log(y)
            self.logger_object.print_log('')
        return arg_dict