# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 11:19:40 2020

@author: haglers
"""

#
from nlp_text_normalization_lib.base_lib.preprocessor_base_class \
    import Preprocessor_base
from tool_lib.py.processing_tools_lib.text_processing_tools import s

#
class Table_normalizer(Preprocessor_base):
    
    #
    def _normalize_atypical_cell(self):
        self.text = \
            self.lambda_manager.lambda_conversion(self._pre_punct() + 'atyp cell' + s(), self.text, '\nATYPICAL CELL')
        self.text = \
            self.lambda_manager.lambda_conversion(self._pre_punct() + 'atypical cell' + s() + ' %', self.text, '\nATYPICAL CELL%')
    
    #
    def _normalize_basophil(self):
        self.text = \
            self.lambda_manager.lambda_conversion(self._pre_punct() + 'baso' + s() + '[ \t]', self.text, '\nBASOPHIL')
        self.text = \
            self.lambda_manager.lambda_conversion(self._pre_punct() + '(% )?basophil' + s(), self.text, '\nBASOPHIL%')
        self.text = \
            self.lambda_manager.lambda_conversion(self._pre_punct() + 'basophil (#|% abs)', self.text, '\nBASOPHIL#')
    
    #
    def _normalize_eosinophil(self):
        self.text = \
            self.lambda_manager.lambda_conversion(self._pre_punct() + 'eos[ \t]', self.text, '\nEOSINOPHIL ')
        self.text = \
            self.lambda_manager.lambda_conversion(self._pre_punct() + '(% )?eosinophil' + s(), self.text, '\nEOSINOPHIL%')
        self.text = \
            self.lambda_manager.lambda_conversion(self._pre_punct() + 'eosinphil (#|% abs)', self.text, '\nEOSINOPHIL#')
        self.text = \
            self.lambda_manager.lambda_conversion(self._pre_punct() + 'eos abs', self.text, '\nEOSINOPHIL#')
                              
    #
    def _normalize_ig(self):
        self.text = \
            self.lambda_manager.lambda_conversion(self._pre_punct() + 'ig #', self.text, 'IG#')
        self.text = \
            self.lambda_manager.lambda_conversion(self._pre_punct() + 'ig %', self.text, 'IG%')
    
    #
    def _normalize_lymphocyte(self):
        self.text = \
            self.lambda_manager.lambda_conversion(self._pre_punct() + 'lymphs', self.text, '\nLYMPHOCYTE')
        self.text = \
            self.lambda_manager.lambda_conversion(self._pre_punct() + '(% )?lymphocyte' + s(), self.text, '\nLYMPHOCYTE%')
        self.text = \
            self.lambda_manager.lambda_conversion(self._pre_punct() + '(ly#|lymph abs)', self.text, '\nLYMPHOCYTE#')
    
    #
    def _normalize_monocyte(self):
        self.text = \
            self.lambda_manager.lambda_conversion(self._pre_punct() + 'mono #', self.text, '\nMONOCYTE#')
        self.text = \
            self.lambda_manager.lambda_conversion(self._pre_punct() + 'mono %', self.text, '\nMONOCYTE%')
        self.text = \
            self.lambda_manager.lambda_conversion(self._pre_punct() + 'monos', self.text, '\nMONOCYTE')
        self.text = \
            self.lambda_manager.lambda_conversion(self._pre_punct() + '(% )?monocyte' + s(), self.text, '\nMONOCYTE%')
        self.text = \
            self.lambda_manager.lambda_conversion(self._pre_punct() + '(% )?monocyte %', self.text, '\nMONOCYTE%')
        self.text = \
            self.lambda_manager.lambda_conversion(self._pre_punct() + 'monocyte% abs', self.text, '\nMONOCYTE#')
                              
    #
    def _normalize_myelocyte(self):
        self.text = \
            self.lambda_manager.lambda_conversion(self._pre_punct() + '(% )?myelocyte' + s(), self.text, '\nMYELOCYTE')
        self.text = \
            self.lambda_manager.lambda_conversion(self._pre_punct() + '(% )?myelocyte %', self.text, '\nMYELOCYTE%')
        
    #
    def _normalize_neutrophil(self):
        self.text = \
            self.lambda_manager.lambda_conversion(self._pre_punct() + '(% )?neutrophils', self.text, '\nNEUTROPHIL%')
        self.text = \
            self.lambda_manager.lambda_conversion(self._pre_punct() + '(ne#|neut abs)', self.text, '\nNEUTROPHIL#')
                              
    #
    def _normalize_nrbc(self):
        self.text = \
            self.lambda_manager.lambda_conversion(self._pre_punct() + 'nrbc #', self.text, 'NRBC#')
        self.text = \
            self.lambda_manager.lambda_conversion(self._pre_punct() + 'nrbc %', self.text, 'NRBC%')
    
    #
    def _pre_punct(self):
        return('\n')
    
    #
    def process_text(self, text):
        self.push_text(text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i),? POC', self.text)
        self._normalize_atypical_cell()
        self._normalize_basophil()
        self._normalize_eosinophil()
        self.text = \
            self.lambda_manager.lambda_conversion(self._pre_punct() + 'hematocrit', self.text, '\nHCT')
        self.text = \
            self.lambda_manager.lambda_conversion(self._pre_punct() + 'hemoglobin', self.text, '\nHGB')
        self._normalize_ig()
        self._normalize_lymphocyte()
        self._normalize_monocyte()
        self._normalize_myelocyte()
        self._normalize_neutrophil()
        self._normalize_nrbc()
        self.text = \
            self.lambda_manager.lambda_conversion(self._pre_punct() + 'plt', self.text, '\nPLT')
        self.text = \
            self.lambda_manager.lambda_conversion(self._pre_punct() + 'PLATELET COUNT', self.text, '\nPLT')
        self.text = \
            self.lambda_manager.lambda_conversion(self._pre_punct() + 'RED CELL COUNT', self.text, '\nRBC')
        self.text = \
            self.lambda_manager.lambda_conversion(self._pre_punct() + 'WHITE CELL COUNT', self.text, '\nWBC')
        text = self.pull_text()
        return text