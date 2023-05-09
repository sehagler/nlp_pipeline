# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 16:45:34 2020

@author: haglers
"""

#
import lambda_lib.tool_lib.lambda_tools as lambda_tools
from tools_lib.processing_tools_lib.function_processing_tools \
    import sequential_composition
from tools_lib.regex_lib.regex_tools \
    import (
        regex_from_list,
        s
    )
    
#
def _cleanup_text(text):
    text = \
        lambda_tools.lambda_conversion('Scarff ', text, 'Scarf ')
    return text
    
#
def _normalize_text(text):
    text = \
        lambda_tools.lambda_conversion('leukaemia', text, 'leukemia')
    text = \
        lambda_tools.lambda_conversion('(?<=[Tt])umour', text, 'umor')
    return text

#
def _setup_text(text):
    text = \
        lambda_tools.contextual_lambda_conversion('Scharff(-| )', '(?i)Scharff', text, 'Scarff')
    text = \
        lambda_tools.contextual_lambda_conversion('Scharf(-| )', '(?i)Scharf', text, 'Scarff')
    text = \
        lambda_tools.contextual_lambda_conversion('Scarf(-| )', '(?i)Scarf', text, 'Scarff')
    return text

#
def _process_irregular_initialisms(text):
    
    # breast cancer
    text = \
        lambda_tools.lambda_conversion('(?i)in situ and invasive duct(al)? (cancer|carcinoma)', text, 'DCIS and IDC')
    text = \
        lambda_tools.lambda_conversion('(?i)usual and atypical duct(al)? hyperplasia( \( UDH, ADH \))?', text, 'UDH and ADH')
    
    return text
    
#
def _process_regular_initialisms(text):
    
    # carcinoma
    text = \
        lambda_tools.lambda_conversion('(?i)sqcc', text, 'SCC')
    carcinoma_list = [ [ 'duct(al)? (cancer|carcinoma)', 'DC' ],
                       [ 'lobular (cancer|carcinoma)', 'LC' ],
                       [ 'renal cell (cancer|carcinoma)', 'RCC' ],
                       [ 'solid papillary (cancer|carcinoma)', 'SPC' ],
                       [ 'squamous cell (cancer|carcinoma)', 'SCC' ],
                       [ 'transitional cell (cancer|carcinoma)', 'TCC' ] ]
    for carcinoma in carcinoma_list:
        text = \
            lambda_tools.initialism_lambda_conversion('(infiltrating|invasive) ' + carcinoma[0], text, 'I' + carcinoma[1])
        text = \
            lambda_tools.initialism_lambda_conversion(carcinoma[0] + ' in situ', text, carcinoma[1] + 'IS')
        text = \
            lambda_tools.initialism_lambda_conversion(carcinoma[0], text, carcinoma[1])
        text = \
            lambda_tools.initialism_lambda_conversion('(infiltrating|invasive) ' + carcinoma[1], text, 'I' + carcinoma[1])
        text = \
            lambda_tools.initialism_lambda_conversion(carcinoma[1] + ' in situ', text, carcinoma[1] + 'IS')
            
    # glaucoma
    text = \
        lambda_tools.initialism_lambda_conversion('primary open angle glaucoma', text, 'POAG')
    
    # hyperplasia
    hyperplasia_list = [ [ 'duct(al)? hyperplasia', 'DH' ],
                         [ 'lobular hyperplasia', 'LH' ],
                         [ 'columnar cell hyperplasia', 'CCH' ] ]
    for hyperplasia in hyperplasia_list:
        text = \
            lambda_tools.initialism_lambda_conversion('atypical ' + hyperplasia[0], text, 'A' + hyperplasia[1])
        text = \
            lambda_tools.initialism_lambda_conversion('usual ' + hyperplasia[0], text, 'U' + hyperplasia[1])
        text = \
            lambda_tools.initialism_lambda_conversion(hyperplasia[0], text, hyperplasia[1])
    
    # leukemia
    text = \
        lambda_tools.initialism_lambda_conversion('acute myeloid leukemia', text, 'AML')
    text = \
        lambda_tools.initialism_lambda_conversion('acute myelomonocytic leukemia', text, 'AMML')
    text = \
        lambda_tools.initialism_lambda_conversion('chronic lymphocytic leukemia', text, 'CLL')
    
    # myeloma
    text = \
        lambda_tools.initialism_lambda_conversion('multiple myeloma', text, 'MM')
    
    # neoplasm
    text = \
        lambda_tools.initialism_lambda_conversion('myelodysplastic / myeloproliferative (disease|neoplasm)', text, 'MDS/MPN')
    text = \
        lambda_tools.initialism_lambda_conversion('myeloproliferative / myelodysplastic (disease|neoplasm)', text, 'MDS/MPN')
    text = \
        lambda_tools.initialism_lambda_conversion('myeloproliferative neoplasm', text, 'MPN')
    
    # sarcoma
    text = \
        lambda_tools.initialism_lambda_conversion('undifferentiated pleomorphic sarcoma', text, 'UPS')
    
    # tumor
    text = \
        lambda_tools.initialism_lambda_conversion('isolated tumor cell' + s(), text, 'ITC')
    
    return text
    
#
def get_initialisms():
    initialism_list = [ 'CHH', 'CLL', 'DC', 'DH', 'DLBCL', 'GIST',
                        '(R(\-)?)?ISS', 'ITC', 'LC', 'LH', 'MM', 'NET', 'NSCLC',
                        'RCC', 'SCC', 'SCLC', 'SLL', 'SPC', 'TCC', 'UPS' ]
    return '([AIU])?' + regex_from_list(initialism_list)
    
#
def nonnumeric_stage():
    stage_list = [ 'advanced', 'early', 'end', 'extensive', 'mild', 'moderate',
                   'severe' ]
    return regex_from_list(stage_list)

#
def numeric_stage():
    stage_base = '[0-9IV]{1,3}([A-Za-z]([0-9])?)?'
    numeric_stage = stage_base + '((-|/)' + stage_base + ')?'
    return numeric_stage

#
class Preprocessor(object):
        
    #
    def process_abbreviations(self):
        pass
        
    #
    def run_preprocessor(self, text):
        text = \
            lambda_tools.lambda_conversion('MDS / MPN', text, 'MDS/MPN')
        text = sequential_composition([_process_irregular_initialisms,
                                       _process_regular_initialisms,
                                       _setup_text,
                                       _normalize_text,
                                       _cleanup_text], text)
        return text