# -*- coding: utf-8 -*-
"""
Created on Mon Mar 04 12:29:38 2019

@author: haglers
"""

#
import os

#
from nlp_lib.py.performance_data_lib.performance_data_manager_class \
    import Performance_data_manager
from nlp_lib.py.tool_lib.analysis_tools_lib.text_analysis_tools \
    import compare_texts
from tool_lib.py.processing_tools_lib.file_processing_tools \
    import read_xlsx_file
from tool_lib.py.query_tools_lib.date_tools import compare_dates

#
class CCC19_performance_data_manager(Performance_data_manager):
    
    #
    def __init__(self, project_manager):
        project_data = project_manager.get_project_data()
        Performance_data_manager.__init__(self, project_manager)
        self.project_data = project_data
    
    #
    def _difference(self, x, y):
        z = list(set(x) - set(y))
        return z
    
    #
    def _find_data_value(self, node, key_0, key_1, mode_flg='single_value'):
        self.data_dict_list = []
        self._walk(node, key_0)
        self.data_value = []
        for data_dict in self.data_dict_list:
            data_list = data_dict[key_1].split(', ')
            if 'MANUAL_REVIEW' in data_list:
                data_list.remove('MANUAL_REVIEW')
            self.data_value.extend(data_list)
        self.data_value = list(self._unique(self.data_value))
        if mode_flg == 'single_value':
            if len(self.data_value) == 0:
                self.data_value = None
            elif len(self.data_value) == 1:
                self.data_value = self.data_value[0]
            elif len(self.data_value) > 1:
                self.data_value = self.multiple_values
        return self.data_value
        
    #
    def _intersection(self, x, y):
        z = list(set(x) & set(y))
        return z
    
    #
    def _performance_values(self, input_list):
        FN = len([ x for x in input_list if x == 'false negative' ])
        FP = len([ x for x in input_list if x == 'false positive' ])
        FP_plus_FN = \
            len([ x for x in input_list if x == 'false positive + false negative' ])
        TN = len([ x for x in input_list if x == 'true negative' ])
        TP = len([ x for x in input_list if x == 'true positive' ])
        return FN, FP, FP_plus_FN, TN, TP
    
    #
    def _process_validation_item(self, x):
        if x == '':
            x = None
        return x
        
    #
    def _read_validation_data(self, project_data):
        directory_manager = project_data['directory_manager']
        patient_list = project_data['patient_list']
        project_name = project_data['project_name']
        data_dir = directory_manager.pull_directory('raw_data_dir')
        book = read_xlsx_file(os.path.join(data_dir, 'ccc19_testing.xlsx'))
        sheet = book.sheet_by_index(0)
        ncols = sheet.ncols
        nrows = sheet.nrows
        validation_data = []
        for row_idx in range(nrows):
            if sheet.cell_value(row_idx, 1) in patient_list:
                validation_data_tmp = []
                for col_idx in range(ncols):
                    cell_value = sheet.cell_value(row_idx, col_idx)
                    try:
                        cell_value = str(int(cell_value))
                    except:
                        pass
                    if col_idx in [7]:
                        cell_value = cell_value.split(', ')
                        if len(cell_value) == 1:
                            if cell_value[0] == '':
                                cell_value = None
                    validation_data_tmp.append(cell_value)
                validation_data.append(validation_data_tmp)
        return validation_data
    
    #
    def _unique(self, lst):
        s = set()
        for el in lst:
            if isinstance(el, str):
                s.add(el)
            elif el[0] == 'not':
                s.add(tuple(*el))
            else:
                s.update(self._unique(el))
        return s
    
    #
    def _walk(self, node, key):
        for k, v in node.items():
            if k == key:
                self.data_dict_list.extend(v)
            elif isinstance(v, dict):
                self._walk(v, key)
                
    #
    def calculate_performance(self):
        nlp_data = self.nlp_data
        validation_data = self._read_validation_data(self.project_data)
        patient_list = self.project_data['patient_list']
        csn_list = self.project_data['document_list']
        validation_mrn_list = []
        validation_csn_list =  []
        for item in validation_data:
            if item[2] in csn_list:
                validation_mrn_list.append(item[1])
                validation_csn_list.append(item[2])
        validation_mrn_list = list(set(validation_mrn_list))
        validation_csn_list = list(set(validation_csn_list))
        nlp_cancer_stage_performance = []
        nlp_ecog_score_performance = []
        nlp_smoking_history_performance = []
        nlp_smoking_products_performance = []
        nlp_smoking_status_performance = []
        for csn in validation_csn_list:
            nlp_cancer_stage_value = None
            nlp_ecog_score_value = None
            nlp_smoking_history_value = None
            nlp_smoking_products_value = []
            nlp_smoking_status_value = None
            for item in nlp_data:
                if nlp_data[item][self.metadata_key]['SOURCE_SYSTEM_NOTE_CSN_ID'] == csn:
                    nlp_cancer_stage_value = \
                        self._find_data_value(nlp_data[item][self.nlp_data_key], 'CANCER_STAGE_' + self.nlp_value_key, 'CANCER_STAGE')
                    nlp_ecog_score_value = \
                        self._find_data_value(nlp_data[item][self.nlp_data_key], 'ECOG_SCORE_' + self.nlp_value_key, 'NORMALIZED_ECOG_SCORE')
                    nlp_smoking_history_value = \
                        self._find_data_value(nlp_data[item][self.nlp_data_key], 'SMOKING_HISTORY_' + self.nlp_value_key, 'NORMALIZED_SMOKING_HISTORY')
                    nlp_smoking_products_value = \
                        self._find_data_value(nlp_data[item][self.nlp_data_key], 'SMOKING_PRODUCTS_' + self.nlp_value_key, 'NORMALIZED_SMOKING_PRODUCTS', mode_flg='multiple_values')
                    nlp_smoking_status_value = \
                        self._find_data_value(nlp_data[item][self.nlp_data_key], 'SMOKING_STATUS_' + self.nlp_value_key, 'NORMALIZED_SMOKING_STATUS')
            for item in validation_data:
                if item[2] == csn:
                    validation_cancer_stage_value = \
                        self._process_validation_item(item[3])
                    validation_ecog_score_value = \
                        self._process_validation_item(item[4])
                    validation_smoking_status_value = \
                        self._process_validation_item(item[5])
                    validation_smoking_history_value = \
                        self._process_validation_item(item[6])
                    validation_smoking_products_value = \
                        self._process_validation_item(item[7])
            display_data_flg = True
            performance, flg = \
                self._compare_values(nlp_cancer_stage_value,
                                     validation_cancer_stage_value)
            nlp_cancer_stage_performance.append(performance)
            if flg:
                display_data_flg = True
            performance, flg = \
                self._compare_values(nlp_ecog_score_value,
                                     validation_ecog_score_value)
            nlp_ecog_score_performance.append(performance)
            if flg:
                display_data_flg = True
            performance, flg = \
                self._compare_values(nlp_smoking_history_value,
                                     validation_smoking_history_value)
            nlp_smoking_history_performance.append(performance)
            if flg:
                display_data_flg = True
            performance, flg = \
                self._compare_lists(nlp_smoking_products_value,
                                    validation_smoking_products_value)
            nlp_smoking_products_performance.append(performance)
            if flg:
                display_data_flg = True
            performance, flg = \
                self._compare_values(nlp_smoking_status_value,
                                     validation_smoking_status_value)
            nlp_smoking_status_performance.append(performance)
            if flg:
                display_data_flg = True
            if False:
                if display_data_flg:
                    print(csn)
        if True:
            performance_statistics_dict = {}
            num_docs = len(validation_csn_list)
            num_pats = len(validation_mrn_list)
            N = num_docs
            FN, FP, FP_plus_FN, TN, TP = \
                self._performance_values(nlp_cancer_stage_performance)
            performance_statistics_dict['CANCER_STAGE'] = \
                self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
            FN, FP, FP_plus_FN, TN, TP = \
                self._performance_values(nlp_ecog_score_performance)
            performance_statistics_dict['ECOG_SCORE'] = \
                self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
            FN, FP, FP_plus_FN, TN, TP = \
                self._performance_values(nlp_smoking_history_performance)
            performance_statistics_dict['SMOKING_HISTORY'] = \
                self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
            FN, FP, FP_plus_FN, TN, TP = \
                self._performance_values(nlp_smoking_products_performance)
            performance_statistics_dict['SMOKING_PRODUCTS'] = \
                self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
            FN, FP, FP_plus_FN, TN, TP = \
                self._performance_values(nlp_smoking_status_performance)
            performance_statistics_dict['SMOKING STATUS'] = \
                self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
            print('\n')
            print('number of docs:\t\t%d' % num_docs)
            print('number of patients:\t%d' % num_pats)
        return performance_statistics_dict
            
    #
    def display_performance(self, performance_statistics_dict):
        self._display_performance_statistics(performance_statistics_dict)