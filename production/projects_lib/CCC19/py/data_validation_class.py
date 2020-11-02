# -*- coding: utf-8 -*-
"""
Created on Mon Mar 04 12:29:38 2019

@author: haglers
"""

#
import collections
import os

#
from nlp_lib.py.manager_lib.directory_manager_class import Directory_manager
from nlp_lib.py.tool_lib.analysis_tools_lib.text_analysis_tools import compare_texts
from nlp_lib.py.tool_lib.processing_tools_lib.file_processing_tools \
    import read_json_file, read_xlsx_file
from nlp_lib.py.tool_lib.query_tools_lib.date_tools import compare_dates
from nlp_lib.py.logger_lib.logger_class import Logger

#
class Data_validation(object):
    
    #
    def __init__(self, project_data):
        self.project_data = project_data
        nlp_data = self._read_nlp_data(project_data)
        validation_data = self._read_validation_data(project_data)
        self._compare_data(nlp_data, validation_data)
        
    #
    def _compare_data(self, nlp_data, validation_data):
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
                if nlp_data[item]['METADATA']['SOURCE_SYSTEM_NOTE_CSN_ID'] == csn:
                    nlp_cancer_stage_value = \
                        self._find_data_value(nlp_data[item]['DATA'], 'CANCER STAGE VALUE')
                    nlp_ecog_score_value = \
                        self._find_data_value(nlp_data[item]['DATA'], 'ECOG SCORE VALUE')
                    nlp_smoking_history_value = \
                        self._find_data_value(nlp_data[item]['DATA'], 'SMOKING HISTORY VALUE')
                    nlp_smoking_products_value = \
                        self._find_data_value(nlp_data[item]['DATA'], 'SMOKING PRODUCTS VALUE', mode_flg='multiple_values')
                    nlp_smoking_status_value = \
                        self._find_data_value(nlp_data[item]['DATA'], 'SMOKING STATUS VALUE')
            for item in validation_data:
                if item[2] == csn:
                    validation_cancer_stage_value = self._process_validation_item(item[3])
                    validation_ecog_score_value = self._process_validation_item(item[4])
                    validation_smoking_status_value = self._process_validation_item(item[5])
                    validation_smoking_history_value = self._process_validation_item(item[6])
                    validation_smoking_products_value = self._process_validation_item(item[7])
            display_data_flg = False
            performance, flg = \
                self._compare_values(nlp_cancer_stage_value, validation_cancer_stage_value)
            nlp_cancer_stage_performance.append(performance)
            if flg:
                display_data_flg = True
            performance, flg = \
                self._compare_values(nlp_ecog_score_value, validation_ecog_score_value)
            nlp_ecog_score_performance.append(performance)
            if flg:
                display_data_flg = True
            performance, flg = \
                self._compare_values(nlp_smoking_history_value, validation_smoking_history_value)
            nlp_smoking_history_performance.append(performance)
            if flg:
                display_data_flg = True
            performance, flg = \
                self._compare_lists(nlp_smoking_products_value, validation_smoking_products_value)
            nlp_smoking_products_performance.append(performance)
            if flg:
                display_data_flg = True
            performance, flg = \
                self._compare_values(nlp_smoking_status_value, validation_smoking_status_value)
            nlp_smoking_status_performance.append(performance)
            if flg:
                display_data_flg = True
            if True:
                if display_data_flg:
                    print(csn)
        if True:
            num_docs = len(validation_csn_list)
            num_pats = len(validation_mrn_list)
            N = num_docs
            print('\n')
            print('number of docs: %d' % num_docs)
            print('number of patients:  %d' % num_pats)
            print('--cancer_stage--')
            FN = len([ x for x in nlp_cancer_stage_performance if x == 'false negative' ])
            FP = len([ x for x in nlp_cancer_stage_performance if x == 'false positive' ])
            TN = len([ x for x in nlp_cancer_stage_performance if x == 'true negative' ])
            TP = len([ x for x in nlp_cancer_stage_performance if x == 'true positive' ])
            A, P, R, F1 = self._performance(FN, FP, TN, TP, N)
            print(f'\taccuracy:  {A:.3f}')
            print(f'\tprecision: {P:.3f}')
            print(f'\trecall:    {R:.3f}')
            print(f'\tF1:        {F1:.3f}')
            print('--ecog_status--')
            FN = len([ x for x in nlp_ecog_score_performance if x == 'false negative' ])
            FP = len([ x for x in nlp_ecog_score_performance if x == 'false positive' ])
            TN = len([ x for x in nlp_ecog_score_performance if x == 'true negative' ])
            TP = len([ x for x in nlp_ecog_score_performance if x == 'true positive' ])
            A, P, R, F1 = self._performance(FN, FP, TN, TP, N)
            print(f'\taccuracy:  {A:.3f}')
            print(f'\tprecision: {P:.3f}')
            print(f'\trecall:    {R:.3f}')
            print(f'\tF1:        {F1:.3f}')
            print('--smoking_history--')
            FN = len([ x for x in nlp_smoking_history_performance if x == 'false negative' ])
            FP = len([ x for x in nlp_smoking_history_performance if x == 'false positive' ])
            TN = len([ x for x in nlp_smoking_history_performance if x == 'true negative' ])
            TP = len([ x for x in nlp_smoking_history_performance if x == 'true positive' ])
            A, P, R, F1 = self._performance(FN, FP, TN, TP, N)
            print(f'\taccuracy:  {A:.3f}')
            print(f'\tprecision: {P:.3f}')
            print(f'\trecall:    {R:.3f}')
            print(f'\tF1:        {F1:.3f}')
            print('--smoking_products--')
            FN = len([ x for x in nlp_smoking_products_performance if x == 'false negative' ])
            FP = len([ x for x in nlp_smoking_products_performance if x == 'false positive' ])
            TN = len([ x for x in nlp_smoking_products_performance if x == 'true negative' ])
            TP = len([ x for x in nlp_smoking_products_performance if x == 'true positive' ])
            A, P, R, F1 = self._performance(FN, FP, TN, TP, N)
            print(f'\taccuracy:  {A:.3f}')
            print(f'\tprecision: {P:.3f}')
            print(f'\trecall:    {R:.3f}')
            print(f'\tF1:        {F1:.3f}')
            print('--smoking_status--')
            FN = len([ x for x in nlp_smoking_status_performance if x == 'false negative' ])
            FP = len([ x for x in nlp_smoking_status_performance if x == 'false positive' ])
            TN = len([ x for x in nlp_smoking_status_performance if x == 'true negative' ])
            TP = len([ x for x in nlp_smoking_status_performance if x == 'true positive' ])
            A, P, R, F1 = self._performance(FN, FP, TN, TP, N)
            print(f'\taccuracy:  {A:.3f}')
            print(f'\tprecision: {P:.3f}')
            print(f'\trecall:    {R:.3f}')
            print(f'\tF1:        {F1:.3f}')
            
    #
    def _performance(self, FN, FP, TN, TP, N):
        if N > 0:
            A = (TP + TN) / N
        else:
            A = -1
        if TP + FP > 0:
            P = TP / (TP + FP)
        else:
            P = -1
        if TP + FN > 0:
            R = TP / (TP + FN)
        else:
            R = -1
        if P != -1 and R != -1:
            if P * R > 0:
                F1 = 2 / (1/P + 1/R)
            else:
                F1 = -1
        else:
            F1 = -1
        return A, P, R, F1
        
    #
    def _compare_lists(self, x, y):
        display_data_flg = False
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
        if display_data_flg:
                print(x)
                print(y)
        return result, display_data_flg
        
    #
    def _compare_values(self, x, y):
        display_data_flg = False
        if y is not None:
            if x is not None:
                if str(x) == str(y):
                    result = 'true positive'
                else:
                    display_data_flg = True
                    result = 'false positive'
            elif x is None:
                display_data_flg = True
                result = 'false negative'
        else:
            if x is not None:
                display_data_flg = True
                result = 'false positive'
            else:
                result = 'true negative'
        if display_data_flg:
            print(str(x) + ' ' + str(y))
        return result, display_data_flg
    
    #
    def _difference(self, x, y):
        z = list(set(x) - set(y))
        return z
    
    #
    def _find_data_value(self, node, key, mode_flg='single_value'):
        self.data_value = []
        self._walk(node, key)
        self.data_value = list(self._unique(self.data_value))
        if mode_flg == 'single_value':
            if len(self.data_value) == 0:
                self.data_value = None
            elif len(self.data_value) == 1:
                self.data_value = self.data_value[0]
            elif len(self.data_value) > 1:
                self.data_value = 'MULTIPLE_VALUES'
        return self.data_value
        
    #
    def _intersection(self, x, y):
        z = list(set(x) & set(y))
        return z
    
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
    def _read_nlp_data(self, project_data):
        directory_manager = project_data['directory_manager']
        patient_list = project_data['patient_list']
        project_name = project_data['project_name']
        nlp_data = {}
        data_dir = directory_manager.pull_directory('processing_data_dir')
        nlp_data_tmp = read_json_file(os.path.join(data_dir, project_name + '.json'))
        for item in nlp_data_tmp:
            patient = nlp_data_tmp[item]['METADATA']['OHSU_MRN']
            if patient in patient_list:
                nlp_data[item] = nlp_data_tmp[item]
        return nlp_data
    
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
                self.data_value.extend(v)
            elif isinstance(v, dict):
                self._walk(v, key)
            