# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 10:38:15 2020

@author: haglers
"""

#
from nlp_lib.py.base_class_lib.preprocessor_base_class import Preprocessor_base
from nlp_lib.py.tool_lib.processing_tools_lib.text_processing_tools import article, be, note_label, part_label, specimen_label, s

#
class Summarization(Preprocessor_base):
    
    #
    def _block_label(self):
        return('([A-Z]*[0-9]*|[0-9]*[A-Z]*)')
    
    #
    def _case_number(self):
        return('[A-Z0-9-]*')
    
    #
    def process_ecog(self):
        self._clear_command_list()
        self._general_command('(?i)(?<!{ )ecog( :)? (performance )?(status|score|ps)', {None : 'ECOG ( ZUBROD ) '})
        self._general_command('(?i)karnofsky (performance )?(status|score|ps)', {None : 'ECOG ( KARNOFSKY ) '})
        self._general_command('(?i)lansky (play performance )?(status|score|ps)', {None : 'ECOG ( LANSKY ) '})
        self._general_command('(?i)(?<!{ )ecog (?!\()', {None : 'ECOG ( ZUBROD ) '})
        self._process_command_list()
    
    #
    def _remove_mychart(self):
        self._clear_command_list()
        self._general_command('(?i)display progress note in mychart : (no|yes)', {None : ''})
        self._process_command_list()
        
    #
    def process_names(self):
        self._clear_command_list()
        self._general_command('(?i)ki-67 \(mm-1\)', {None : 'Ki-67'})
        text_list = []
        text_list.append('(?i)(pathologic( tumor)?|TNM) stag(e|ing)')
        text_list.append('(?i)stage summary')
        for text_str in text_list:
            self._general_command(text_str, {None : 'Stage'})
        self._process_command_list()
        
    #
    def _remove_see(self):
        self._clear_command_list()
        self._general_command('(?i)(\n\s*)?\( (please )?see [^\n\)\]]* \)', {None : ''})
        self._general_command('(?i)(\n\s*)?\( see case ' + self._case_number() + ' \)', {None : ''})
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
                    'part' + s() + '( )?' + part_label() + '( to ' + part_label() + ')?'
        self._substitution_endings_list(match_str)
        match_str = '(?i)((\n\s*)?-( )?)?(please[\n\s]+)?see (also )?' + \
                    'specimen' + s() + '( )?' + specimen_label() + '( to ' + specimen_label() + ')?'
        self._substitution_endings_list(match_str)
        
    #
    def _remove_slide(self):
        self._clear_command_list()
        self._general_command('(?i)\( slide' + s() + ' [^n\)\]]+ \)', {None : ''})
        self._general_command('(?i)(\n\s*)?\( (for example )?slide' + s() +  \
                              '[\n\s]+' + self._slide_label() + '(((,)? ' + self._slide_label() + ')+)?' + \
                              '(( and |-)' + self._slide_label() + ')? \)', {None : ''})
        self._general_command('(?i)(\n\s*)?\( (for example )?slide' + s() + \
                              '[\n\s]+' + self._slide_label() + \
                              '(((,)? ' + self._slide_label() + ')+)?' + \
                              '(( and |-)' + self._slide_label() + ')? \)', {None : ''})
        self._general_command('(?i)(\n\s*)?\( \d+ slide' + s() + ' \)', {None : ''})
        self._general_command('(?i)(, )?slide ' + self._slide_label(), {None : ''})
        self._process_command_list()
        
    #
    def _remove_tnm_staging(self):
        self._clear_command_list()
        self._general_command('(?i) \( pTNM \)', {None : ''})
        self._general_command('(?i) \( pT \)', {None : ''})
        self._general_command('(?i) \( pN \)', {None : ''})
        self._general_command('(?i) \( p?M \)', {None : ''})
        self._process_command_list()
    
    #
    def _slice_label(self):
        return('[0-9]+')
    
    #
    def _slide_label(self):
        return('([A-Z]*[0-9]*|[0-9]*[A-Z]*)')
        
    #
    def _substitution_endings_list(self, search_str):
        self._clear_command_list()
        self._general_command(search_str + '\n', {None : '\n'})
        self._general_command(search_str + '\t', {None : '\t'})
        self._general_command(search_str + ' ', {None : ' '})
        self._general_command(search_str + ',', {None : ','})
        self._general_command(search_str + '\.', {None : '.'})
        self._general_command(search_str + ';', {None : ';'})
        self._general_command(search_str + '( )?-', {None : '-'})
        self._process_command_list()
    
    #
    def _test_label(self):
        return('[a-z0-9\-]+')
    
    #
    def remove_extraneous_text(self):
        self._remove_mychart()
        self._remove_see()
        self._remove_slide()
        self._remove_tnm_staging()
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
        self._general_command('(?i)(\n\s*)?\( block' + s() + ' (#( )?)?' + self._block_label() + '(-' + self._block_label() + ')? \)', {None : ''})
        self._general_command('(?i)(\n\s*)?case number:[\n\s]+' + self._case_number(), {None : ''})
        self._general_command('(?i)\s*\( part' + s() + '-' + part_label() + '((-to-|-)' + part_label() + ' )? \)', {None : ''})
        self._general_command('(?i)(\n\s*)?\( spans slices ' + self._slice_label() + '-' + self._slice_label() + ' \)', {None : ''})
        self._general_command('(?i)slice (#( )?)?' + self._slice_label() + '((,)? )?(with clip((,)? )?)?', {None : ''})
        self._general_command('(?i)\( test # ' + self._test_label() + ' \)', {None : ''})
        self._general_command('(?i)check out the free oregon quit line(.*\n)*.*www . quitnow . net / oregon', {None : ''})
        self._process_command_list()