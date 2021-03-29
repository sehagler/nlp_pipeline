# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 13:22:11 2020

@author: haglers
"""

#
from nlp_lib.py.document_preprocessing_lib.document_preprocessing_manager_class \
    import Document_preprocessing_manager
from nlp_lib.py.worker_lib.preprocessing_worker_class \
    import Preprocessing_worker

#
class BeatAML_Waves_3_And_4_preprocessing_worker(Preprocessing_worker):
    
    #
    def __init__(self, project_data, preprocess_files_flg, password):
        Preprocessing_worker.__init__(self, project_data, preprocess_files_flg,
                                      password)
        self.beataml_report_preprocessor = Document_preprocessing_manager()
        self.beataml_report_preprocessor.beataml_report_preprocessor(project_data, 'formatted')
        self.cytogenetics_report_preprocessor = \
            Document_preprocessing_manager()
        self.cytogenetics_report_preprocessor.cytogenetics_report_preprocessor(project_data, 'formatted')
        self.hematopathology_report_preprocessor = \
            Document_preprocessing_manager()
        self.hematopathology_report_preprocessor.hematopathology_report_preprocessor(project_data, 'formatted')
        self.raw_data_manager_mode_flg = 'get_data_by_document_value'
    
    #
    def _report_preprocessor(self, xml_metadata):
        if xml_metadata['NLP_PROCESS'] == 'BEATAML_REPORT':
            report_preprocessor = self.beataml_report_preprocessor
        elif xml_metadata['NLP_PROCESS'] == 'CYTOGENETICS_REPORT':
            report_preprocessor = self.cytogenetics_report_preprocessor
        elif xml_metadata['NLP_PROCESS'] == 'HEMATOPATHOLOGY_REPORT':
            report_preprocessor = self.hematopathology_report_preprocessor
        else:
            print('invalid NLP_PROCESS')
        return report_preprocessor