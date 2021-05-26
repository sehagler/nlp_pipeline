# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 10:18:29 2021

@author: haglers
"""

#
from nlp_lib.py.document_preprocessing_lib.report_preprocessor_lib.breast_cancer_report_preprocessor_class \
    import Breast_cancer_report_preprocessor
from nlp_lib.py.document_preprocessing_lib.report_preprocessor_lib.cytogenetics_report_preprocessor_class \
    import Cytogenetics_report_preprocessor
from nlp_lib.py.document_preprocessing_lib.report_preprocessor_lib.hematopathology_report_preprocessor_class \
    import Hematopathology_report_preprocessor
from nlp_lib.py.document_preprocessing_lib.report_preprocessor_lib.note_preprocessor_class \
    import Note_preprocessor
from nlp_lib.py.document_preprocessing_lib.report_preprocessor_lib.raw_report_preprocessor_class \
    import Raw_report_preprocessor

#
class Document_preprocessing_manager(object):
    
    #
    def __init__(self, static_data_manager):
        self.static_data = static_data_manager.get_project_data()
        self.format_flg = self.static_data['formatting']
            
    #
    def format_report(self, source_system):
        self.report_preprocessor.format_report(source_system)
            
    #
    def normalize_report(self):
        self.report_preprocessor.normalize_report()
        
    #
    def pull_dynamic_data_manager(self):
        dynamic_data_manager = \
            self.report_preprocessor.pull_dynamic_data_manager()
        return dynamic_data_manager
        
    #
    def pull_text(self):
        text = self.report_preprocessor.pull_text()
        return text
            
    #
    def push_dynamic_data_manager(self, dynamic_data_manager):
        self.report_preprocessor.push_dynamic_data_manager(dynamic_data_manager)
        
    #
    def push_text(self, text):
        self.report_preprocessor.push_text(text)
        
    #
    def raw_report_preprocessor_normalize_report(self):
        self.raw_report_preprocessor.normalize_report()
        
    #
    def raw_report_preprocessor_pull_text(self):
        text = self.raw_report_preprocessor.pull_text()
        return text
        
    #
    def raw_report_preprocessor_push_text(self, text):
        self.raw_report_preprocessor.push_text(text)
        
    #
    def set_raw_report_preprocessor(self, static_data):
        self.raw_report_preprocessor = Raw_report_preprocessor(static_data)
        
    #
    def set_report_preprocessor(self, xml_metadata):
        if xml_metadata['NLP_PROCESS'] == 'BREAST_CANCER_PATHOLOGY_REPORT':
            self.report_preprocessor = \
                Breast_cancer_report_preprocessor(self.static_data, self.format_flg)
        elif xml_metadata['NLP_PROCESS'] == 'CYTOGENETICS_REPORT':
            self.report_preprocessor = \
                Cytogenetics_report_preprocessor(self.static_data, self.format_flg)
            #self.report_preprocessor = \
            #    BeatAML_report_preprocessor(self.static_data, self.format_flg)
        elif xml_metadata['NLP_PROCESS'] == 'HEMATOPATHOLOGY_REPORT':
            self.report_preprocessor = \
                Hematopathology_report_preprocessor(self.static_data, self.format_flg)
            #self.report_preprocessor = \
            #    BeatAML_report_preprocessor(self.static_data, self.format_flg)
        elif xml_metadata['NLP_PROCESS'] == 'NOTE':
            self.report_preprocessor = \
                Note_preprocessor(self.static_data, self.format_flg)
        else:
            print('invalid NLP_PROCESS')