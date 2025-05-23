# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 11:19:40 2020

@author: haglers
"""

#
import lambda_lib.tool_lib.lambda_tools as lambda_tools
from tools_lib.regex_lib.regex_tools import s
from tools_lib.processing_tools_lib.function_processing_tools \
    import sequential_composition
    
#
pre_punct = '\n'
    
#
def _normalize_atypical_cell(text):
    text = \
        lambda_tools.lambda_conversion(pre_punct + 'atyp cell' + s(), text, '\nATYPICAL CELL')
    text = \
        lambda_tools.lambda_conversion(pre_punct + 'atypical cell' + s() + ' %', text, '\nATYPICAL CELL%')
    return text

#
def _normalize_basophil(text):
    text = \
        lambda_tools.lambda_conversion(pre_punct + 'baso' + s() + '[ \t]', text, '\nBASOPHIL')
    text = \
        lambda_tools.lambda_conversion(pre_punct + '(% )?basophil' + s(), text, '\nBASOPHIL%')
    text = \
        lambda_tools.lambda_conversion(pre_punct + 'basophil (#|% abs)', text, '\nBASOPHIL#')
    return text

#
def _normalize_blood(text):
    text = \
        lambda_tools.lambda_conversion(pre_punct + 'hematocrit', text, '\nHCT')
    text = \
        lambda_tools.lambda_conversion(pre_punct + 'hemoglobin', text, '\nHGB')
    text = \
        lambda_tools.lambda_conversion(pre_punct + 'plt', text, '\nPLT')
    text = \
        lambda_tools.lambda_conversion(pre_punct + 'PLATELET COUNT', text, '\nPLT')
    text = \
        lambda_tools.lambda_conversion(pre_punct + 'RED CELL COUNT', text, '\nRBC')
    text = \
        lambda_tools.lambda_conversion(pre_punct + 'WHITE CELL COUNT', text, '\nWBC')
    return text

#
def _normalize_eosinophil(text):
    text = \
        lambda_tools.lambda_conversion(pre_punct + 'eos[ \t]', text, '\nEOSINOPHIL ')
    text = \
        lambda_tools.lambda_conversion(pre_punct + '(% )?eosinophil' + s(), text, '\nEOSINOPHIL%')
    text = \
        lambda_tools.lambda_conversion(pre_punct + 'eosinphil (#|% abs)', text, '\nEOSINOPHIL#')
    text = \
        lambda_tools.lambda_conversion(pre_punct + 'eos abs', text, '\nEOSINOPHIL#')
    return text

#
def _normalize_ig(text):
    text = \
        lambda_tools.lambda_conversion(pre_punct + 'ig #', text, 'IG#')
    text = \
        lambda_tools.lambda_conversion(pre_punct + 'ig %', text, 'IG%')
    return text

#
def _normalize_lymphocyte(text):
    text = \
        lambda_tools.lambda_conversion(pre_punct + 'lymphs', text, '\nLYMPHOCYTE')
    text = \
        lambda_tools.lambda_conversion(pre_punct + '(% )?lymphocyte' + s(), text, '\nLYMPHOCYTE%')
    text = \
        lambda_tools.lambda_conversion(pre_punct + '(ly#|lymph abs)', text, '\nLYMPHOCYTE#')
    return text

#
def _normalize_monocyte(text):
    text = \
        lambda_tools.lambda_conversion(pre_punct + 'mono #', text, '\nMONOCYTE#')
    text = \
        lambda_tools.lambda_conversion(pre_punct + 'mono %', text, '\nMONOCYTE%')
    text = \
        lambda_tools.lambda_conversion(pre_punct + 'monos', text, '\nMONOCYTE')
    text = \
        lambda_tools.lambda_conversion(pre_punct + '(% )?monocyte' + s(), text, '\nMONOCYTE%')
    text = \
        lambda_tools.lambda_conversion(pre_punct + '(% )?monocyte %', text, '\nMONOCYTE%')
    text = \
        lambda_tools.lambda_conversion(pre_punct + 'monocyte% abs', text, '\nMONOCYTE#')
    return text

#
def _normalize_myelocyte(text):
    text = \
        lambda_tools.lambda_conversion(pre_punct + '(% )?myelocyte' + s(), text, '\nMYELOCYTE')
    text = \
        lambda_tools.lambda_conversion(pre_punct + '(% )?myelocyte %', text, '\nMYELOCYTE%')
    return text

#
def _normalize_neutrophil(text):
    text = \
        lambda_tools.lambda_conversion(pre_punct + '(% )?neutrophils', text, '\nNEUTROPHIL%')
    text = \
        lambda_tools.lambda_conversion(pre_punct + '(ne#|neut abs)', text, '\nNEUTROPHIL#')
    return text
                          
#
def _normalize_nrbc(text):
    text = \
        lambda_tools.lambda_conversion(pre_punct + 'nrbc #', text, 'NRBC#')
    text = \
        lambda_tools.lambda_conversion(pre_punct + 'nrbc %', text, 'NRBC%')
    return text

#
def _normalize_poc(text):
    text = \
        lambda_tools.deletion_lambda_conversion('(?i),? POC', text)
    return text
   
#
def table_normalizer(text):
    text = sequential_composition([_normalize_atypical_cell,
                                   _normalize_basophil,
                                   _normalize_blood,
                                   _normalize_eosinophil,
                                   _normalize_ig,
                                   _normalize_lymphocyte,
                                   _normalize_monocyte,
                                   _normalize_myelocyte,
                                   _normalize_neutrophil,
                                   _normalize_nrbc,
                                   _normalize_poc], text)
    return text