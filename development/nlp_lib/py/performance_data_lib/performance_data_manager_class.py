# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 09:39:27 2020

@author: haglers
"""

#
import collections

#
from distutils.dir_util import copy_tree
import getpass
from jsondiff import diff
import os
import shutil

#
from nlp_lib.py.base_class_lib.packager_base_class import Packager_base
from nlp_lib.py.manager_lib.directory_manager_class import Directory_manager
from nlp_lib.py.tool_lib.processing_tools_lib.file_processing_tools \
    import read_json_file, xml_diff

#
class Performance_data_manager(Packager_base):
    
    #
    def __init__(self, project_manager):
        project_data = project_manager.get_project_data()
        Packager_base.__init__(self, project_data)
        self.directory_manager = project_data['directory_manager']
        
    #
    def _compare_lists(self, x, y):
        display_data_flg = False
        try:
            if self.multiple_values in x:
                x = self.multiple_values
        except:
            pass
        if x is not self.multiple_values:
            if y is not None:
                if len(x) > 0:
                    if collections.Counter(x) == collections.Counter(y):
                        result = 'true positive'
                    else:
                        display_data_flg = True
                        result = 'false positive'
                else:
                    display_data_flg = True
                    result = 'false negative'
            else:
                if len(x) > 0:
                    display_data_flg = True
                    result = 'false positive'
                else:
                    result = 'true negative'
        else:
            result = 'multiple values'
        #if display_data_flg:
        #        print(x)
        #        print(y)
        return result, display_data_flg
        
    #
    def _compare_values(self, x, y):
        display_data_flg = False
        try:
            if self.multiple_values in x:
                x = self.multiple_values
        except:
            pass
        if x is not self.multiple_values:
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
            result = 'multiple values'
        #if display_data_flg:
        #    print(str(x) + ' ' + str(y))
        return result, display_data_flg
    
    #
    def _display_performance_statistics(self, performance_statistics_list):
        for performance_statistics in performance_statistics_list:
            print(performance_statistics['QUERY'])
            print(' accuracy:\t' + performance_statistics['ACCURACY'])
            print(' precision:\t' + performance_statistics['PRECISION'])
            print(' recall:\t' + performance_statistics['RECALL'])
            print(' F1:\t\t' + performance_statistics['F1'])

    #
    def _performance_statistics(self, FN, FP, FP_plus_FN, TN, TP, N):
        #N = TP + TN + FN + FP + FP_plus_FN
        if N > 0:
            A = (TP + TN) / N
        else:
            A = -1
        if TP + FP + FP_plus_FN > 0:
            P = TP / (TP + FP + FP_plus_FN)
        else:
            P = -1
        if TP + FN > 0:
            R = TP / (TP + FN + FP_plus_FN)
        else:
            R = -1
        if P != -1 and R != -1:
            if P * R > 0:
                F1 = 2 / (1/P + 1/R)
            else:
                F1 = -1
        else:
            F1 = -1
        performance_statistics = {}
        performance_statistics['ACCURACY'] = str(round(A, 3))
        performance_statistics['F1'] = str(round(F1, 3))
        performance_statistics['PRECISION'] = str(round(P, 3))
        performance_statistics['RECALL'] = str(round(R, 3))
        return performance_statistics
        
    #
    def display_performance_data(self):
        self.validation_manager.display_performance(self.performance_statistics_list)
        
    #
    def get_performance_data(self):
        self.validation_manager.read_nlp_data()
        self.performance_statistics_list = \
            self.validation_manager.calculate_performance()
        
    #
    def write_performance_data(self):
        self._write_performance_data(self.performance_statistics_list)