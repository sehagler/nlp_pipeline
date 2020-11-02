# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 10:17:40 2020

@author: haglers
"""

#
from nlp_lib.py.base_class_lib.preprocessor_base_class import Preprocessor_base
from nlp_lib.py.tool_lib.processing_tools_lib.text_processing_tools import s

#
class Named_entity_recognition(Preprocessor_base):
        
    #
    def _process_regular_initialisms(self):
        self._clear_command_list()
        self._normalize_regular_initialism('cerebrospinal fluid', 'CSF')
        self._normalize_regular_initialism('chronic kidney disease', 'CKD')
        self._normalize_regular_initialism('chronic renal disease( \( CRD \))?', 'CKD')
        self._normalize_regular_initialism('chronic renal failure( \( CRF \))?', 'CKD')
        self._normalize_regular_initialism('chronic renal (impairment|insufficiency)', 'CKD')
        self._normalize_regular_initialism('food and drug administration', 'FDA')
        self._normalize_regular_initialism('fluorescen(ce|t) in situ hybridization', 'FISH')
        self._normalize_regular_initialism('in situ hybridization', 'ISH')
        self._normalize_regular_initialism('high(-| )?power(ed)? field' + s(), 'HPF')
        self._normalize_regular_initialism('packs?( (/|per))? days?', 'PPD')
        self._normalize_regular_initialism(' ppd', ' PPD')
        self._normalize_regular_initialism('packs?( (/|per))? wks?', 'PPW')
        self._normalize_regular_initialism(' ppw', ' PPW')
        self._normalize_regular_initialism('packs?( (/|per))? yrs?', 'PPY')
        self._normalize_regular_initialism(' ppy', ' PPY')
        self._normalize_regular_initialism('past medical (history|hx)', 'PMH')
        self._normalize_regular_initialism('PMHx', 'PMH')
        self._normalize_regular_initialism('PMH / o', 'PMH')
        self._normalize_regular_initialism('world health organization', 'WHO')
        self._general_command('(?i)red blood cell', {None : 'RBC'})
        self._normalize_regular_initialism('(?i)sudan black B', 'SBB')
        self._general_command('(?i)white blood cell', {None : 'WBC'})
        self._process_command_list()
        
    #
    def process_initialisms(self):
        self._process_regular_initialisms()