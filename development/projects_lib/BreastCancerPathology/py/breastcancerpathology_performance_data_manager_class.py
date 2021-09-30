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
class BreastCancerPathology_performance_data_manager(Performance_data_manager):
    
    #
    def __init__(self, static_data_manager, performance_json_manager,
                 project_json_manager):
        Performance_data_manager.__init__(self,  static_data_manager,
                                          performance_json_manager,
                                          project_json_manager)
        self.static_data = static_data_manager.get_static_data()
    
    #
    def _get_nlp_data(self, data_in):
        data_out = {}
        data_out['ER_SCORE'] = \
            self._get_data_value(data_in, None, 'BREAST_CANCER_BIOMARKERS_ER_' + self.nlp_value_key, 'ER_SCORE', mode_flg='single_value')
        if data_out['ER_SCORE'] is not None:
            data_out['ER_SCORE'] = data_out['ER_SCORE'][0]
        data_out['ER_STATUS'] = \
            self._get_data_value(data_in, None, 'BREAST_CANCER_BIOMARKERS_ER_' + self.nlp_value_key, 'ER_STATUS', mode_flg='single_value')
        if data_out['ER_STATUS'] is not None:
            data_out['ER_STATUS'] = data_out['ER_STATUS'][0]
        data_out['ER_PERCENTAGE'] = \
            self._get_data_value(data_in, None, 'BREAST_CANCER_BIOMARKERS_ER_' + self.nlp_value_key, 'ER_PERCENTAGE', mode_flg='single_value')
        if data_out['ER_PERCENTAGE'] is not None:
            data_out['ER_PERCENTAGE'] = data_out['ER_PERCENTAGE'][0]
        data_out['HER2_SCORE'] = \
            self._get_data_value(data_in, None, 'BREAST_CANCER_BIOMARKERS_HER2_' + self.nlp_value_key, 'HER2_SCORE', mode_flg='single_value')
        if data_out['HER2_SCORE'] is not None:
            data_out['HER2_SCORE'] = data_out['HER2_SCORE'][0]
        data_out['HER2_STATUS'] = \
            self._get_data_value(data_in, None, 'BREAST_CANCER_BIOMARKERS_HER2_' + self.nlp_value_key, 'HER2_STATUS', mode_flg='single_value')
        if data_out['HER2_STATUS'] is not None:
            data_out['HER2_STATUS'] = data_out['HER2_STATUS'][0]
        data_out['HER2_PERCENTAGE'] = \
            self._get_data_value(data_in, None, 'BREAST_CANCER_BIOMARKERS_HER2_' + self.nlp_value_key, 'HER2_PERCENTAGE', mode_flg='single_value')
        if data_out['HER2_PERCENTAGE'] is not None:
            data_out['HER2_PERCENTAGE'] = data_out['HER2_PERCENTAGE'][0]
        data_out['KI67_STATUS'] = \
            self._get_data_value(data_in, None, 'BREAST_CANCER_BIOMARKERS_KI67_' + self.nlp_value_key, 'KI67_STATUS', mode_flg='single_value')
        if data_out['KI67_STATUS'] is not None:
            data_out['KI67_STATUS'] = data_out['KI67_STATUS'][0]
        data_out['KI67_PERCENTAGE'] = \
            self._get_data_value(data_in, None, 'BREAST_CANCER_BIOMARKERS_KI67_' + self.nlp_value_key, 'KI67_PERCENTAGE', mode_flg='single_value')
        if data_out['KI67_PERCENTAGE'] is not None:
            data_out['KI67_PERCENTAGE'] = data_out['KI67_PERCENTAGE'][0]
        data_out['PR_SCORE'] = \
            self._get_data_value(data_in, None, 'BREAST_CANCER_BIOMARKERS_PR_' + self.nlp_value_key, 'PR_SCORE', mode_flg='single_value')
        if data_out['PR_SCORE'] is not None:
            data_out['PR_SCORE'] = data_out['PR_SCORE'][0]
        data_out['PR_STATUS'] = \
            self._get_data_value(data_in, None, 'BREAST_CANCER_BIOMARKERS_PR_' + self.nlp_value_key, 'PR_STATUS', mode_flg='single_value')
        if data_out['PR_STATUS'] is not None:
            data_out['PR_STATUS'] = data_out['PR_STATUS'][0]
        data_out['PR_PERCENTAGE'] = \
            self._get_data_value(data_in, None, 'BREAST_CANCER_BIOMARKERS_PR_' + self.nlp_value_key, 'PR_PERCENTAGE', mode_flg='single_value')
        if data_out['PR_PERCENTAGE'] is not None:
            data_out['PR_PERCENTAGE'] = data_out['PR_PERCENTAGE'][0]
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
    def _process_er_performance(self, N, validation_csn_list, nlp_values,
                                  validation_data):
        nlp_er_status_performance = []
        nlp_er_score_performance = []
        nlp_er_percentage_performance = []
        for csn in validation_csn_list:
            data_out = nlp_values[csn]
            print(csn)
            if data_out is not None:
                if 'ER_STATUS' in data_out.keys():
                    nlp_er_status_value = data_out['ER_STATUS']
                else:
                    nlp_er_status_value = None
                if 'ER_SCORE' in data_out.keys():
                    nlp_er_score_value = data_out['ER_SCORE']
                else:
                    nlp_er_score_value = None
                if 'ER_PERCENTAGE' in data_out.keys():
                    nlp_er_percentage_value = data_out['ER_PERCENTAGE']
                else:
                    nlp_er_percentage_value = None
            else:
                nlp_er_status_value = None
                nlp_er_score_value = None
                nlp_er_percentage_value = None
            for item in validation_data:
                if item[2] == csn:
                    validation_er_status_value = \
                        self._process_validation_item(item[4])
                    validation_er_score_value = \
                        self._process_validation_item(item[5])
                    validation_er_percentage_value = \
                        self._process_validation_item(item[6])
            if validation_er_status_value is not None:
                validation_er_status_value = \
                    tuple(validation_er_status_value.split(', '))
            if validation_er_score_value is not None:
                validation_er_score_value = \
                    tuple(validation_er_score_value.split(', '))
            if validation_er_percentage_value is not None:
                validation_er_percentage_value = \
                    tuple(validation_er_percentage_value.split(', '))
            display_data_flg = True
            performance, flg = \
                self._compare_data_values(nlp_er_status_value,
                                          validation_er_status_value)
            nlp_er_status_performance.append(performance)
            if flg:
                display_data_flg = True
            performance, flg = \
                self._compare_data_values(nlp_er_score_value,
                                          validation_er_score_value)
            nlp_er_score_performance.append(performance)
            if flg:
                display_data_flg = True
            performance, flg = \
                self._compare_data_values(nlp_er_percentage_value,
                                          validation_er_percentage_value)
            nlp_er_percentage_performance.append(performance)
            if flg:
                display_data_flg = True
        FN, FP, FP_plus_FN, TN, TP = \
            self._performance_values(nlp_er_status_performance)
        self.performance_statistics_dict['ER_STATUS'] = \
            self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
        FN, FP, FP_plus_FN, TN, TP = \
            self._performance_values(nlp_er_score_performance)
        self.performance_statistics_dict['ER_SCORE'] = \
            self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
        FN, FP, FP_plus_FN, TN, TP = \
            self._performance_values(nlp_er_percentage_performance)
        self.performance_statistics_dict['ER_PERCENTAGE'] = \
            self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
    
    #
    def _process_her2_performance(self, N, validation_csn_list, nlp_values,
                                  validation_data):
        nlp_her2_status_performance = []
        nlp_her2_score_performance = []
        nlp_her2_percentage_performance = []
        for csn in validation_csn_list:
            data_out = nlp_values[csn]
            print(csn)
            if data_out is not None:
                if 'HER2_STATUS' in data_out.keys():
                    nlp_her2_status_value = data_out['HER2_STATUS']
                else:
                    nlp_her2_status_value = None
                if 'HER2_SCORE' in data_out.keys():
                    nlp_her2_score_value = data_out['HER2_SCORE']
                else:
                    nlp_her2_score_value = None
                if 'HER2_PERCENTAGE' in data_out.keys():
                    nlp_her2_percentage_value = data_out['HER2_PERCENTAGE']
                else:
                    nlp_her2_percentage_value = None
            else:
                nlp_her2_status_value = None
                nlp_her2_score_value = None
                nlp_her2_percentage_value = None
            for item in validation_data:
                if item[2] == csn:
                    validation_her2_status_value = \
                        self._process_validation_item(item[11])
                    validation_her2_score_value = \
                        self._process_validation_item(item[12])
                    validation_her2_percentage_value = \
                        self._process_validation_item(item[13])
            if validation_her2_status_value is not None:
                validation_her2_status_value = \
                    tuple(validation_her2_status_value.split(', '))
            if validation_her2_score_value is not None:
                validation_her2_score_value = \
                    tuple(validation_her2_score_value.split(', '))
            if validation_her2_percentage_value is not None:
                validation_her2_percentage_value = \
                    tuple(validation_her2_percentage_value.split(', '))
            display_data_flg = True
            performance, flg = \
                self._compare_data_values(nlp_her2_status_value,
                                          validation_her2_status_value)
            nlp_her2_status_performance.append(performance)
            if flg:
                display_data_flg = True
            performance, flg = \
                self._compare_data_values(nlp_her2_score_value,
                                          validation_her2_score_value)
            nlp_her2_score_performance.append(performance)
            if flg:
                display_data_flg = True
            performance, flg = \
                self._compare_data_values(nlp_her2_percentage_value,
                                          validation_her2_percentage_value)
            nlp_her2_percentage_performance.append(performance)
            if flg:
                display_data_flg = True
        FN, FP, FP_plus_FN, TN, TP = \
            self._performance_values(nlp_her2_status_performance)
        self.performance_statistics_dict['HER2_STATUS'] = \
            self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
        FN, FP, FP_plus_FN, TN, TP = \
            self._performance_values(nlp_her2_score_performance)
        self.performance_statistics_dict['HER2_SCORE'] = \
            self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
        FN, FP, FP_plus_FN, TN, TP = \
            self._performance_values(nlp_her2_percentage_performance)
        self.performance_statistics_dict['HER2_PERCENTAGE'] = \
            self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N) 
    
    #
    def _process_ki67_performance(self, N, validation_csn_list, nlp_values,
                                  validation_data):
        nlp_ki67_status_performance = []
        nlp_ki67_percentage_performance = []
        for csn in validation_csn_list:
            data_out = nlp_values[csn]
            print(csn)
            if data_out is not None:
                if 'KI67_STATUS' in data_out.keys():
                    nlp_ki67_status_value = data_out['KI67_STATUS']
                else:
                    nlp_ki67_status_value = None
                if 'KI67_PERCENTAGE' in data_out.keys():
                    nlp_ki67_percentage_value = data_out['KI67_PERCENTAGE']
                else:
                    nlp_ki67_percentage_value = None
            else:
                nlp_ki67_status_value = None
                nlp_ki67_percentage_value = None
            for item in validation_data:
                if item[2] == csn:
                    validation_ki67_status_value = \
                        self._process_validation_item(item[14])
                    validation_ki67_percentage_value = \
                        self._process_validation_item(item[15])
            if validation_ki67_status_value is not None:
                validation_ki67_status_value = \
                    tuple(validation_ki67_status_value.split(', '))
            if validation_ki67_percentage_value is not None:
                validation_ki67_percentage_value = \
                    tuple(validation_ki67_percentage_value.split(', '))
            display_data_flg = True
            performance, flg = \
                self._compare_data_values(nlp_ki67_status_value,
                                          validation_ki67_status_value)
            nlp_ki67_status_performance.append(performance)
            if flg:
                display_data_flg = True
            performance, flg = \
                self._compare_data_values(nlp_ki67_percentage_value,
                                          validation_ki67_percentage_value)
            nlp_ki67_percentage_performance.append(performance)
            if flg:
                display_data_flg = True
        FN, FP, FP_plus_FN, TN, TP = \
            self._performance_values(nlp_ki67_status_performance)
        self.performance_statistics_dict['KI67_STATUS'] = \
            self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
        FN, FP, FP_plus_FN, TN, TP = \
            self._performance_values(nlp_ki67_percentage_performance)
        self.performance_statistics_dict['KI67_PERCENTAGE'] = \
            self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
            
    #
    def _process_pr_performance(self, N, validation_csn_list, nlp_values,
                                  validation_data):
        nlp_pr_status_performance = []
        nlp_pr_score_performance = []
        nlp_pr_percentage_performance = []
        for csn in validation_csn_list:
            data_out = nlp_values[csn]
            print(csn)
            if data_out is not None:
                if 'PR_STATUS' in data_out.keys():
                    nlp_pr_status_value = data_out['PR_STATUS']
                else:
                    nlp_pr_status_value = None
                if 'PR_SCORE' in data_out.keys():
                    nlp_pr_score_value = data_out['PR_SCORE']
                else:
                    nlp_pr_score_value = None
                if 'PR_PERCENTAGE' in data_out.keys():
                    nlp_pr_percentage_value = data_out['PR_PERCENTAGE']
                else:
                    nlp_pr_percentage_value = None
            else:
                nlp_pr_status_value = None
                nlp_pr_score_value = None
                nlp_pr_percentage_value = None
            for item in validation_data:
                if item[2] == csn:
                    validation_pr_status_value = \
                        self._process_validation_item(item[8])
                    validation_pr_score_value = \
                        self._process_validation_item(item[9])
                    validation_pr_percentage_value = \
                        self._process_validation_item(item[10])
            if validation_pr_status_value is not None:
                validation_pr_status_value = \
                    tuple(validation_pr_status_value.split(', '))
            if validation_pr_score_value is not None:
                validation_pr_score_value = \
                    tuple(validation_pr_score_value.split(', '))
            if validation_pr_percentage_value is not None:
                validation_pr_percentage_value = \
                    tuple(validation_pr_percentage_value.split(', '))
            display_data_flg = True
            performance, flg = \
                self._compare_data_values(nlp_pr_status_value,
                                          validation_pr_status_value)
            nlp_pr_status_performance.append(performance)
            if flg:
                display_data_flg = True
            performance, flg = \
                self._compare_data_values(nlp_pr_score_value,
                                          validation_pr_score_value)
            nlp_pr_score_performance.append(performance)
            if flg:
                display_data_flg = True
            performance, flg = \
                self._compare_data_values(nlp_pr_percentage_value,
                                          validation_pr_percentage_value)
            nlp_pr_percentage_performance.append(performance)
            if flg:
                display_data_flg = True
        FN, FP, FP_plus_FN, TN, TP = \
            self._performance_values(nlp_pr_status_performance)
        self.performance_statistics_dict['PR_STATUS'] = \
            self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
        FN, FP, FP_plus_FN, TN, TP = \
            self._performance_values(nlp_pr_score_performance)
        self.performance_statistics_dict['PR_SCORE'] = \
            self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
        FN, FP, FP_plus_FN, TN, TP = \
            self._performance_values(nlp_pr_percentage_performance)
        self.performance_statistics_dict['PR_PERCENTAGE'] = \
            self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
        
    #
    def _read_validation_data(self, static_data):
        directory_manager = static_data['directory_manager']
        if 'patient_list' in static_data.keys():
            patient_list = static_data['patient_list']
        else:
            patient_list = None
        project_name = static_data['project_name']
        data_dir = directory_manager.pull_directory('raw_data_dir')
        book = read_xlsx_file(os.path.join(data_dir, 'breastcancerpathology_testing.xlsx'))
        sheet = book.sheet_by_index(0)
        ncols = sheet.ncols
        nrows = sheet.nrows
        validation_data = []
        for row_idx in range(nrows):
            if patient_list is None or sheet.cell_value(row_idx, 1) in patient_list:
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
        manual_review_str = 'MANUAL_REVIEW'
        nlp_data = self.nlp_data
        validation_data = self._read_validation_data(self.static_data)
        if 'document_list' in self.static_data.keys():
            csn_list = self.static_data['document_list']
        else:
            csn_list = None
        validation_mrn_list = []
        validation_csn_list =  []
        for item in validation_data:
            if csn_list is None or item[2] in csn_list:
                validation_mrn_list.append(item[1])
                validation_csn_list.append(item[2])
        validation_mrn_list = list(set(validation_mrn_list))
        validation_csn_list = list(set(validation_csn_list))
        nlp_values = self._read_nlp_value_data(validation_csn_list, nlp_data)
        num_docs = len(validation_csn_list)
        num_pats = len(validation_mrn_list)
        N = num_docs
        self.performance_statistics_dict = {}
        self._process_er_performance(N, validation_csn_list, nlp_values,
                                     validation_data)
        self._process_pr_performance(N, validation_csn_list, nlp_values,
                                     validation_data)
        self._process_her2_performance(N, validation_csn_list, nlp_values,
                                       validation_data)
        self._process_ki67_performance(N, validation_csn_list, nlp_values,
                                       validation_data)
        print('\n')
        print('number of docs:\t\t%d' % num_docs)
        print('number of patients:\t%d' % num_pats)
        return self.performance_statistics_dict