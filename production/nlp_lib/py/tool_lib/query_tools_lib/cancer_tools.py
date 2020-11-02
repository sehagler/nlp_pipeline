# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 16:45:34 2020

@author: haglers
"""

#
from nlp_lib.py.base_class_lib.preprocessor_base_class import Preprocessor_base
from nlp_lib.py.tool_lib.processing_tools_lib.text_processing_tools import s

#
class Named_entity_recognition(Preprocessor_base):
    
    #
    def _process_irregular_initialisms(self):
        
        self._clear_command_list()
        
        # breast cancer
        self._general_command('(?i)in situ and invasive duct(al)? (cancer|carcinoma)',
                              {None : 'DCIS and IDC'})
        self._general_command('(?i)usual and atypical duct(al)? hyperplasia( \( UDH, ADH \))?', 
                              {None : 'UDH and ADH'})
        
        self._process_command_list()
        
    #
    def _process_regular_initialisms(self):
        
        self._clear_command_list()
        
        # carcinoma
        self._general_command('(?i)sqcc', {None : 'SCC'})
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
        
        # miscellaneous
        self._normalize_regular_initialism('columnar cell change', 'CCC')
        self._normalize_regular_initialism('eastern cooperative oncology group', 'ECOG')
        self._normalize_regular_initialism('flat epithelial atypia', 'FEA')
        self._normalize_regular_initialism('pathologic complete response', 'pCR')
        self._normalize_regular_initialism('residual ca(ncer)? burden', 'RCB')
        self._general_command('(?i)FAB (?=[0-9])', {None : 'FAB M'})
        self._general_command('(?i)HLA-Dr', {None : 'HLA-DR'})
        self._general_command('(?i)blasts ?(\+|and|plus) ?promonocytes', {None : 'blasts/promonocytes'})
        self._normalize_regular_initialism('(?i)butyrate esterase', 'BE')
        self._normalize_regular_initialism('(?i)minimal residual disease', 'MRD')
        self._normalize_regular_initialism('(?i)myelodysplastic syndrome', 'MDS')
        self._normalize_regular_initialism('(?i)myeloperoxidase', 'MPO')
        
        self._process_command_list()
        
    #
    def process_abbreviations(self):
        pass
        
    #
    def process_initialisms(self):
        self._process_irregular_initialisms()
        self._process_regular_initialisms()

#
class Posttokenizer(Preprocessor_base):
        
    #
    def process_general(self):
        self._clear_command_list()
        self._general_command('MDS / MPN', {None : 'MDS/MPN'})
        self._process_command_list()
        
#
class Text_preparation(Preprocessor_base):
    
    #
    def cleanup_text(self):
        self._clear_command_list()
        self._general_command('(?i)Scarff ', {None : 'Scarf '})
        self._process_command_list()
        
    #
    def normalize_text(self):
        self._clear_command_list()
        self._general_command('(?i)leukaemia', {None : 'leukemia'})
        self._general_command('(?<=[Tt])umour', {None : 'umor'})
        self._process_command_list()
    
    #
    def setup_text(self):
        self._clear_command_list()
        self._general_command('(?i)Scharff(-| )', {'(?i)Scharff': 'Scarff'})
        self._general_command('(?i)Scharf(-| )', {'(?i)Scharf': 'Scarff'})
        self._general_command('(?i)Scarf(-| )', {'(?i)Scarf': 'Scarff'})
        self._process_command_list()