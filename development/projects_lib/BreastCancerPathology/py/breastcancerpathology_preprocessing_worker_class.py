# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 14:20:35 2020

@author: haglers
"""

#
from nlp_lib.py.document_preprocessing_lib.document_preprocessing_manager_class \
    import Document_preprocessing_manager
from nlp_lib.py.worker_lib.preprocessing_worker_class \
    import Preprocessing_worker

#
class BreastCancerPathology_preprocessing_worker(Preprocessing_worker):
    
    #
    def __init__(self, project_data, preprocess_files_flg, password):
        Preprocessing_worker.__init__(self, project_data, preprocess_files_flg,
                                      password)
        self.report_preprocessor = Document_preprocessing_manager()
        self.report_preprocessor.breastcancerpathology_report_preprocessor(project_data, 'formatted')
        self.raw_data_manager_mode_flg = 'get_data_by_document_value'
    
    #
    def _report_preprocessor(self, xml_metadata):
        return self.report_preprocessor