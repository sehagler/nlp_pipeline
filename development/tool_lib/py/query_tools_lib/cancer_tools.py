# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 16:45:34 2020

@author: haglers
"""

#
from nlp_text_normalization_lib.base_lib.preprocessor_base_class \
    import Preprocessor_base
from tool_lib.py.processing_tools_lib.text_processing_tools \
    import regex_from_list, s

#
class Named_entity_recognition(Preprocessor_base):
    
    #
    def _process_irregular_initialisms(self):
        
        # breast cancer
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)in situ and invasive duct(al)? (cancer|carcinoma)', self.text, 'DCIS and IDC')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)usual and atypical duct(al)? hyperplasia( \( UDH, ADH \))?', self.text, 'UDH and ADH')
        
    #
    def _process_regular_initialisms(self):
        
        # carcinoma
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)sqcc', self.text, 'SCC')
        carcinoma_list = [ [ 'duct(al)? (cancer|carcinoma)', 'DC' ],
                           [ 'lobular (cancer|carcinoma)', 'LC' ],
                           [ 'renal cell (cancer|carcinoma)', 'RCC' ],
                           [ 'solid papillary (cancer|carcinoma)', 'SPC' ],
                           [ 'squamous cell (cancer|carcinoma)', 'SCC' ],
                           [ 'transitional cell (cancer|carcinoma)', 'TCC' ] ]
        for carcinoma in carcinoma_list:
            self.text = \
                self.lambda_manager.initialism_lambda_conversion('invasive ' + carcinoma[0], self.text, 'I' + carcinoma[1])
            self.text = \
                self.lambda_manager.initialism_lambda_conversion(carcinoma[0] + ' in situ', self.text, carcinoma[1] + 'IS')
            self.text = \
                self.lambda_manager.initialism_lambda_conversion(carcinoma[0], self.text, carcinoma[1])
            self.text = \
                self.lambda_manager.initialism_lambda_conversion('invasive ' + carcinoma[1], self.text, 'I' + carcinoma[1])
            self.text = \
                self.lambda_manager.initialism_lambda_conversion(carcinoma[1] + ' in situ', self.text, carcinoma[1] + 'IS')
        
        # hyperplasia
        hyperplasia_list = [ [ 'duct(al)? hyperplasia', 'DH' ],
                             [ 'lobular hyperplasia', 'LH' ],
                             [ 'columnar cell hyperplasia', 'CCH' ] ]
        for hyperplasia in hyperplasia_list:
            self.text = \
                self.lambda_manager.initialism_lambda_conversion('atypical ' + hyperplasia[0], self.text, 'A' + hyperplasia[1])
            self.text = \
                self.lambda_manager.initialism_lambda_conversion('usual ' + hyperplasia[0], self.text, 'U' + hyperplasia[1])
            self.text = \
                self.lambda_manager.initialism_lambda_conversion(hyperplasia[0], self.text, hyperplasia[1])
        
        # leukemia
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('acute myeloid leukemia', self.text, 'AML')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('acute myelomonocytic leukemia', self.text, 'AMML')
        
        # myeloma
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('multiple myeloma', self.text, 'MM')
        
        # neoplasm
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('myelodysplastic / myeloproliferative (disease|neoplasm)', self.text, 'MDS/MPN')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('myeloproliferative / myelodysplastic (disease|neoplasm)', self.text, 'MDS/MPN')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('myeloproliferative neoplasm', self.text, 'MPN')
        
        # sarcoma
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('undifferentiated pleomorphic sarcoma', self.text, 'UPS')
        
        # tumor
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('isolated tumor cell' + s(), self.text, 'ITC')
        
    #
    def process_abbreviations(self):
        pass
        
    #
    def run_preprocessor(self):
        self._normalize_whitespace()
        self._process_irregular_initialisms()
        self._process_regular_initialisms()

#
class Posttokenizer(Preprocessor_base):
        
    #
    def process_general(self):
        self.text = \
            self.lambda_manager.lambda_conversion('MDS / MPN', self.text, 'MDS/MPN')
        
#
class Text_preparation(Preprocessor_base):
    
    #
    def cleanup_text(self):
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)Scarff ', self.text, 'Scarf ')
        
    #
    def normalize_text(self):
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)leukaemia', self.text, 'leukemia')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[Tt])umour', self.text, 'umor')
    
    #
    def setup_text(self):
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(?i)Scharff(-| )', '(?i)Scharff', self.text, 'Scarff')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(?i)Scharf(-| )', '(?i)Scharf', self.text, 'Scarff')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(?i)Scarf(-| )', '(?i)Scarf', self.text, 'Scarff')
            
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