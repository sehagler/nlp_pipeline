# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 09:44:25 2018

@author: haglers
"""

#
from nlp_lib.py.base_class_lib.preprocessor_base_class import Preprocessor_base
from nlp_lib.py.processor_lib.preprocessor_lib.deidentifier_lib.deidentifier_class \
    import Deidentifier

#
class Raw_report_preprocessor(Preprocessor_base):
    
    #
    def __init__(self):
        pass
    
    #
    def _deidentifier(self):
        deidentifier = Deidentifier()
        deidentifier.push_text(self.text)
        deidentifier.remove_phi()
        self.text = deidentifier.pull_text()

    #
    def normalize_report(self):
        self._make_text_ascii()
        self._deidentifier()
        self._make_text_xml_compatible()