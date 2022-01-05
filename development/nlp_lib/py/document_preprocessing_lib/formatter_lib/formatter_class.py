# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 12:58:14 2021

@author: haglers
"""

#
import re

#
from nlp_lib.py.base_lib.preprocessor_base_class \
    import Preprocessor_base

#
class Formatter(Preprocessor_base):
    
    #
    def __init__(self, static_data):
        Preprocessor_base.__init__(self, static_data)
        self.body_header = 'SUMMARY'
    
    #
    def _add_body_header(self):
        self.text = self.body_header + '\n' + self.text
        self.text = re.sub('^' + self.body_header + '\n' + self.body_header,
                           self.body_header + '\n', self.text)
        self.text = re.sub('^' + self.body_header + '[\n\s]*',
                           self.body_header + '\n\n', self.text)
    
    #
    def _format_beakerap(self):
        self._clear_command_list()
        self._pull_out_section_header('(?i)[ \t]case (reviewed|seen) by:?')
        self._pull_out_section_header('(?i)[ \t]clinical history')
        self._pull_out_section_header('(?i)[ \t]comment(s)?( )?(\([a-z0-9 ]*\))?:')
        self._pull_out_section_header('(?i)[ \t]note( )?(\([a-z0-9 ]*\))?:')
        self._process_command_list()
        self._add_body_header()
        self._clear_command_list()
        self._general_command('(?<![0-9]) - (?![0-9])', {None : '\n- '})
        self._general_command('\n +', {None : '\n'})
        self._process_command_list()
        self._format_section_headers()
        self._format_hematopathology_table_beaker_ap()
        
    #
    def _format_hematopathology_table_beaker_ap(self):
        self._clear_command_list()
        self._pull_out_section_header('(?i)[ \t]antibodies tested')
        self._pull_out_section_header('(?i)[ \t]bone marrow aspirate smears')
        self._pull_out_section_header('(?i)[ \t]bone marrow (biopsy/)?clot section')
        self._pull_out_section_header('(?i)[ \t]bone marrow differential')
        self._pull_out_section_header('(?i)[ \t]cbc')
        self._pull_out_section_header('(?i)[ \t]component value')
        self._pull_out_section_header('(?i)[ \t]cytogenetic and fish studies')
        self._pull_out_section_header('(?i)[ \t]flow cytometric analysis')
        self._pull_out_section_header('(?i)[ \t]immunohistochemical stains:')
        self._pull_out_section_header('(?i)[ \t]immunologic analysis:')
        self._pull_out_section_header('(?i)[ \t]molecular studies:')
        self._pull_out_section_header('(?i)[ \t]peripheral blood differential')
        self._pull_out_section_header('(?i)[ \t]peripheral blood morphology')
        self._pull_out_section_header('(?i)[ \t]resulting agency')
        self._pull_out_section_header('(?i)[ \t]special stains')
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
        self._general_command('\nFinal Diagnosis\n', {None : '\nFINAL DIAGNOSIS\n'})
        self._general_command('\n(MANUAL|PERIPHERAL BLOOD) DIFFERENTIAL', {None : '\n\nMANUAL DIFFERENTIAL'})
        self._process_command_list()
        
    #
    def _format_hematopathology_table_powerpath(self):
        self._clear_command_list()
        self._pull_out_table_entry('[ \t]Bands[ \t]+[0-9]')
        self._pull_out_table_entry('[ \t](?<!% )Baso(phil)?s[ \t]+(x )?[0-9]')
        self._pull_out_table_entry('[ \t](?<!% )Eos(inophils)?[ \t]+(x )?[0-9]')
        self._pull_out_table_entry('[ \t](?<!% )Lymph(ocyte)?s[ \t]+(x )?[0-9]')
        self._pull_out_table_entry('[ \t](?<!% )Mono(cyte)?s[ \t]+(x )?[0-9]')
        self._pull_out_table_entry('[ \t](?<!% )Neutrophils[ \t]+[0-9]')
        self._pull_out_table_entry('[ \t]PMNs[ \t]+(x )?[0-9]')
        self._process_command_list()
        
    #
    def _format_powerpath(self):
        self._add_body_header()
        self._format_section_headers()
        self._format_hematopathology_table_powerpath()
        
    #
    def _format_section_headers(self):
        self._clear_command_list()
        self._general_command('(?i)\nFinal (Pathologic )?Diagnosis\n', {None : ''})
        self._general_command('\nDIFFERENTIAL', {None : '\nMANUAL DIFFERENTIAL'})
        self._general_command('\nImmunologic Analysis\n', {None : ''})
        self._general_command('\nMicroscopic Description\n', {None : ''})
        self._process_command_list()
        
    #
    def _pull_out_section_header(self, command):
        self._clear_command_list()
        self.command_list.append([ 1, command ])
        self._process_command_list()
        
    #
    def _pull_out_table_entry(self, command):
        self._clear_command_list()
        self.command_list.append([ 2, command ])
        self._process_command_list()
        
    #
    def process_document(self, text, source_system):
        self.text = text
        if source_system == 'BeakerAP':
            self._format_beakerap()
        else:
            self._format_powerpath()
        return self.text