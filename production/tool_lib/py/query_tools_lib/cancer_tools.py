# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 16:45:34 2020

@author: haglers
"""

#
from nlp_pipeline_lib.py.base_lib.preprocessor_base_class import Preprocessor_base
from tool_lib.py.processing_tools_lib.text_processing_tools import s

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
            self._normalize_regular_initialism('invasive ' + carcinoma[0], 'I' + carcinoma[1])
            self._normalize_regular_initialism(carcinoma[0] + ' in situ', carcinoma[1] + 'IS')
            self._normalize_regular_initialism(carcinoma[0], carcinoma[1])
            self._normalize_regular_initialism('invasive ' + carcinoma[1], 'I' + carcinoma[1])
            self._normalize_regular_initialism(carcinoma[1] + ' in situ', carcinoma[1] + 'IS')
        
        # hyperplasia
        hyperplasia_list = [ [ 'duct(al)? hyperplasia', 'DH' ],
                             [ 'lobular hyperplasia', 'LH' ],
                             [ 'columnar cell hyperplasia', 'CCH' ] ]
        for hyperplasia in hyperplasia_list:
            self._normalize_regular_initialism('atypical ' + hyperplasia[0], 'A' + hyperplasia[1])
            self._normalize_regular_initialism('usual ' + hyperplasia[0], 'U' + hyperplasia[1])
            self._normalize_regular_initialism(hyperplasia[0], hyperplasia[1])
        
        # leukemia
        self._normalize_regular_initialism('acute myeloid leukemia', 'AML')
        self._normalize_regular_initialism('acute myelomonocytic leukemia', 'AMML')
        
        # myeloma
        self._normalize_regular_initialism('multiple myeloma', 'MM')
        
        # neoplasm
        self._normalize_regular_initialism('myelodysplastic / myeloproliferative (disease|neoplasm)', 'MDS/MPN')
        self._normalize_regular_initialism('myeloproliferative / myelodysplastic (disease|neoplasm)', 'MDS/MPN')
        self._normalize_regular_initialism('myeloproliferative neoplasm', 'MPN')
        
        # sarcoma
        self._normalize_regular_initialism('undifferentiated pleomorphic sarcoma', 'UPS')
        
        # tumor
        self._normalize_regular_initialism('isolated tumor cell' + s(), 'ITC')
        
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