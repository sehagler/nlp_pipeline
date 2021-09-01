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
from tool_lib.py.query_tools_lib.blasts_tools \
    import Summarization as Summarization_blasts
from tool_lib.py.query_tools_lib.breast_cancer_biomarkers_tools \
    import Summarization as Summarization_breast_cancer_biomarkers
from tool_lib.py.query_tools_lib.ecog_tools \
    import Summarization as Summarization_ecog
from tool_lib.py.query_tools_lib.fish_analysis_summary_tools \
    import Summarization as Summarization_fish_analysis_summary
from tool_lib.py.query_tools_lib.histological_grade_tools \
    import Summarization as Summarization_histological_grade
from tool_lib.py.query_tools_lib.immunophenotype_tools \
    import Summarization as Summarization_immunophenotype
from tool_lib.py.query_tools_lib.serial_number_tools \
    import Summarization as Summarization_serial_number
from tool_lib.py.query_tools_lib.smoking_tools \
    import Summarization as Summarization_smoking
from tool_lib.py.query_tools_lib.tnm_stage_tools \
    import Summarization as Summarization_tnm_stage

#
class Summarization(Preprocessor_base):
    
    #
    def __init__(self, static_data):
        Preprocessor_base.__init__(self, static_data)
        self.summarization_blasts = \
            Summarization_blasts(self.static_data)
        self.summarization_breast_cancer_biomarkers = \
            Summarization_breast_cancer_biomarkers(self.static_data)
        self.summarization_ecog = Summarization_ecog(self.static_data)
        self.summarization_fish_analysis_summary = \
            Summarization_fish_analysis_summary(self.static_data)
        self.summarization_histological_grade = \
            Summarization_histological_grade(self.static_data)
        self.summarization_immunophenotype = \
            Summarization_immunophenotype(self.static_data)
        self.summarization_serial_number = \
            Summarization_serial_number(self.static_data)
        self.summarization_smoking = \
            Summarization_smoking(self.static_data)
        self.summarization_tnm_stage = \
            Summarization_tnm_stage(self.static_data)
   
    #
    def _remove_extraneous_text(self):
        self._remove_mychart()
        self._remove_see()
        self._clear_command_list()
        self._general_command('(?i)[\n\s]+based on pathologic finding' + s(), {None : ''})
        self._general_command('(?i)(?<=Dr [A-Z])\.', {None : ''})
        self._general_command('(?i)my electronic signature.*' + article() + ' final diagnosis( \.)?', {None : ''})
        self._general_command('(?i)i have reviewed.*and final diagnosis( \.)?', {None : ''})
        self._general_command('(?i)inclu(des|sive of) all specimens', {None : ''})
        self._general_command('(?i)pathologist interpretation ' + be() + ' based on ' + article() + ' review.*representative hematoxylin and eosin stains( \.)?', {None : ''})
        self._general_command('(?i)' + article() + ' test ' + be() + ' developed.*FDA( \.)?', {None : ''})
        self._general_command('(?i)' + article() + ' clinical interpretation ' + be() + ' made by ' + article() + ' clinical geneticist( \.)?', {None : ''})
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
    def _substitution_endings_list(self, search_str):
        self._general_command(search_str + '\n', {None : '\n'})
        self._general_command(search_str + '\t', {None : '\t'})
        self._general_command(search_str + ' ', {None : ' '})
        self._general_command(search_str + ',', {None : ','})
        self._general_command(search_str + '\.', {None : '.'})
        self._general_command(search_str + ';', {None : ';'})
        self._general_command(search_str + '( )?-', {None : '-'})
    
    #
    def process_document(self, text):
        self.text = text
        self._normalize_whitespace()
        self.summarization_blasts.push_text(self.text)
        self.summarization_blasts.remove_extraneous_text()
        self.text = self.summarization_blasts.pull_text()
        self.text = \
            self.summarization_breast_cancer_biomarkers.process_text(self.text)
        self.summarization_ecog.push_text(self.text)
        self.summarization_ecog.process_ecog()
        self.text = self.summarization_ecog.pull_text()
        self.summarization_fish_analysis_summary.push_text(self.text)
        self.summarization_fish_analysis_summary.remove_extraneous_text()
        self.text = self.summarization_fish_analysis_summary.pull_text()
        self.summarization_histological_grade.push_text(self.text)
        self.summarization_histological_grade.process_mitotic_rate()
        self.summarization_histological_grade.process_nuclear_pleomorphism()
        self.summarization_histological_grade.process_tubule_formation()
        self.text = self.summarization_histological_grade.pull_text()
        self.summarization_immunophenotype.push_text(self.text)
        self.summarization_immunophenotype.remove_extraneous_text()
        self.text = self.summarization_immunophenotype.pull_text()
        self.summarization_serial_number.push_text(self.text)
        self.summarization_serial_number.remove_extraneous_text()
        self.text = self.summarization_serial_number.pull_text()
        self.summarization_smoking.push_text(self.text)
        self.summarization_smoking.remove_extraneous_text()
        self.text = self.summarization_smoking.pull_text()
        self.summarization_tnm_stage.push_text(self.text)
        self.summarization_tnm_stage.process_tnm_staging()
        self.summarization_tnm_stage.remove_tnm_staging()
        self.summarization_tnm_stage.remove_extraneous_text()
        self.text = self.summarization_tnm_stage.pull_text()
        self._remove_extraneous_text()
        self._normalize_whitespace()
        return self.text