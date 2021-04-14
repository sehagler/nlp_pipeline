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
from nlp_lib.py.logger_lib.logger_class import Logger
from nlp_lib.py.tool_lib.processing_tools_lib.file_processing_tools \
    import read_package_json_file, read_nlp_data_from_package_json_file, write_json_file, xml_diff

#
class Performance_data_manager(object):
    
    #
    def __init__(self, project_manager):
        project_data = project_manager.get_project_data()
        self.directory_manager = project_data['directory_manager']
        self.save_dir = \
            self.directory_manager.pull_directory('processing_data_dir')
        self.project_data = project_data
        
        self.log_dir = self.directory_manager.pull_directory('log_dir')
        self.logger = Logger(self.log_dir)
        self.static_data = project_data

        json_structure_manager = project_data['json_structure_manager']
        self.document_wrapper_key = \
            json_structure_manager.pull_key('document_wrapper_key')
        self.documents_wrapper_key = \
            json_structure_manager.pull_key('documents_wrapper_key')
        self.metadata_key = \
            json_structure_manager.pull_key('metadata_key')
        self.nlp_data_key = \
            json_structure_manager.pull_key('nlp_data_key')
        self.nlp_datetime_key = \
            json_structure_manager.pull_key('nlp_datetime_key')
        self.nlp_datum_key = \
            json_structure_manager.pull_key('nlp_datum_key')
        self.nlp_metadata_key = \
            json_structure_manager.pull_key('nlp_metadata_key')
        self.nlp_performance_key = \
            json_structure_manager.pull_key('nlp_performance_key')
        self.nlp_query_key = \
            json_structure_manager.pull_key('nlp_query_key')
        self.nlp_section_key = \
            json_structure_manager.pull_key('nlp_section_key')
        self.nlp_specimen_key = \
            json_structure_manager.pull_key('nlp_specimen_key')
        self.nlp_source_text_key = \
            json_structure_manager.pull_key('nlp_source_text_key')
        self.nlp_text_element_key = \
            json_structure_manager.pull_key('nlp_text_element_key')
        self.nlp_text_key = \
            json_structure_manager.pull_key('nlp_text_key')
        self.nlp_value_key = \
            json_structure_manager.pull_key('nlp_value_key')
            
        # to be moved to appropriate location
        json_structure_manager = project_data['json_structure_manager']
        self.multiple_specimens = \
            json_structure_manager.pull_key('multiple_specimens')
        self.multiple_values = \
            json_structure_manager.pull_key('multiple_values')
        #
    
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
    def _write_performance_data(self, project_data, performance_statistics_list):
        project_name = project_data['project_name']
        documents_wrapper = read_package_json_file(project_data)
        for i in range(len(documents_wrapper[self.documents_wrapper_key])):
            nlp_data = \
                documents_wrapper[self.documents_wrapper_key][i][self.document_wrapper_key][self.nlp_data_key]
            query_list = []
            for nlp_datum in nlp_data:
                query_list.append(nlp_datum[self.nlp_datum_key][self.nlp_query_key])
            query_list = list(set(query_list))
            performance_statistics_list_tmp = []
            for item in performance_statistics_list:
                if item[self.nlp_query_key] in query_list:
                    performance_statistics_list_tmp.append(item)
            documents_wrapper[self.documents_wrapper_key][i][self.document_wrapper_key][self.nlp_performance_key] = \
                performance_statistics_list_tmp
        write_json_file(os.path.join(self.save_dir, project_name + '.json'),
                        documents_wrapper)
        
    #
    def display_performance_data(self):
        self.display_performance(self.performance_statistics_list)
        
    #
    def get_performance_data(self):
        self.read_nlp_data()
        self.performance_statistics_list = \
            self.calculate_performance()
            
    #
    def read_nlp_data(self):
        self.nlp_data = read_nlp_data_from_package_json_file(self.static_data)
        
    #
    def write_performance_data(self):
        self._write_performance_data(self.project_data,
                                     self.performance_statistics_list)