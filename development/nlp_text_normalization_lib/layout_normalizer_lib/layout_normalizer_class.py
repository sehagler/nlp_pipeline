# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 12:58:14 2021

@author: haglers
"""

#
import re

#
from lambda_lib.object_lib.lambda_object_class import Lambda_object
from nlp_text_normalization_lib.layout_normalizer_lib.normalizers_lib.section_header_normalizer_class \
    import Section_header_normalizer

#
class Layout_normalizer(object):
    
    #
    def __init__(self, section_header_structure):
        self.lambda_object = Lambda_object()
        self.section_header_normalizer = \
            Section_header_normalizer(section_header_structure)
        self.report_text_header = 'REPORT TEXT'
        
    #
    def _add_report_text_header(self):
        self.text = self.report_text_header + '\n' + self.text
        self.text = \
            self.lambda_object.lambda_conversion('^' + self.report_text_header + '\n' + self.report_text_header,
                                                  self.text, self.report_text_header + '\n')
        self.text = \
            self.lambda_object.lambda_conversion('^' + self.report_text_header + '[\n\s]*',
                                                  self.text, self.report_text_header + '\n\n')
            
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
    def _normalize_hematopathology_table(self, text):
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
    def _pull_out_table_entry(self, command):
        self._insert_whitespace(command, '\n')
        
    #
    def format_text(self, dynamic_data_manager, text, source_system):
        self.dynamic_data_manager = dynamic_data_manager
        self.text = text
        self._add_report_text_header()
        
        self.dynamic_data_manager.append_keywords_text(self.report_text_header, 0)
        self.text = self.section_header_normalizer.pull_out_section_headers(self.text)
        self.section_header_normalizer.push_dynamic_data_manager(self.dynamic_data_manager)
        self.text = \
            self.section_header_normalizer.normalize_section_header(self.text)
        self.text = \
            self.section_header_normalizer.clear_section_header_tags(self.text)
        self.dynamic_memory_manager = \
            self.section_header_normalizer.pull_dynamic_data_manager()
        
        self.text = self._normalize_hematopathology_table(self.text)
        return self.dynamic_data_manager, self.text