# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 16:45:34 2020

@author: haglers
"""

#
import lambda_lib.tool_lib.lambda_tools as lambda_tools
    
#
def _normalize_chemical_abbreviations(text):
    text = \
        lambda_tools.contextual_lambda_conversion('alcohol(?!i)', 'alcohol', text, 'ETOH')
    text = \
        lambda_tools.initialism_lambda_conversion('butyrate esterase', text, 'BE')
    text = \
        lambda_tools.lambda_conversion('(?i)immunohistochemi(cal|stry)', text, 'IHC')
    text = \
        lambda_tools.initialism_lambda_conversion('methotrexate', text, 'MTX')
    text = \
        lambda_tools.initialism_lambda_conversion('myeloperoxidase', text, 'MPO')
    text = \
        lambda_tools.initialism_lambda_conversion('sudan black B', text, 'SBB')
    return text

#
class Preprocessor(object):

    #
    def __init__(self, static_data_object, logger_object):
        self.static_data_object = static_data_object
        self.logger_object = logger_object
        
    #
    def run_object(self, text):
        text = _normalize_chemical_abbreviations(text)
        return text