# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 12:50:00 2020

@author: haglers
"""

#
import os
import re

#
from nlp_lib.py.base_lib.postprocessor_base_class \
    import Postprocessor_base
from nlp_lib.py.base_lib.preprocessor_base_class \
    import Preprocessor_base
from tool_lib.py.processing_tools_lib.text_processing_tools \
    import article, be, s

#
class Named_entity_recognition(Preprocessor_base):
    
    #
    def run_preprocessor(self):
        self._general_command('(?i)estrogen and progesterone( receptor' + s() + ')?',
                              {None : 'ER and PR'})
        self._general_command('(?i)progesterone and estrogen( receptor' + s() + ')?',
                              {None : 'PR and ER'})
        self._general_command('(?i)estrogen receptor', {None : 'ER'})
        self._general_command('(?i)ER \( ER \)', {None : 'ER'})
        self._general_command('(?i)ER \( ER , clone [A-Z0-9]+ \)', {'ER , clone' : ''})
        self._general_command('(?i)ER results , clone [A-Z0-9]+', {'results , clone' : ''})
        self._general_command('(?i)HER(-| / )?2(( | / )?(c-)?neu)?( \( cerb2 \))?', {None : 'HER2'})
        self._general_command('(?i)HER2- / (c-)?neu( \( cerb2 \))?', {None : 'HER2'})
        self._general_command('(?i)C-ERB B2 \( HER2 \)', {None: 'HER2'})
        self._general_command('(?i)Ki-67( \(mm-1\))?', {None : 'KI67'})
        self._general_command('(?i)progesterone receptor', {None : 'PR'})
        self._general_command('(?i)PR \( PR \)', {None : 'PR'})
        self._general_command('(?i)PR \( PR , clone [A-Z0-9]+ \)', {'PR , clone' : ''})
        self._general_command('(?i)PR results , clone [A-Z0-9]+', {'results , clone' : ''})
        self._general_command('(?i)immunohistochemi(cal|stry)', {None : 'IHC'})

#
class Postprocessor(Postprocessor_base):

    #
    def _extract_data_value(self, text_list):
        biomarker_name_list = [ 'ER', 'HER2', 'Ki67', 'PR' ]
        blocks_text_list = text_list[1]
        text_list = text_list[0]
        if len(text_list) > 0:
            biomarker_name_text_list = text_list[1]
            biomarker_status_text_list = text_list[2]
            biomarker_score_text_list = text_list[3]
            biomarker_percentage_text_list = text_list[4]
            neighborhood_text_list = text_list[5]
            biomarker_name_offset_list = text_list[6]
        else:
            biomarker_name_text_list = []
            biomarker_status_text_list = []
            biomarker_score_text_list = []
            biomarker_percentage_text_list = []
            neighborhood_text_list = []
            biomarker_name_offset_list = []
        if len(blocks_text_list) > 0:
            blocks_biomarker_name_text_list = blocks_text_list[1]
            blocks_biomarker_block_text_list = blocks_text_list[2]
            blocks_neighborhood_text_list = blocks_text_list[3]
            blocks_biomarker_name_offset_list = blocks_text_list[4]
        else:
            blocks_biomarker_name_text_list = []
            blocks_biomarker_block_text_list = []
            blocks_neighborhood_text_list = []
            blocks_biomarker_name_offset_list = []
        neighborhoods = []
        for i in range(len(neighborhood_text_list)):
            neighborhoods.append(neighborhood_text_list[i])
        unique_neighborhoods = list(set(neighborhoods))
        biomarker_dict_list = []
        er_value_list = []
        her2_value_list = []
        ki67_value_list = []
        pr_value_list = []
        for neighborhood in unique_neighborhoods:
            biomarker_dict = {}
            for biomarker_name in biomarker_name_list:
                biomarker_dict[biomarker_name] = {}
                biomarker_dict[biomarker_name]['STATUS'] = []
                biomarker_dict[biomarker_name]['SCORE'] = []
                biomarker_dict[biomarker_name]['PERCENTAGE'] = []
                biomarker_dict[biomarker_name]['BLOCK'] = []
            for i in range(len(neighborhood_text_list)):
                if neighborhood_text_list[i] == neighborhood:
                    biomarker_name = biomarker_name_text_list[i]
                    biomarker_status = \
                        self._process_status(biomarker_name,
                                             biomarker_status_text_list[i])
                    biomarker_score = \
                        self._process_score(biomarker_score_text_list[i])
                    biomarker_percentage = \
                        self._process_percentage(biomarker_percentage_text_list[i])
                    biomarker_offset = biomarker_name_offset_list[i][1]
                    biomarker_block = ''
                    for j in range(len(blocks_biomarker_name_offset_list)):
                        blocks_biomarker_offset = \
                            blocks_biomarker_name_offset_list[j][1]
                        if biomarker_offset == blocks_biomarker_offset:
                            biomarker_block = blocks_biomarker_block_text_list[j]
                    if len(biomarker_status) > 0:
                        biomarker_dict[biomarker_name]['STATUS'].append(biomarker_status.lower())
                    if len(biomarker_score) > 0:
                        biomarker_dict[biomarker_name]['SCORE'].append(biomarker_score.lower())
                    if len(biomarker_percentage) > 0:
                        biomarker_dict[biomarker_name]['PERCENTAGE'].append(biomarker_percentage.lower())
                    if len(biomarker_block) > 0:
                        biomarker_dict[biomarker_name]['BLOCK'].append(biomarker_block.upper())
                for biomarker_name in biomarker_name_list:
                    biomarker_dict[biomarker_name]['STATUS'] = \
                        list(set(biomarker_dict[biomarker_name]['STATUS']))
                    biomarker_dict[biomarker_name]['SCORE'] = \
                        list(set(biomarker_dict[biomarker_name]['SCORE']))
                    biomarker_dict[biomarker_name]['PERCENTAGE'] = \
                        list(set(biomarker_dict[biomarker_name]['PERCENTAGE']))
                    biomarker_dict[biomarker_name]['BLOCK'] = \
                        list(set(biomarker_dict[biomarker_name]['BLOCK']))
                    biomarker_dict[biomarker_name]['NEIGHBORHOOD'] = \
                        neighborhood
                if len(biomarker_dict['HER2']['STATUS']) > 1:
                    her2_status_text_list_tmp = [ x for x in \
                                                  biomarker_dict['HER2']['STATUS'] \
                                                  if x != 'equivocal' ]
                    if len(her2_status_text_list_tmp) > 0:
                        biomarker_dict['HER2']['STATUS'] = \
                            her2_status_text_list_tmp
                biomarker_dict_list.append(biomarker_dict)
        value_dict_list = []
        for biomarker_dict in biomarker_dict_list:
            for biomarker_name in biomarker_name_list:
                value_dict = {}
                if len(biomarker_dict[biomarker_name]['BLOCK']) > 0 or \
                   len(biomarker_dict[biomarker_name]['PERCENTAGE']) > 0 or \
                   len(biomarker_dict[biomarker_name]['SCORE']) > 0 or \
                   len(biomarker_dict[biomarker_name]['STATUS']) > 0:
                    if len(biomarker_dict[biomarker_name]['BLOCK']) > 1 or \
                       len(biomarker_dict[biomarker_name]['PERCENTAGE']) > 1 or \
                       len(biomarker_dict[biomarker_name]['SCORE']) > 1 or \
                       len(biomarker_dict[biomarker_name]['STATUS']) > 1:
                           biomarker_dict[biomarker_name]['BLOCK'] = \
                               self.manual_review
                           biomarker_dict[biomarker_name]['PERCENTAGE'] = \
                               self.manual_review
                           biomarker_dict[biomarker_name]['SCORE'] = \
                               self.manual_review
                           biomarker_dict[biomarker_name]['STATUS'] = \
                               self.manual_review
                    if len(biomarker_dict[biomarker_name]['STATUS']) > 0:
                        value_dict[ biomarker_name + '_STATUS'] = \
                            biomarker_dict[biomarker_name]['STATUS']
                    if biomarker_name != 'Ki67' and \
                       len(biomarker_dict[biomarker_name]['SCORE']) > 0:
                        value_dict[ biomarker_name + '_SCORE'] = \
                            biomarker_dict[biomarker_name]['SCORE']
                    if len(biomarker_dict[biomarker_name]['PERCENTAGE']) > 0:
                        value_dict[ biomarker_name + '_PERCENTAGE'] = \
                            biomarker_dict[biomarker_name]['PERCENTAGE']
                    if len(biomarker_dict[biomarker_name]['BLOCK']) > 0:
                        value_dict[ biomarker_name + '_BLOCK'] = \
                            biomarker_dict[biomarker_name]['BLOCK']
                    value_dict[ biomarker_name + '_NEIGHBORHOOD'] = \
                            biomarker_dict[biomarker_name]['NEIGHBORHOOD']
                    value_dict_list.append(value_dict)
        return value_dict_list
    
    #
    def _process_percentage(self, percentage):
        match = re.search('[0-9]+%-[0-9]+%', percentage)
        if match is not None:
            percentage = re.sub('(?<=%)-(?=[0-9])', ',', match.group(0))
            percentage = '(' + percentage + ')'
        return percentage
    
    #
    def _process_score(self, score):
        score = re.sub(' \+', '+', score)
        score = re.sub(' (/|(out )?of) [0-4](\+)?', '', score)
        match = re.search('[0-4](\+)? (\-|to) [0-4](\+)?', score)
        if match is not None:
            score = re.sub(' (\-|to) ', ',', match.group(0))
            score = '(' + score +')'
        match = re.search('(?i)no staining', score)
        if match is not None:
            score = '0'
        return score
        
    #
    def _process_status(self, biomarker_name, status):
        if biomarker_name in [ 'ER', 'HER2', 'PR' ]:
            if status.lower() in [ 'borderline' ]:
                status = 'equivocal'
            elif status.lower() in [ 'negativity', 'no', 'non-amplified', 
                                     'nonreactive', 'not amplified', 'unamplified',
                                     'unfavorable', 'without immunoreactivity']:
                status = 'negative'
            elif status.lower() in [ 'amplified', 'favorable', 'immunoreactive',
                                     'immunoreactivity', 'positivity', 'present',
                                     'reactive', 'strong', 'variable' ]:
                status = 'positive'
        return status

#
class Summarization(Preprocessor_base):
    
    #
    def _receptor_predicate(self):
        return('(ampification|antigen|clone|(over)?expression|immunoreactivity|protein|receptor|status)')
        
    #
    def _process_CK56(self):
        self._clear_command_list()
        self._general_command('(?i)CK5 / 6', {None : 'CK5/6'})
        self._process_command_list()
    
    #
    def _process_ER(self):
        self._general_command('(?i)\nERs', {None : '\nER'})
        self._general_command('(?i)\sERs', {None : ' ER'})
        self._general_command('[\n\s]+ER-', {None : ' ER '})
        search_str = 'ER ' + self._receptor_predicate() + s()
        for _ in range(3):
            self._general_command('(?i)\n' + search_str, {None : '\nER'})
            self._general_command('(?i)\s' + search_str, {None : ' ER'})
            self._general_command('(?i)' + search_str, {None : 'ER'})
        search_str = 'ER,? ' + self._receptor_predicate() + s() + ' [a-zA-Z0-9]*'
        for _ in range(2):
            self._general_command('(?i)[\n\s]+\( ' + search_str + ' \)', {None : ''})
            self._general_command('(?i)[\n\s]+' + search_str, {None : ''})
        self._general_command('(?i)\nER( :)?( )?-', {None : '\nER negative'})
        self._general_command('(?i)\sER( :)?( )?-', {None : ' ER negative'})
        self._general_command('(?i)\nER( :)?( )?\+', {None : '\nER positive'})
        self._general_command('(?i)\sER( :)?( )?\+', {None : ' ER positive'})
        
    #
    def _process_HER2(self):
        self._general_command('(?i)HER2( :)?( )?-', {None : 'HER2 negative'})
        self._general_command('(?i)HER2( :)?( )?\+', {None : 'HER2 positive'})
        for _ in range(7):
            search_str = '(?i)HER2 ([a-z]* for )?' + \
                         self._receptor_predicate() + s()
            self._general_command(search_str, {None : 'HER2'})
        for _ in range(7):
            search_str = self._receptor_predicate() + s() + '\s' + 'for HER2'
            self._general_command(search_str, {None : 'for HER2'})
        self._general_command('(?i)' + self._receptor_predicate() + ' of HER2', {None : 'HER2'})
        self._general_command('(?i)HER2 ' + self._receptor_predicate(), {None : 'HER2'})
        
    #
    def _process_PR(self):
        self._general_command('(?i)\nPRs', {None : '\nPR'})
        self._general_command('(?i)\sPRs', {None : ' PR'})
        self._general_command('[\n\s]+PR-', {None : ' PR '})
        search_str = 'PR ' + self._receptor_predicate() + s()
        for _ in range(3):
            self._general_command('(?i)\n' + search_str, {None : '\nPR'})
            self._general_command('(?i)\s' + search_str, {None : ' PR'})
            self._general_command('(?i)' + search_str, {None : 'PR'})
        search_str = 'PR,? ' + self._receptor_predicate() + s() + ' [a-zA-Z0-9]*'
        for _ in range(2):
            self._general_command('(?i)[\n\s]+\( ' + search_str + ' \)', {None : ''})
            self._general_command('(?i)[\n\s]+' + search_str, {None : ''})
        self._general_command('(?i)\nPR( :)?( )?-', {None : '\nPR negative'})
        self._general_command('(?i)\sPR( :)?( )?-', {None : ' PR negative'})
        self._general_command('(?i)\nPR( :)?( )?\+', {None : '\nPR positive'})
        self._general_command('(?i)\sPR( :)?( )?\+', {None : ' PR positive'})
        
    #
    def _remove_extraneous_text(self):
        self._general_command('(?i) \( Hereceptest \)', {None : ''})
        self._general_command('(?i)by IHC', {None : ''})
        self._general_command('(?i)' + article() + ' positive ER or PR result requires.*moderate to strong nuclear staining( \.)?', {None : ''})
        self._general_command('(?i)(, )?Pathway TM', {None : ''})
        self._general_command('(?i) \( PATHWAYTMHER2 kit , 4B5 \)', {None : ''})
        self._general_command('(?i)\( PATHWAY(TMHER2| \( TM \) HER2) Kit( , clone [0-9A-Z]+)? \)', {None : ''})
        self._general_command('(?i)\* ' + article() + ' asterisk indicates that ' + article() + ' IHC.*computer assisted quantitative image analysis( \.)?', {None : ''})
        self._general_command('(?i)\( analyte specific reagents.*clinical lab testing( \.)? \)( \.)?', {None : ''})
        self._general_command('(?i)\( analyte specific reagents.*FDA( \.)? \)( \.)?', {None : ''})
        self._general_command('(?i)IHC stains are performed on formalin\-fixed(.*\n)*.*appropriate positive and negative controls( \.)?', {None : ''})
        self._general_command('(?i)Scoring and interpretation are per(.*\n)*.*\( interpretation : positive \)( \.)?', {None : ''})
        self._general_command('(?i)' + article() + ' ER and PR stains are considered(.*\n)*.*Arch Pathol Lab Med 134\(6\) : 907 \- 22 \. 2010( \.)?', {None : ''})
        self._general_command('(?i)' + article() + ' ER and PR stains are considered(.*\n)*.*Indeterminate recommend repeat on another specimen( \.)?', {None : ''})
        self._general_command('(?i)' + article() + ' ER and PR IHC stains are performed(.*\n)*.*10% of ' + article() + ' tumor cells( \.)?', {None : ''})
        self._general_command('(?i)Brightfield Dual ISH analysis(.*\n)*.*positive and negative controls( \.)?', {None : ''})
        self._general_command('(?i)HER2 IHC staining is performed with(.*\n)*.*Arch Pathol Lab Med 131:18 \- 43 \. 2007( \.)?', {None : ''})
        self._general_command('(?i)HER2 IHC staining is performed with(.*\n)*.*specimens[\- ]are fixed longer than 1 hour( \.)?', {None : ''})
        self._general_command('(?i)HER2 scoring and interpretation are per(.*\n)*.*proficiency testing for ER , PR and HER2 IHC( \.)?', {None : ''})
        self._general_command('(?i)HER2 (expression )?' + be() + ' expressed by ' + article() + ' ACIS score(.*\n)*.*confirm HER2 DNA amplification( \.)?', {None : ''})
        self._general_command('(?i)' + article() + ' HER2 analysis is done(.*\n)*.*tissue sent for confirmation by FISH analysis( \.)?', {None : ''})
        self._general_command('(?i)' + article() + ' ER , PR and HER2 IHC stains are performed(.*\n)*.*Inadequate specimens[\- ]are not reported \.', {None : ''})
        self._general_command('(?i); see ISH results below', {None : ''})
        
    #
    def run_preprocessor(self):
        self._process_CK56()
        self._process_ER()
        self._process_HER2()
        self._process_PR()
        self._remove_extraneous_text()