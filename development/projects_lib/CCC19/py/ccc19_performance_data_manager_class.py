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
        self.identifier_key = 'SOURCE_SYSTEM_DOCUMENT_ID'
        validation_data = self._read_validation_data()
        self.identifier_list = self._get_validation_csn_list(validation_data)
        self.queries = [ ('CANCER_STAGE', None, 'CANCER_STAGE', 'CANCER_STAGE', 'single_value', True),
                         ('NORMALIZED_ECOG_SCORE', None, 'ECOG_STATUS', 'NORMALIZED_ECOG_SCORE', 'single_value', True),
                         ('NORMALIZED_SMOKING_HISTORY', None, 'SMOKING_HISTORY', 'NORMALIZED_SMOKING_HISTORY', 'single_value', True),
                         ('NORMALIZED_SMOKING_PRODUCTS', None, 'SMOKING_PRODUCTS', 'NORMALIZED_SMOKING_PRODUCTS', 'multiple_values', False),
                         ('NORMALIZED_SMOKING_STATUS', None, 'SMOKING_STATUS', 'NORMALIZED_SMOKING_STATUS', 'single_value', True) ]
                
    #
    def _get_smoking_products_performance(self, csn, nlp_values, nlp_datum_key,
                                          validation_data, validation_datum_key):
            data_out = nlp_values[csn]
            if data_out is not None:
                if nlp_datum_key in data_out.keys():
                    nlp_smoking_products_value = \
                        data_out[nlp_datum_key]
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
            nlp_smoking_products_value = \
                self._nlp_to_tuple(nlp_smoking_products_value)
            validation_smoking_products_value = \
                self._validation_to_tuple(validation_smoking_products_value)
            performance, flg = \
                self._compare_data_values(nlp_smoking_products_value,
                                          validation_smoking_products_value)
            return performance
    
    #
    def _process_performance(self, nlp_values, validation_data):
        validation_csn_list = \
            self._get_validation_csn_list(validation_data)
        nlp_performance_dict = {}
        for i in range(len(self.queries)):
            validation_datum_key = self.queries[i][0]
            nlp_performance_dict[validation_datum_key] = []
        for csn in validation_csn_list:
            print(csn)
            for i in range(len(self.queries)):
                nlp_datum_key = self.queries[i][3]
                validation_datum_key = self.queries[i][0]
                if validation_datum_key == 'NORMALIZED_SMOKING_PRODUCTS':
                    performance = self._get_smoking_products_performance(csn,
                                                                         nlp_values,
                                                                         nlp_datum_key,
                                                                         validation_data,
                                                                         validation_datum_key)
                else:
                    performance = self._get_performance(csn, nlp_values,
                                                        nlp_datum_key,
                                                        validation_data,
                                                        validation_datum_key)
                nlp_performance_dict[validation_datum_key].append(performance)
        N = len(validation_csn_list)
        for key in nlp_performance_dict.keys():
            FN, FP, FP_plus_FN, TN, TP = \
                self._performance_values(nlp_performance_dict[key])
            self.performance_statistics_dict[key] = \
                self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
        
    #
    def _read_validation_data(self):
        validation_filename = 'ccc19_testing.xlsx'
        directory_manager = self.static_data['directory_manager']
        if 'patient_list' in self.static_data.keys():
            patient_list = self.static_data['patient_list']
        else:
            patient_list = None
        data_dir = directory_manager.pull_directory('raw_data_dir')
        book = read_xlsx_file(os.path.join(data_dir, validation_filename))
        sheet = book.sheet_by_index(0)
        ncols = sheet.ncols
        nrows = sheet.nrows
        validation_data = []
        for row_idx in range(nrows):
            validation_data_tmp = []
            for col_idx in range(ncols):
                cell_value = sheet.cell_value(row_idx, col_idx)
                try:
                    cell_value = str(int(cell_value))
                except:
                    pass
                validation_data_tmp.append(cell_value)
            validation_data.append(validation_data_tmp)
        return validation_data