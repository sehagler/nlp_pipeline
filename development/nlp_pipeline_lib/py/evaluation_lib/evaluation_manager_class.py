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
    def _compare_lists(self, x, y):
        display_data_flg = False
        try:
            if self.manual_review in x:
                x = self.manual_review
        except:
            pass
        try:
            if len(x) == 0:
                x = None
        except:
            pass
        if x != self.manual_review:
            if y is not None:
                if x is not None:
                    if collections.Counter(x) == collections.Counter(y):
                        result = 'true positive'
                    else:
                        display_data_flg = True
                        result = 'false positive'
                else:
                    display_data_flg = True
                    result = 'false negative'
            else:
                if x is not None:
                    display_data_flg = True
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
        if 'true positive' not in result and 'true negative' not in result:
            print(x)
            print(y)
            print('')
        return result, display_data_flg
        
    #
    def _compare_values(self, x, y):
        display_data_flg = False
        try:
            if self.manual_review in x:
                x = self.manual_review
        except:
            pass
        if x != self.manual_review:
            if y is not None:
                if x is not None:
                    if str(x) == str(y):
                        result = 'true positive'
                    else:
                        display_data_flg = True
                        result = 'false positive + false negative'
                elif x is None:
                    display_data_flg = True
                    result = 'false negative'
            else:
                if x is not None:
                    display_data_flg = True
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
        if 'true positive' not in result and 'true negative' not in result:
            print(x)
            print(y)
            print('')
        return result, display_data_flg
    
    #
    def _compare_values_range(self, x, y, value_range):
        display_data_flg = False
        try:
            if self.manual_review in x:
                x = self.manual_review
        except:
            pass
        if x != self.manual_review:
            if y is not None:
                if x is not None:
                    if abs(float(x[0]) - float(y[0])) <= value_range:
                        result = 'true positive'
                    else:
                        display_data_flg = True
                        result = 'false positive + false negative'
                elif x is None:
                    display_data_flg = True
                    result = 'false negative'
            else:
                if x is not None:
                    display_data_flg = True
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
        if 'true positive' not in result and 'true negative' not in result:
            print(x)
            print(y)
            print('')
        return result, display_data_flg
        
    #
    def evaluation(self, x, y, value_range=None):
        if value_range is None:
            if (isinstance(x, list) or isinstance(x, tuple) or x is None) and \
               (isinstance(y, list) or isinstance(y, tuple) or y is None):
                result, display_data_flg = self._compare_lists(x, y)
            else:
                result, display_data_flg = self._compare_values(x, y)
        else:
            result, display_data_flg = self._compare_values_range(x, y, value_range)
        return result, display_data_flg