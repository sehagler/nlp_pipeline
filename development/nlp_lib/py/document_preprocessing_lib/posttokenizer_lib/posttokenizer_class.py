# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 10:50:58 2021

@author: haglers
"""

#
from nlp_lib.py.document_preprocessing_lib.base_class_lib.preprocessor_base_class \
    import Preprocessor_base
from tool_lib.py.query_tools_lib.antigens_tools \
    import Posttokenizer as Posttokenizer_antigens
from tool_lib.py.query_tools_lib.cancer_tools \
    import Posttokenizer as Posttokenizer_cancer
from tool_lib.py.query_tools_lib.karyotype_tools \
    import Posttokenizer as Posttokenizer_karyotype
from tool_lib.py.query_tools_lib.histological_grade_tools \
    import Posttokenizer as Posttokenizer_histological_grade

#
class Posttokenizer(Preprocessor_base):
    
    #
    def __init__(self, static_data):
        Preprocessor_base.__init__(self, static_data)
        self.posttokenizer_antigens = Posttokenizer_antigens(self.static_data)
        self.posttokenizer_cancer = Posttokenizer_cancer(self.static_data)
        self.posttokenizer_histological_grade = \
            Posttokenizer_histological_grade(self.static_data)
        self.posttokenizer_karyotype = \
            Posttokenizer_karyotype(self.static_data)
    
    #
    def _process_general(self):
        self._general_command(' M [:/] E ', {None : ' M:E '})
        self._general_command(' N [:/] C ', {None : ' N:C '})
        self._general_command('(?i) n / a ', {None : ' n/a '})
        
    #
    def _process_medical_abbreviations(self):
        self._general_command('(?i) f / u ', {None : ' f/u '})
        self._general_command('(?i) h / o ', {None : ' h/o '})
        self._general_command('(?i) s / p ', {None : ' s/p '})
    
    #
    def process_document(self, text):
        self.text = text
        self._normalize_whitespace()
        self._process_general()
        self._process_medical_abbreviations()
        self._normalize_whitespace()  
        #self._clear_section_header_tags()
        self.posttokenizer_antigens.push_text(self.text)
        self.posttokenizer_antigens.process_antigens()
        self.text = self.posttokenizer_antigens.pull_text()
        self.posttokenizer_cancer.push_text(self.text)
        self.posttokenizer_cancer.process_general()
        self.text = self.posttokenizer_cancer.pull_text()
        self.posttokenizer_histological_grade.push_text(self.text)
        self.posttokenizer_histological_grade.process_grade()
        self.text = self.posttokenizer_histological_grade.pull_text()
        self.posttokenizer_karyotype.push_text(self.text)
        self.posttokenizer_karyotype.process_karyotype()
        self.text = self.posttokenizer_karyotype.pull_text()
        self._clear_command_list()
        self._general_command('\( [0-9]+ - [0-9]+ \)', {' \)' : '.0 )'})
        self._general_command('\( [0-9]+ - [0-9]+\.[0-9]+ \)', {' - ' : '.0 - '})
        self._general_command('day 0( is equal to | ?= ?)', {None : ''})
        self._process_command_list()
        #self._clear_section_header_tags()
        return self.text