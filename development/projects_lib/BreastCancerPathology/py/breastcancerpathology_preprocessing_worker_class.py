# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 14:20:35 2020

@author: haglers
"""

#
from nlp_lib.py.processor_lib.preprocessor_lib.worker_lib.preprocessing_worker_class \
    import Preprocessing_worker
from projects_lib.BreastCancerPathology.py.breastcancerpathology_preprocessor_class \
    import BreastCancerPathology_preprocessor

#
class BreastCancerPathology_preprocessing_worker(Preprocessing_worker):
    
    #
    def __init__(self, project_data, preprocess_files_flg):
        Preprocessing_worker.__init__(self, project_data, preprocess_files_flg)
        self.report_preprocessor = BreastCancerPathology_preprocessor(project_data, 'formatted')
        
    #
    def _preprocess_documents(self, raw_data_reader, start_idx, document_ctr, 
                              fail_ctr):
        document_value_dict = raw_data_reader.get_document_values()
        for data_file in document_value_dict:
            for document_value_key in sorted(document_value_dict[data_file].keys()):
                for document_value in sorted(document_value_dict[data_file][document_value_key]):
                    data_tmp = \
                        raw_data_reader.get_data_by_document_value(data_file,
                                                                   document_value_key,
                                                                   document_value)
                    document_ctr, fail_ctr = \
                        self._preprocess_document(raw_data_reader, data_tmp, 
                                                  start_idx, document_ctr,
                                                  fail_ctr)
        return document_ctr, fail_ctr
    
    #
    def _report_preprocessor(self, xml_metadata):
        return self.report_preprocessor