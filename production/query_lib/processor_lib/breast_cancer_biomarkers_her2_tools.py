# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 15:52:26 2022

@author: haglers
"""

#
from query_lib.processor_lib.base_lib.breast_cancer_biomarkers_tools_base \
    import Postprocessor as Postprocessor_base
  
#
class Postprocessor(Postprocessor_base):
    pass
  
#
class Preprocessor(object):

    #
    def __init__(self, static_data_object, logger_object):
        self.static_data_object = static_data_object
        self.logger_object = logger_object
    
    #
    def run_object(self, text):
        return text