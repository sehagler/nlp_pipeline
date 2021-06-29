# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 12:50:00 2020

@author: haglers
"""

#
import re

#
from nlp_lib.py.postprocessing_lib.base_class_lib.postprocessor_base_class \
    import Postprocessor_base
from nlp_lib.py.document_preprocessing_lib.base_class_lib.preprocessor_base_class import Preprocessor_base
from tool_lib.py.processing_tools_lib.text_processing_tools import s

#
class Named_entity_recognition(Preprocessor_base):
    
    #
    def process_biomarkers(self):
        self._general_command('(?i)estrogen and progesterone( receptor' + s() + ')?',
                              {None : 'ER and PR'})
        self._general_command('(?i)progesterone and estrogen( receptor' + s() + ')?',
                              {None : 'PR and ER'})
        self._general_command('(?i)estrogen receptor( \( ER( , clone [A-Z0-9]+)? \))?', {None : 'ER'})
        self._general_command('(?i)HER(-| / )?2(( | / )?neu)?( \( cerb2 \))?', {None : 'HER2'})
        self._general_command('(?i)progesterone receptor( \( PR( , clone [A-Z0-9]+)? \))?', {None : 'PR'})
        self._general_command('(?i)immunohistochemi(cal|stry)', {None : 'IHC'})

#
class Postprocessor(Postprocessor_base):
    
    #
    def __init__(self, project_data, data_file, label):
        Postprocessor_base.__init__(self, project_data, label, data_file)
        self._extract_data_values()
        
    #
    def _extract_data_value(self, text_list):
        manual_review_str = 'MANUAL_REVIEW'
        if len(text_list) > 0:
            biomarker_name_text_list = text_list[1]
            biomarker_score_text_list = text_list[3]
            biomarker_status_text_list = text_list[2]
            context_text_list = text_list[4]
        else:
            biomarker_name_text_list = []
            biomarker_score_text_list = []
            biomarker_status_text_list = []
            context_text_list = []
        contexts = []
        for i in range(len(context_text_list)):
            contexts.append(context_text_list[i])
        unique_contexts = list(set(contexts))
        er_value_list = []
        her2_value_list = []
        pr_value_list = []
        for context in unique_contexts:
            er_score_text_list = []
            er_status_text_list = []
            her2_score_text_list = []
            her2_status_text_list = []
            pr_score_text_list = []
            pr_status_text_list = []
            for i in range(len(context_text_list)):
                if context_text_list[i] == context:
                    biomarker_name = biomarker_name_text_list[i]
                    biomarker_score = \
                        self._process_score(biomarker_score_text_list[i])
                    biomarker_status = \
                        self._process_status(biomarker_status_text_list[i])
                    if biomarker_name == 'ER':
                        if len(biomarker_score.lower()) > 0:
                            er_score_text_list.append(biomarker_score.lower())
                        if len(biomarker_status.lower()) > 0:
                            er_status_text_list.append(biomarker_status.lower())
                    elif biomarker_name == 'HER2':
                        if len(biomarker_score.lower()) > 0:
                            her2_score_text_list.append(biomarker_score.lower())
                        if len(biomarker_status.lower()) > 0:
                            her2_status_text_list.append(biomarker_status.lower())
                    elif biomarker_name == 'PR':
                        if len(biomarker_score.lower()) > 0:
                            pr_score_text_list.append(biomarker_score.lower())
                        if len(biomarker_status.lower()) > 0:
                            pr_status_text_list.append(biomarker_status.lower())
            er_value_list.append((er_status_text_list, er_score_text_list, context))
            her2_value_list.append((her2_status_text_list, her2_score_text_list, context))
            pr_value_list.append((pr_status_text_list, pr_score_text_list, context))
        value_dict_list = []
        for value in er_value_list:
            if len(value[0]) > 0 or len(value[1]) > 0:
                value_dict = {}
                if len(value[0]) == 1:
                    value_dict['ER_STATUS'] = value[0]
                elif len(value[0]) > 1:
                    value_dict['ER_STATUS'] = manual_review_str
                if len(value[1]) == 1:
                    value_dict['ER_SCORE'] = value[1]
                elif len(value[0]) > 1:
                    value_dict['ER_SCORE'] = manual_review_str
                value_dict['CONTEXT'] = value[2]
                value_dict_list.append(value_dict)
        for value in her2_value_list:
            if len(value[0]) > 0 or len(value[1]) > 0:
                value_dict = {}
                if len(value[0]) == 1:
                    value_dict['HER2_STATUS'] = value[0]
                elif len(value[0]) > 1:
                    value_dict['HER2_STATUS'] = manual_review_str
                if len(value[1]) == 1:
                    value_dict['HER2_SCORE'] = value[1]
                elif len(value[0]) > 1:
                    value_dict['HER2_SCORE'] = manual_review_str
                value_dict['CONTEXT'] = value[2]
                value_dict_list.append(value_dict)
        for value in pr_value_list:
            if len(value[0]) > 0 or len(value[1]) > 0:
                value_dict = {}
                if len(value[0]) == 1:
                    value_dict['PR_STATUS'] = value[0]
                elif len(value[0]) > 1:
                    value_dict['PR_STATUS'] = manual_review_str
                if len(value[1]) == 1:
                    value_dict['PR_SCORE'] = value[1]
                elif len(value[0]) > 1:
                    value_dict['PR_SCORE'] = manual_review_str
                value_dict['CONTEXT'] = value[2]
                value_dict_list.append(value_dict)
        return value_dict_list
    
    #
    def _process_score(self, score):
        score = re.sub(' (/|(out )?of) [0-4](\+)?', '', score)
        match = re.search('[0-4](\+)? \- [0-4](\+)?', score)
        if match is not None:
            score = re.sub(' \- ', ',', match.group(0))
            score = '(' + score +')'
        return score
        
    #
    def _process_status(self, status):
        if status.lower() in [ 'absent', 'non-amplified' ]:
            status = 'negative'
        elif status.lower() in [ 'amplified', 'immunoreactive', 'present',
                                 'strong' ]:
            status = 'positive'
        return status

#
class Summarization(Preprocessor_base):
    
    #
    def _receptor_predicate(self):
        return('(ampification|antigen|clone|(over)?expression|immunoreactivity|protein|receptor|status)')
        
    #
    def process_estrogen_receptor(self):
        self._general_command('(?i)\nERs', {None : '\nER'})
        self._general_command('(?i)\sERs', {None : ' ER'})
        self._general_command('(?i)ER SP1', {None : 'ER'})
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
    def process_her2(self):
        self._general_command(' \( PATHWAYTMHER2 kit , 4B5 \)', {None : ''})
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
    def process_progesterone_receptor(self):
        self._general_command('(?i)\nPRs', {None : '\nPR'})
        self._general_command('(?i)\sPRs', {None : ' PR'})
        self._general_command('(?i)PR IE2', {None : 'PR'})
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