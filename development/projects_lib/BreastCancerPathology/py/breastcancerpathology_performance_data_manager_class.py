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
class BreastCancerPathology_performance_data_manager(Performance_data_manager):
    
    #
    def __init__(self, project_manager):
        project_data = project_manager.get_project_data()
        Performance_data_manager.__init__(self, project_manager)
        self.project_data = project_data
    
    #
    def _get_nlp_data(self, data_in):
        data_out = {}
        data_out['ER_SCORE'] = \
            self._get_data_value(data_in, None, 'BIOMARKERS_' + self.nlp_value_key, 'ER_SCORE', mode_flg='single_value')
        if data_out['ER_SCORE'] is not None:
            data_out['ER_SCORE'] = data_out['ER_SCORE'][0]
        data_out['ER_STATUS'] = \
            self._get_data_value(data_in, None, 'BIOMARKERS_' + self.nlp_value_key, 'ER_STATUS', mode_flg='single_value')
        if data_out['ER_STATUS'] is not None:
            data_out['ER_STATUS'] = data_out['ER_STATUS'][0]
        data_out['HER2_SCORE'] = \
            self._get_data_value(data_in, None, 'BIOMARKERS_' + self.nlp_value_key, 'HER2_SCORE', mode_flg='single_value')
        if data_out['HER2_SCORE'] is not None:
            data_out['HER2_SCORE'] = data_out['HER2_SCORE'][0]
        data_out['HER2_STATUS'] = \
            self._get_data_value(data_in, None, 'BIOMARKERS_' + self.nlp_value_key, 'HER2_STATUS', mode_flg='single_value')
        if data_out['HER2_STATUS'] is not None:
            data_out['HER2_STATUS'] = data_out['HER2_STATUS'][0]
        data_out['PR_SCORE'] = \
            self._get_data_value(data_in, None, 'BIOMARKERS_' + self.nlp_value_key, 'PR_SCORE', mode_flg='single_value')
        if data_out['PR_SCORE'] is not None:
            data_out['PR_SCORE'] = data_out['PR_SCORE'][0]
        data_out['PR_STATUS'] = \
            self._get_data_value(data_in, None, 'BIOMARKERS_' + self.nlp_value_key, 'PR_STATUS', mode_flg='single_value')
        if data_out['PR_STATUS'] is not None:
            data_out['PR_STATUS'] = data_out['PR_STATUS'][0]
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
    def _read_validation_data(self, project_data):
        directory_manager = project_data['directory_manager']
        if 'patient_list' in project_data.keys():
            patient_list = project_data['patient_list']
        else:
            patient_list = None
        project_name = project_data['project_name']
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
        nlp_data = self.nlp_data
        validation_data = self._read_validation_data(self.project_data)
        if 'document_list' in self.project_data.keys():
            csn_list = self.project_data['document_list']
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
        nlp_er_score_performance = []
        nlp_er_status_performance = []
        nlp_her2_score_performance = []
        nlp_her2_status_performance = []
        nlp_pr_score_performance = []
        nlp_pr_status_performance = []
        for csn in validation_csn_list:
            data_out = nlp_values[csn]
            print(csn)
            if data_out is not None:
                if 'ER_SCORE' in data_out.keys():
                    nlp_er_score_value = data_out['ER_SCORE']
                else:
                    nlp_er_score_value = None
                if 'ER_STATUS' in data_out.keys():
                    nlp_er_status_value = data_out['ER_STATUS']
                else:
                    nlp_er_status_value = None
                if 'HER2_SCORE' in data_out.keys():
                    nlp_her2_score_value = data_out['HER2_SCORE']
                else:
                    nlp_her2_score_value = None
                if 'HER2_STATUS' in data_out.keys():
                    nlp_her2_status_value = data_out['HER2_STATUS']
                else:
                    nlp_her2_status_value = None
                if 'PR_SCORE' in data_out.keys():
                    nlp_pr_score_value = data_out['PR_SCORE']
                else:
                    nlp_pr_score_value = None
                if 'PR_STATUS' in data_out.keys():
                    nlp_pr_status_value = data_out['PR_STATUS']
                else:
                    nlp_pr_status_value = None
            else:
                nlp_er_score_value = None
                nlp_er_status_value = None
                nlp_her2_score_value = None
                nlp_her2_status_value = None
                nlp_pr_score_value = None
                nlp_pr_status_value = None
            for item in validation_data:
                if item[2] == csn:
                    validation_er_score_value = \
                        self._process_validation_item(item[4])
                    validation_er_status_value = \
                        self._process_validation_item(item[3])
                    validation_her2_score_value = \
                        self._process_validation_item(item[9])
                    validation_her2_status_value = \
                        self._process_validation_item(item[8])
                    validation_pr_score_value = \
                        self._process_validation_item(item[6])
                    validation_pr_status_value = \
                        self._process_validation_item(item[5])
            if validation_er_status_value is not None:
                validation_er_status_value = \
                    tuple(validation_er_status_value.split(', '))
            if validation_er_score_value is not None:
                validation_er_score_value = \
                    tuple(validation_er_score_value.split(', '))
            if validation_her2_status_value is not None:
                validation_her2_status_value = \
                    tuple(validation_her2_status_value.split(', '))
            if validation_her2_score_value is not None:
                validation_her2_score_value = \
                    tuple(validation_her2_score_value.split(', '))
            if validation_pr_status_value is not None:
                validation_pr_status_value = \
                    tuple(validation_pr_status_value.split(', '))
            if validation_pr_score_value is not None:
                validation_pr_score_value = \
                    tuple(validation_pr_score_value.split(', '))
            display_data_flg = True
            print(nlp_er_status_value)
            print(validation_er_status_value)
            print('')
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
            if False:
                if display_data_flg:
                    print(csn)
        if True:
            performance_statistics_dict = {}
            num_docs = len(validation_csn_list)
            num_pats = len(validation_mrn_list)
            N = num_docs
            FN, FP, FP_plus_FN, TN, TP = \
                self._performance_values(nlp_er_status_performance)
            performance_statistics_dict['ER_STATUS'] = \
                self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
            FN, FP, FP_plus_FN, TN, TP = \
                self._performance_values(nlp_er_score_performance)
            performance_statistics_dict['ER_SCORE'] = \
                self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
            FN, FP, FP_plus_FN, TN, TP = \
                self._performance_values(nlp_her2_status_performance)
            performance_statistics_dict['HER2_STATUS'] = \
                self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
            FN, FP, FP_plus_FN, TN, TP = \
                self._performance_values(nlp_her2_score_performance)
            performance_statistics_dict['HER2_SCORE'] = \
                self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
            FN, FP, FP_plus_FN, TN, TP = \
                self._performance_values(nlp_pr_status_performance)
            performance_statistics_dict['PR_STATUS'] = \
                self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
            FN, FP, FP_plus_FN, TN, TP = \
                self._performance_values(nlp_pr_score_performance)
            performance_statistics_dict['PR_SCORE'] = \
                self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
            print('\n')
            print('number of docs:\t\t%d' % num_docs)
            print('number of patients:\t%d' % num_pats)
        return performance_statistics_dict