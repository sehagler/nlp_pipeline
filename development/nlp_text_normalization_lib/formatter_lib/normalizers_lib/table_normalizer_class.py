# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 11:19:40 2020

@author: haglers
"""

#
import re

#
from lambda_lib.lambda_manager_class import Lambda_manager
from regex_lib.regex_tools import s

#
class Table_normalizer(object):
    
    #
    def __init__(self, static_data):
        self.static_data = static_data
        self.lambda_manager = Lambda_manager()
        
    #
    def _insert_whitespace(self, match_str, whitespace):
        match = 0
        m_str = re.compile(match_str)
        while match is not None:
            match = m_str.search(self.text, re.IGNORECASE)
            if match is not None:
                self.text = self.text[:match.start()] + whitespace + \
                            self.text[match.start()+1:]
    
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
    def _pull_out_table_entry(self, command):
        self._insert_whitespace(command, '\n')
        
    #
    def normalize_hematopathology_table(self, text):
        self.text = text
        self._pull_out_table_entry('[ \t]Bands[ \t]+[0-9]')
        self._pull_out_table_entry('[ \t](?<!% )Baso(phil)?s[ \t]+(x )?[0-9]')
        self._pull_out_table_entry('[ \t](?<!% )Eos(inophils)?[ \t]+(x )?[0-9]')
        self._pull_out_table_entry('[ \t](?<!% )Lymph(ocyte)?s[ \t]+(x )?[0-9]')
        self._pull_out_table_entry('[ \t](?<!% )Mono(cyte)?s[ \t]+(x )?[0-9]')
        self._pull_out_table_entry('[ \t](?<!% )Neutrophils[ \t]+[0-9]')
        self._pull_out_table_entry('[ \t]PMNs[ \t]+(x )?[0-9]')
        self._pull_out_table_entry('[ \t]ANISOCYTOSIS')
        self._pull_out_table_entry('[ \t]ATYPICAL CELLS? [#%]')
        self._pull_out_table_entry('[ \t]BASO(PHIL)? [#%]')
        self._pull_out_table_entry('[ \t]EOS(INOPHIL)? [#%]')
        self._pull_out_table_entry('[ \t]HCT(?= [0-9])')
        self._pull_out_table_entry('[ \t]HEMATOCRIT')
        self._pull_out_table_entry('[ \t]HEMOGLOBIN')
        self._pull_out_table_entry('[ \t]HGB(?= [0-9])')
        self._pull_out_table_entry('[ \t]IG[#%]')
        self._pull_out_table_entry('[ \t]LY#(?= [0-9])')
        self._pull_out_table_entry('[ \t]LYMPHOCYTE [#%]')
        self._pull_out_table_entry('[ \t]MANUAL DIFFERENTIAL')
        self._pull_out_table_entry('[ \t]MCHC')
        self._pull_out_table_entry('[ \t]MCV')
        self._pull_out_table_entry('[ \t]METAMYELOCYTES [#%]')
        self._pull_out_table_entry('[ \t]MONOCYTE [#%]')
        self._pull_out_table_entry('[ \t]MYELOCYTES [#%]')
        self._pull_out_table_entry('[ \t]MPV')
        self._pull_out_table_entry('[ \t]NE#(?= [0-9])')
        self._pull_out_table_entry('[ \t]NEUTROPHIL [#%]')
        self._pull_out_table_entry('[ \t]NRBC[#%]')
        self._pull_out_table_entry('[ \t]PLT(?= [0-9])')
        self._pull_out_table_entry('[ \t]PLASMA CELLS? [#%]')
        self._pull_out_table_entry('[ \t]PLATELET COUNT')
        self._pull_out_table_entry('[ \t]POLYCHROMASIA')
        self._pull_out_table_entry('[ \t]PROMYELOCYTES [#%]')
        self._pull_out_table_entry('[ \t]RBC [0-9]')
        self._pull_out_table_entry('[ \t]RDW SD')
        self._pull_out_table_entry('[ \t]REACTIVE LYMPHS? [#%]')
        self._pull_out_table_entry('[ \t]RED CELL COUNT')
        self._pull_out_table_entry('[ \t]ROW(?= [0-9])')
        self._pull_out_table_entry('[ \t]WHITE CELL COUNT')
        self._pull_out_table_entry('[ \t]WBC(?= [0-9])')
        return self.text
    
    #
    def process_text(self, text):
        self.text = text
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
        return self.text