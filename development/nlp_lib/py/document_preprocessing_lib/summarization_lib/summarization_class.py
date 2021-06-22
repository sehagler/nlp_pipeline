# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 12:29:58 2021

@author: haglers
"""

#
from nlp_lib.py.document_preprocessing_lib.base_class_lib.preprocessor_base_class \
    import Preprocessor_base
from tool_lib.py.processing_tools_lib.text_processing_tools \
    import article, be, note_label, s, specimen_label
from tool_lib.py.query_tools_lib.biomarker_tools \
    import Summarization as Summarization_biomarkers
from tool_lib.py.query_tools_lib.ecog_tools \
    import Summarization as Summarization_ecog
from tool_lib.py.query_tools_lib.histological_grade_tools \
    import Summarization as Summarization_histological_grade
from tool_lib.py.query_tools_lib.serial_number_tools \
    import Summarization as Summarization_serial_number
from tool_lib.py.query_tools_lib.tnm_stage_tools \
    import Summarization as Summarization_tnm_stage

#
class Summarization(Preprocessor_base):
    
    #
    def __init__(self, static_data):
        Preprocessor_base.__init__(self, static_data)
        self.summarization_biomarkers = \
            Summarization_biomarkers(self.static_data)
        self.summarization_ecog = Summarization_ecog(self.static_data)
        self.summarization_histological_grade = \
            Summarization_histological_grade(self.static_data)
        self.summarization_serial_number = \
            Summarization_serial_number(self.static_data)
        self.summarization_tnm_stage = \
            Summarization_tnm_stage(self.static_data)
    
    #
    def _process_names(self):
        self._clear_command_list()
        self._general_command('(?i)ki-67 \(mm-1\)', {None : 'Ki-67'})
        text_list = []
        text_list.append('(?i)(pathologic( tumor)?|TNM) stag(e|ing)')
        text_list.append('(?i)stage summary')
        for text_str in text_list:
            self._general_command(text_str, {None : 'Stage'})
        self._process_command_list()
    
    #
    def _remove_extraneous_text(self):
        self._remove_mychart()
        self._remove_see()
        self._clear_command_list()
        self._general_command('(?i)(\( )?(AJCC )?\d(\d)?th Ed(ition|.)( \))?', {None : ''})
        self._general_command('(?i)(\( )?AJCC( \))?', {None : ''})
        self._general_command('(?i)[\n\s]+by FISH', {None : ''})
        self._general_command('(?i)[\n\s]+by immunohistochemistry', {None : ''})
        self._general_command('(?i)[\n\s]+by immunostain', {None : ''})
        self._general_command('(?i)[\n\s]+(by)?(\( )?ARUP lab(s)?( \))?', {None : ''})
        self._general_command('(?i)\* ' + article() + ' asterisk indicates that ' + article() + ' immunohistochemical.*computer assisted quantitative image analysis( \.)?', {None : ''})
        self._general_command('(?i)\( analyte specific reagents.*clinical lab testing( \.)? \)( \.)?', {None : ''})
        self._general_command('(?i)\( analyte specific reagents.*FDA( \.)? \)( \.)?', {None : ''})
        self._general_command('(?i)' + article() + ' positive ER or PR result requires.*moderate to strong nuclear staining( \.)?', {None : ''})
        self._general_command('(?i)' + article() + ' ER and PR immunohistochemical stains are performed.*10% of the tumor cells( \.)?', {None : ''})
        self._general_command('(?i)[\n\s]+based on pathologic finding' + s(), {None : ''})
        self._general_command('(?i)(?<=Dr [A-Z])\.', {None : ''})
        self._general_command('(?i)my electronic signature.*' + article() + ' final diagnosis( \.)?', {None : ''})
        self._general_command('(?i)HER2 (expression )?' + be() + ' expressed by ' + article() + ' ACIS score(.*\n)*.*confirm HER2 DNA amplification( \.)?', {None : ''})
        self._general_command('(?i)i have reviewed.*and final diagnosis( \.)?', {None : ''})
        self._general_command('(?i)inclu(des|sive of) all specimens', {None : ''})
        self._general_command('(?i)pathologist interpretation ' + be() + ' based on ' + article() + ' review.*representative hematoxylin and eosin stains( \.)?', {None : ''})
        self._general_command('(?i)' + article() + ' test ' + be() + ' developed.*FDA( \.)?', {None : ''})
        self._general_command('(?i)' + article() + ' clinical interpretation ' + be() + ' made by ' + article() + ' clinical geneticist( \.)?', {None : ''})
        self._general_command('(?i)[\n\s]+\( PATHWAY(TM)?( )?HER2 kit(, 4B5)? \)', {None : ''})
        self._general_command('(?i)check out the free oregon quit line(.*\n)*.*www . quitnow . net / oregon', {None : ''})
        self._process_command_list()
    
    #
    def _remove_mychart(self):
        self._clear_command_list()
        self._general_command('(?i)display progress note in mychart : (no|yes)', {None : ''})
        self._process_command_list()
        
    #
    def _remove_see(self):
        self._clear_command_list()
        self._general_command('(?i)(\n\s*)?\( (please )?see [^\n\)\]]* \)', {None : ''})
        self._general_command('(?i)\s*see\n', {None : '\n'})
        self._process_command_list()
        match_str = '(?i)((\n\s*)?-( )?)?(please[\n\s]+)?see[\n\s]+' + \
                    '(the )?(second )?(amendment|cancer|note|synoptic)?( )?' + \
                    '(below|comment|report|synops(e|i))' + s() + \
                    '( and synoptic summary)?( and tumor protocol)?' + \
                    '( below)?( for (additional|technical) (details|information))?( \.)?'
        self._substitution_endings_list(match_str)
        match_str = '(?i)((\n\s*)?-( )?)?(please[\n\s]+)?see ' + \
                    '(note|(staging )?summary|(cancer )?synopsis|synoptic report)' + \
                    '( below)?( for (additional|technical) details)?'
        self._substitution_endings_list(match_str)
        match_str = '(?i)((\n\s*)?-( )?)?(please[\n\s]+)?see (also )?' + \
                    'note' + s() + '( )?' + note_label() + '( to ' + note_label() + ')?'
        self._substitution_endings_list(match_str)
        match_str = '(?i)((\n\s*)?-( )?)?(please[\n\s]+)?see (also )?' + \
                    'specimen' + s() + '( )?' + specimen_label() + '( to ' + specimen_label() + ')?'
        self._substitution_endings_list(match_str)
    
    #
    def process_document(self, text):
        self.text = text
        self._normalize_whitespace()
        self.summarization_biomarkers.push_text(self.text)
        self.summarization_biomarkers.process_estrogen_receptor()
        self.summarization_biomarkers.process_her2()
        self.summarization_biomarkers.process_progesterone_receptor()
        self.text = self.summarization_biomarkers.pull_text()
        self.summarization_ecog.push_text(self.text)
        self.summarization_ecog.process_ecog()
        self.text = self.summarization_ecog.pull_text()
        self.summarization_histological_grade.push_text(self.text)
        self.summarization_histological_grade.process_mitotic_rate()
        self.summarization_histological_grade.process_nuclear_pleomorphism()
        self.summarization_histological_grade.process_tubule_formation()
        self.text = self.summarization_histological_grade.pull_text()
        self.summarization_serial_number.push_text(self.text)
        self.summarization_serial_number.remove_extraneous_text()
        self.text = self.summarization_serial_number.pull_text()
        self.summarization_tnm_stage.push_text(self.text)
        self.summarization_tnm_stage.remove_tnm_staging()
        self.text = self.summarization_tnm_stage.pull_text()
        self._process_names()
        self._remove_extraneous_text()
        self._normalize_whitespace()
        return self.text