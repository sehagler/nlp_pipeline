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
class AdverseEvents_preprocessing_worker(Preprocessing_worker):
    
    #
    def __init__(self, project_data, preprocess_files_flg, password):
        Preprocessing_worker.__init__(self, project_data, preprocess_files_flg,
                                      password)
        self.note_preprocessor = Document_preprocessing_manager()
        self.note_preprocessor.note_preprocessor(project_data, 'unformatted')
        self.pathology_report_preprocessor = Document_preprocessing_manager()
        self.pathology_report_preprocessor.pathology_report_preprocessor(project_data, 'unformatted')
        self.raw_data_manager_mode_flg = 'get_data_by_document_number'
    
    #
    def _report_preprocessor(self, xml_metadata):
        if xml_metadata['NLP_PROCESS'] == 'NOTE':
            report_preprocessor = self.note_preprocessor
        else:
            report_preprocessor = self.pathology_report_preprocessor
        return report_preprocessor