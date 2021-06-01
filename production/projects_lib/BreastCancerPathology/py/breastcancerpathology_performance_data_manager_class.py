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
        data_out['ER'] = \
            self._get_data_value(data_in, None, 'BIOMARKERS_' + self.nlp_value_key, 'ER', mode_flg='single_value')
        data_out['HER2'] = \
            self._get_data_value(data_in, None, 'BIOMARKERS_' + self.nlp_value_key, 'HER2', mode_flg='single_value')
        data_out['PR'] = \
            self._get_data_value(data_in, None, 'BIOMARKERS_' + self.nlp_value_key, 'PR', mode_flg='single_value')
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
        nlp_er_performance = []
        nlp_her2_performance = []
        nlp_pr_performance = []
        for csn in validation_csn_list:
            data_out = nlp_values[csn]
            if data_out is not None:
                if 'ER' in data_out.keys():
                    nlp_er_value = data_out['ER']
                else:
                    nlp_er_value = None
                if 'HER2' in data_out.keys():
                    nlp_her2_value = data_out['HER2']
                else:
                    nlp_her2_value = None
                if 'PR' in data_out.keys():
                    nlp_pr_value = data_out['PR']
                else:
                    nlp_pr_value = None
            else:
                nlp_er_value = None
                nlp_her2_value = None
                nlp_pr_value = None
            for item in validation_data:
                if item[2] == csn:
                    validation_er_value = \
                        self._process_validation_item(item[3])
                    validation_her2_value = \
                        self._process_validation_item(item[5])
                    validation_pr_value = \
                        self._process_validation_item(item[4])
            if validation_er_value is not None:
                validation_er_value = tuple(validation_er_value.split(', '))
            if validation_her2_value is not None:
                validation_her2_value = tuple(validation_her2_value.split(', '))
            if validation_pr_value is not None:
                validation_pr_value = tuple(validation_pr_value.split(', '))
            display_data_flg = True
            performance, flg = \
                self._compare_data_values(nlp_er_value, validation_er_value)
            nlp_er_performance.append(performance)
            if flg:
                display_data_flg = True
            performance, flg = \
                self._compare_data_values(nlp_her2_value, validation_her2_value)
            nlp_her2_performance.append(performance)
            if flg:
                display_data_flg = True
            performance, flg = \
                self._compare_data_values(nlp_pr_value, validation_pr_value)
            nlp_pr_performance.append(performance)
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
                self._performance_values(nlp_er_performance)
            performance_statistics_dict['ER'] = \
                self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
            FN, FP, FP_plus_FN, TN, TP = \
                self._performance_values(nlp_her2_performance)
            performance_statistics_dict['HER2'] = \
                self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
            FN, FP, FP_plus_FN, TN, TP = \
                self._performance_values(nlp_pr_performance)
            performance_statistics_dict['PR'] = \
                self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
            print('\n')
            print('number of docs:\t\t%d' % num_docs)
            print('number of patients:\t%d' % num_pats)
        return performance_statistics_dict