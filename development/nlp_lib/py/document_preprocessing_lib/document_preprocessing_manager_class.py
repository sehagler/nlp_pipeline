# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 10:18:29 2021

@author: haglers
"""

#
from nlp_lib.py.document_preprocessing_lib.report_preprocessor_lib.beataml_report_preprocessor_class \
    import BeatAML_report_preprocessor
from nlp_lib.py.document_preprocessing_lib.report_preprocessor_lib.breastcancerpathology_report_preprocessor_class \
    import BreastCancerPathology_report_preprocessor
from nlp_lib.py.document_preprocessing_lib.report_preprocessor_lib.ccc19_note_preprocessor_class \
    import CCC19_note_preprocessor
from nlp_lib.py.document_preprocessing_lib.report_preprocessor_lib.cytogenetics_report_preprocessor_class \
    import Cytogenetics_report_preprocessor
from nlp_lib.py.document_preprocessing_lib.report_preprocessor_lib.hematopathology_report_preprocessor_class \
    import Hematopathology_report_preprocessor
from nlp_lib.py.document_preprocessing_lib.template_lib.preprocessor_template_lib.note_template_class \
    import Note_template
from nlp_lib.py.document_preprocessing_lib.template_lib.preprocessor_template_lib.pathology_report_class \
    import Pathology_report
from nlp_lib.py.document_preprocessing_lib.template_lib.preprocessor_template_lib.raw_report_preprocessor_class \
    import Raw_report_preprocessor

#
class Document_preprocessing_manager(object):
    
    #
    def __init__(self, static_data_manager):
        self.static_data = static_data_manager.get_project_data()
        self.format_flg = self.static_data['formatting']
    
    '''
    #
    def beataml_report_preprocessor(self):
        self.report_preprocessor = \
            BeatAML_report_preprocessor(self.static_data, self.format_flg)
            
    #
    def breastcancerpathology_report_preprocessor(self):
        self.report_preprocessor = \
            BreastCancerPathology_report_preprocessor(self.static_data, self.format_flg)
            
    #
    def ccc19_note_preprocessor(self):
        self.report_preprocessor = \
            CCC19_note_preprocessor(self.static_data, self.format_flg)
            
    #
    def cytogenetics_report_preprocessor(self):
        self.report_preprocessor = \
            Cytogenetics_report_preprocessor(self.static_data, self.format_flg)
    '''
            
    #
    def format_report(self, source_system):
        self.report_preprocessor.format_report(source_system)
            
    '''
    #
    def hematopathology_report_preprocessor(self):
        self.report_preprocessor = \
            Hematopathology_report_preprocessor(self.static_data, self.format_flg)
    '''
            
    #
    def normalize_report(self):
        self.report_preprocessor.normalize_report()
        
    '''
    #
    def note_preprocessor(self):
        self.report_preprocessor = \
            Note_template(self.static_data, self.format_flg)
            
    #
    def pathology_report_preprocessor(self):
        self.report_preprocessor = \
            Pathology_report(self.static_data, self.format_flg)
    '''
        
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
        if xml_metadata['NLP_PROCESS'] == 'BEATAML_REPORT':
            #self.beataml_report_preprocessor()
            self.report_preprocessor = \
                BeatAML_report_preprocessor(self.static_data, self.format_flg)
        elif xml_metadata['NLP_PROCESS'] == 'BREAST_CANCER_PATHOLOGY_REPORT':
            #self.breastcancerpathology_report_preprocessor()
            self.report_preprocessor = \
                BreastCancerPathology_report_preprocessor(self.static_data, self.format_flg)
        elif xml_metadata['NLP_PROCESS'] == 'CCC19_NOTE':
            #self.ccc19_note_preprocessor()
            self.report_preprocessor = \
                CCC19_note_preprocessor(self.static_data, self.format_flg)
        elif xml_metadata['NLP_PROCESS'] == 'CYTOGENETICS_REPORT':
            #self.cytogenetics_report_preprocessor()
            self.report_preprocessor = \
                Cytogenetics_report_preprocessor(self.static_data, self.format_flg)
        elif xml_metadata['NLP_PROCESS'] == 'HEMATOPATHOLOGY_REPORT':
            #self.hematopathology_report_preprocessor()
            self.report_preprocessor = \
                Hematopathology_report_preprocessor(self.static_data, self.format_flg)
        elif xml_metadata['NLP_PROCESS'] == 'NOTE':
            #self.note_preprocessor()
            self.report_preprocessor = \
                Note_template(self.static_data, self.format_flg)
        else:
            print('invalid NLP_PROCESS')