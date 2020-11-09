# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 09:44:25 2018

@author: haglers
"""

#
import re

#
from nlp_lib.py.template_lib.preprocessor_template_lib.pathology_report_class import Pathology_report
from nlp_lib.py.tool_lib.query_tools_lib.karyotype_tools import Named_entity_recognition as Named_entity_recognition_karyotype

#
class Cytogenetics_report(Pathology_report):
    
    #
    def _named_entity_recognition(self):
        Pathology_report._named_entity_recognition(self)
        named_entity_recognition_karyotype = Named_entity_recognition_karyotype()
        named_entity_recognition_karyotype.push_text(self.text)
        named_entity_recognition_karyotype.process_karyotype()
        self.text = named_entity_recognition_karyotype.pull_text()
        self._normalize_whitespace()
