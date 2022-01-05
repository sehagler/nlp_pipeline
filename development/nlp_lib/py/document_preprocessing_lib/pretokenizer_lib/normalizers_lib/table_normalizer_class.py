# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 11:19:40 2020

@author: haglers
"""

#
from nlp_lib.py.base_lib.preprocessor_base_class \
    import Preprocessor_base
from tool_lib.py.processing_tools_lib.text_processing_tools import s

#
class Table_normalizer(Preprocessor_base):
    
    #
    def _normalize_atypical_cell(self):
        self._general_command(self._pre_punct() + 'atyp cell' + s(), {None : '\nATYPICAL CELL'})
        self._general_command(self._pre_punct() + 'atypical cell' + s() + ' %', {None : '\nATYPICAL CELL%'})
    
    #
    def _normalize_basophil(self):
        self._general_command(self._pre_punct() + 'baso' + s() + '[ \t]', {None : '\nBASOPHIL'})
        self._general_command(self._pre_punct() + '(% )?basophil' + s(), {None : '\nBASOPHIL%'})
        self._general_command(self._pre_punct() + 'basophil (#|% abs)', {None : '\nBASOPHIL#'})
    
    #
    def _normalize_eosinophil(self):
        self._general_command(self._pre_punct() + 'eos[ \t]', {None : '\nEOSINOPHIL '})
        self._general_command(self._pre_punct() + '(% )?eosinophil' + s(), {None : '\nEOSINOPHIL%'})
        self._general_command(self._pre_punct() + 'eosinphil (#|% abs)', {None : '\nEOSINOPHIL#'})
        self._general_command(self._pre_punct() + 'eos abs', {None : '\nEOSINOPHIL#'})
                              
    #
    def _normalize_ig(self):
        self._general_command(self._pre_punct() + 'ig #', {None : 'IG#'})
        self._general_command(self._pre_punct() + 'ig %', {None : 'IG%'})
    
    #
    def _normalize_lymphocyte(self):
        self._general_command(self._pre_punct() + 'lymphs', {None : '\nLYMPHOCYTE'})
        self._general_command(self._pre_punct() + '(% )?lymphocyte' + s(), {None : '\nLYMPHOCYTE%'})
        self._general_command(self._pre_punct() + '(ly#|lymph abs)', {None : '\nLYMPHOCYTE#'})
    
    #
    def _normalize_monocyte(self):
        self._general_command(self._pre_punct() + 'mono #', {None : '\nMONOCYTE#'})
        self._general_command(self._pre_punct() + 'mono %', {None : '\nMONOCYTE%'})
        self._general_command(self._pre_punct() + 'monos', {None : '\nMONOCYTE'})
        self._general_command(self._pre_punct() + '(% )?monocyte' + s(), {None : '\nMONOCYTE%'})
        self._general_command(self._pre_punct() + '(% )?monocyte %', {None : '\nMONOCYTE%'})
        self._general_command(self._pre_punct() + 'monocyte% abs', {None : '\nMONOCYTE#'})
                              
    #
    def _normalize_myelocyte(self):
        self._general_command(self._pre_punct() + '(% )?myelocyte' + s(), {None : '\nMYELOCYTE'})
        self._general_command(self._pre_punct() + '(% )?myelocyte %', {None : '\nMYELOCYTE%'})
        
    #
    def _normalize_neutrophil(self):
        self._general_command(self._pre_punct() + '(% )?neutrophils', {None : '\nNEUTROPHIL%'})
        self._general_command(self._pre_punct() + '(ne#|neut abs)', {None : '\nNEUTROPHIL#'})
                              
    #
    def _normalize_nrbc(self):
        self._general_command(self._pre_punct() + 'nrbc #', {None : 'NRBC#'})
        self._general_command(self._pre_punct() + 'nrbc %', {None : 'NRBC%'})
    
    #
    def _pre_punct(self):
        return('(?i)\n')
    
    #
    def process_text(self, text):
        self.push_text(text)
        self._general_command('(?i),? POC', {None : ''})
        self._normalize_atypical_cell()
        self._normalize_basophil()
        self._normalize_eosinophil()
        self._general_command(self._pre_punct() + 'hematocrit', {None : '\nHCT'})
        self._general_command(self._pre_punct() + 'hemoglobin', {None : '\nHGB'})
        self._normalize_ig()
        self._normalize_lymphocyte()
        self._normalize_monocyte()
        self._normalize_myelocyte()
        self._normalize_neutrophil()
        self._normalize_nrbc()
        self._general_command(self._pre_punct() + 'plt', {None : '\nPLT'})
        self._general_command(self._pre_punct() + 'PLATELET COUNT', {None : '\nPLT'})
        self._general_command(self._pre_punct() + 'RED CELL COUNT', {None : '\nRBC'})
        self._general_command(self._pre_punct() + 'WHITE CELL COUNT', {None : '\nWBC'})
        text = self.pull_text()
        return text