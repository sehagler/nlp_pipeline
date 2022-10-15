# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 16:03:49 2022

@author: haglers
"""

#
import collections

#
class Evaluation_manager(object):
    
    #
    def __init__(self, static_data_manager):
        self.static_data_manager = static_data_manager
        
        static_data = self.static_data_manager.get_static_data()
       
        json_structure_manager = static_data['json_structure_manager']
        self.manual_review = \
            json_structure_manager.pull_key('manual_review')
        
    #
    def _compare_lists(self, x, y, display_flg):
        if x is not None and self.manual_review in x:
            x = self.manual_review
        if x is not None and len(x) == 0:
            x = None
        if x != self.manual_review:
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
                if self.manual_review in y:
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
    def _compare_values(self, x, y, display_flg):
        if x is not None and self.manual_review in x:
            x = self.manual_review
        if x != self.manual_review:
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
                if self.manual_review in y:
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
    def _compare_values_range(self, x, y, display_flg, value_range):
        display_data_flg = False
        print(x)
        print(y)
        if x is not None and self.manual_review in x:
            x = self.manual_review
        if x != self.manual_review:
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
                if self.manual_review in y:
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
    def evaluation(self, x, y, display_flg, value_range=None):
        if value_range is None:
            if (isinstance(x, list) or isinstance(x, tuple) or x is None) and \
               (isinstance(y, list) or isinstance(y, tuple) or y is None):
                result = self._compare_lists(x, y, display_flg)
            else:
                result = self._compare_values(x, y, display_flg)
        else:
            result = self._compare_values_range(x, y, display_flg, value_range)
        return result