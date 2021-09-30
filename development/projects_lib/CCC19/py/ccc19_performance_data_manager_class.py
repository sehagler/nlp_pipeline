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
from tool_lib.py.analysis_tools_lib.text_analysis_tools import compare_texts
from tool_lib.py.processing_tools_lib.file_processing_tools \
    import read_xlsx_file
from tool_lib.py.query_tools_lib.date_tools import compare_dates

#
class CCC19_performance_data_manager(Performance_data_manager):
    
    #
    def __init__(self, static_data_manager, performance_json_manager,
                 project_json_manager):
        Performance_data_manager.__init__(self, static_data_manager, 
                                          performance_json_manager,
                                          project_json_manager)
        self.static_data = static_data_manager.get_static_data()
    
    #
    def _get_nlp_data(self, data_in):
        data_out = {}
        data_out['CANCER_STAGE'] = \
            self._get_data_value(data_in, None, 'CANCER_STAGE_' + self.nlp_value_key, 'CANCER_STAGE', mode_flg='single_value')
        if data_out['CANCER_STAGE'] is not None:
            data_out['CANCER_STAGE'] = data_out['CANCER_STAGE'][0]
        data_out['NORMALIZED_ECOG_SCORE'] = \
            self._get_data_value(data_in, None, 'ECOG_STATUS_' + self.nlp_value_key, 'NORMALIZED_ECOG_SCORE', mode_flg='single_value')
        if data_out['NORMALIZED_ECOG_SCORE'] is not None:
            data_out['NORMALIZED_ECOG_SCORE'] = \
                data_out['NORMALIZED_ECOG_SCORE'][0]
        data_out['NORMALIZED_SMOKING_HISTORY'] = \
            self._get_data_value(data_in, None, 'SMOKING_HISTORY_' + self.nlp_value_key, 'NORMALIZED_SMOKING_HISTORY', mode_flg='single_value')
        if data_out['NORMALIZED_SMOKING_HISTORY'] is not None:
            data_out['NORMALIZED_SMOKING_HISTORY'] = \
                data_out['NORMALIZED_SMOKING_HISTORY'][0]
        data_out['NORMALIZED_SMOKING_PRODUCTS'] = \
            self._get_data_value(data_in, None, 'SMOKING_PRODUCTS_' + self.nlp_value_key, 'NORMALIZED_SMOKING_PRODUCTS', mode_flg='multiple_values')
        data_out['NORMALIZED_SMOKING_STATUS'] = \
            self._get_data_value(data_in, None, 'SMOKING_STATUS_' + self.nlp_value_key, 'NORMALIZED_SMOKING_STATUS', mode_flg='single_value')
        if data_out['NORMALIZED_SMOKING_STATUS'] is not None:
            data_out['NORMALIZED_SMOKING_STATUS'] = \
                data_out['NORMALIZED_SMOKING_STATUS'][0]
        del_keys = []
        for key in data_out:
            if data_out[key] is not None:
                data_out[key] = data_out[key]
            else:
                del_keys.append(key)
        for key in del_keys:
            del data_out[key]  
        if not data_out:
            data_out = None
        return data_out
    
    #
    def _process_cancer_stage_performance(self, N, validation_csn_list,
                                          nlp_values, validation_data):
        nlp_cancer_stage_performance = []
        for csn in validation_csn_list:
            data_out = nlp_values[csn]
            print(csn)
            if data_out is not None:
                if 'CANCER_STAGE' in data_out.keys():
                    nlp_cancer_stage_value = data_out['CANCER_STAGE']
                else:
                    nlp_cancer_stage_value = None
            else:
                nlp_cancer_stage_value = None
            for item in validation_data:
                if item[2] == csn:
                    validation_cancer_stage_value = \
                        self._process_validation_item(item[3])
            if validation_cancer_stage_value is not None:
                validation_cancer_stage_value = \
                    tuple([ validation_cancer_stage_value ])
            display_data_flg = True
            performance, flg = \
                self._compare_data_values(nlp_cancer_stage_value,
                                          validation_cancer_stage_value)
            nlp_cancer_stage_performance.append(performance)
            if flg:
                display_data_flg = True
            FN, FP, FP_plus_FN, TN, TP = \
                self._performance_values(nlp_cancer_stage_performance)
            self.performance_statistics_dict['CANCER_STAGE'] = \
                self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
                
    #
    def _process_ecog_status_performance(self, N, validation_csn_list,
                                         nlp_values, validation_data):
        nlp_ecog_status_performance = []
        for csn in validation_csn_list:
            data_out = nlp_values[csn]
            print(csn)
            if data_out is not None:
                if 'NORMALIZED_ECOG_SCORE' in data_out.keys():
                    nlp_ecog_status_value = data_out['NORMALIZED_ECOG_SCORE']
                else:
                    nlp_ecog_status_value = None
            else:
                nlp_ecog_status_value = None
            for item in validation_data:
                if item[2] == csn:
                    validation_ecog_status_value = \
                        self._process_validation_item(item[4])
            if validation_ecog_status_value is not None:
                validation_ecog_status_value = \
                    tuple([ validation_ecog_status_value ])
            display_data_flg = True
            performance, flg = \
                self._compare_data_values(nlp_ecog_status_value,
                                          validation_ecog_status_value)
            nlp_ecog_status_performance.append(performance)
            if flg:
                display_data_flg = True
            FN, FP, FP_plus_FN, TN, TP = \
                self._performance_values(nlp_ecog_status_performance)
            self.performance_statistics_dict['ECOG_STATUS'] = \
                self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
                
    #
    def _process_smoking_history_performance(self, N, validation_csn_list,
                                             nlp_values, validation_data):
        nlp_smoking_history_performance = []
        for csn in validation_csn_list:
            data_out = nlp_values[csn]
            print(csn)
            if data_out is not None:
                if 'NORMALIZED_SMOKING_HISTORY' in data_out.keys():
                    nlp_smoking_history_value = \
                        data_out['NORMALIZED_SMOKING_HISTORY']
                else:
                    nlp_smoking_history_value = None
            else:
                nlp_smoking_history_value = None
            for item in validation_data:
                if item[2] == csn:
                    validation_smoking_history_value = \
                        self._process_validation_item(item[6])
            if validation_smoking_history_value is not None:
                validation_smoking_history_value = \
                    tuple([ validation_smoking_history_value ])
            display_data_flg = True
            performance, flg = \
                self._compare_data_values(nlp_smoking_history_value,
                                          validation_smoking_history_value)
            nlp_smoking_history_performance.append(performance)
            if flg:
                display_data_flg = True
            FN, FP, FP_plus_FN, TN, TP = \
                self._performance_values(nlp_smoking_history_performance)
            self.performance_statistics_dict['SMOKING_HISTORY'] = \
                self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
                
    #
    def _process_smoking_products_performance(self, N, validation_csn_list,
                                              nlp_values, validation_data):
        nlp_smoking_products_performance = []
        for csn in validation_csn_list:
            data_out = nlp_values[csn]
            print(csn)
            if data_out is not None:
                if 'NORMALIZED_SMOKING_PRODUCTS' in data_out.keys():
                    nlp_smoking_products_value = \
                        data_out['NORMALIZED_SMOKING_PRODUCTS']
                    nlp_smoking_products_value_tmp = \
                        nlp_smoking_products_value
                    nlp_smoking_products_value = []
                    for item0 in nlp_smoking_products_value_tmp:
                        for item1 in item0:
                            nlp_smoking_products_value.append(item1)
                    nlp_smoking_products_value = \
                        list(set(nlp_smoking_products_value))
                else:
                    nlp_smoking_products_value = None
            else:
                nlp_smoking_products_value = None
            for item in validation_data:
                if item[2] == csn:
                    validation_smoking_products_value = \
                        self._process_validation_item(item[7])
            if validation_smoking_products_value is not None:
                validation_smoking_products_value = \
                    tuple(validation_smoking_products_value)
            display_data_flg = True
            performance, flg = \
                self._compare_data_values(nlp_smoking_products_value,
                                          validation_smoking_products_value)
            nlp_smoking_products_performance.append(performance)
            if flg:
                display_data_flg = True
            FN, FP, FP_plus_FN, TN, TP = \
                self._performance_values(nlp_smoking_products_performance)
            self.performance_statistics_dict['SMOKING_PRODUCTS'] = \
                self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
                
    #
    def _process_smoking_status_performance(self, N, validation_csn_list,
                                            nlp_values, validation_data):
        nlp_smoking_status_performance = []
        for csn in validation_csn_list:
            data_out = nlp_values[csn]
            print(csn)
            if data_out is not None:
                if 'NORMALIZED_SMOKING_STATUS' in data_out.keys():
                    nlp_smoking_status_value = \
                        data_out['NORMALIZED_SMOKING_STATUS']
                else:
                    nlp_smoking_status_value = None
            else:
                nlp_smoking_status_value = None
            for item in validation_data:
                if item[2] == csn:
                    validation_smoking_status_value = \
                        self._process_validation_item(item[5])
            if validation_smoking_status_value is not None:
                validation_smoking_status_value = \
                    tuple([ validation_smoking_status_value ])
            display_data_flg = True
            performance, flg = \
                self._compare_data_values(nlp_smoking_status_value,
                                          validation_smoking_status_value)
            nlp_smoking_status_performance.append(performance)
            if flg:
                display_data_flg = True
            FN, FP, FP_plus_FN, TN, TP = \
                self._performance_values(nlp_smoking_status_performance)
            self.performance_statistics_dict['SMOKING_STATUS'] = \
                self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
        
    #
    def _read_validation_data(self, static_data):
        directory_manager = static_data['directory_manager']
        patient_list = static_data['patient_list']
        project_name = static_data['project_name']
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
    def calculate_performance(self):
        nlp_data = self.nlp_data
        validation_data = self._read_validation_data(self.static_data)
        csn_list = self.static_data['document_list']
        validation_mrn_list = []
        validation_csn_list =  []
        for item in validation_data:
            if item[2] in csn_list:
                validation_mrn_list.append(item[1])
                validation_csn_list.append(item[2])
        validation_mrn_list = list(set(validation_mrn_list))
        validation_csn_list = list(set(validation_csn_list))
        nlp_values = self._read_nlp_value_data(validation_csn_list, nlp_data)
        num_docs = len(validation_csn_list)
        num_pats = len(validation_mrn_list)
        N = num_docs
        self.performance_statistics_dict = {}
        self._process_cancer_stage_performance(N, validation_csn_list,
                                               nlp_values, validation_data)
        self._process_ecog_status_performance(N, validation_csn_list,
                                              nlp_values, validation_data)
        self._process_smoking_history_performance(N, validation_csn_list,
                                                  nlp_values, validation_data)
        self._process_smoking_products_performance(N, validation_csn_list,
                                                   nlp_values, validation_data)
        self._process_smoking_status_performance(N, validation_csn_list,
                                                 nlp_values, validation_data)
        print('\n')
        print('number of docs:\t\t%d' % num_docs)
        print('number of patients:\t%d' % num_pats)
        return self.performance_statistics_dict