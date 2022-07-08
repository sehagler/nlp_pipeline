# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 12:50:00 2020

@author: haglers
"""

#
import os
import re

#
from tool_lib.py.query_tools_lib.base_lib.postprocessor_base_class \
    import Postprocessor_base
from nlp_text_normalization_lib.base_lib.preprocessor_base_class \
    import Preprocessor_base
from tool_lib.py.processing_tools_lib.text_processing_tools \
    import article, be, s

#
class Named_entity_recognition(Preprocessor_base):
    
    #
    def run_preprocessor(self):
        
        #
        self._normalize_whitespace()
        
        #
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)estrogen and progesterone( receptor' + s() + ')?', self.text, 'ER and PR')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)progesterone and estrogen( receptor' + s() + ')?', self.text, 'PR and ER')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)androgen receptor', self.text, 'AR')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)BCL-2', self.text, 'BCL2')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)estrogen receptor', self.text, 'ER')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)GATA3', self.text, 'GATA3')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)GATA-3', self.text, 'GATA3')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)HER(-| / )?2(( | / )?(c-)?neu)?( \( cerb2 \))?', self.text, 'HER2')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)HER2- / (c-)?neu( \( cerb2 \))?', self.text, 'HER2')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)immunohistochemi(cal|stry)', self.text, 'IHC')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)Ki-67', self.text, 'KI67')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)PD-L1', self.text, 'PDL1')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)progesterone receptor', self.text, 'PR')
        
        #
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)AR \( AR \)', self.text, 'AR')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)ER \( ER \)', self.text, 'ER')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(?i)ER \( ER , clone [A-Z0-9]+ \)', 'ER , clone', self.text, '')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(?i)ER results , clone [A-Z0-9]+', 'results , clone', self.text, '')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)C-ERB B2 \( HER2 \)', self.text, 'HER2')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)proliferati(on|ve) (index|rate) \( KI67 \)', self.text, 'KI67')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)KI67( proliferati(on|ve))? (index|rate)', self.text, 'KI67')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)KI67( \(mm-1\))?', self.text, 'KI67')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)KI67 \( KI67 \)', self.text, 'KI67')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)PR \( PR \)', self.text, 'PR')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(?i)PR \( PR , clone [A-Z0-9]+ \)', 'PR , clone', self.text, '')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(?i)PR results , clone [A-Z0-9]+', 'results , clone', self.text, '')

#
class Postprocessor(Postprocessor_base):
    
    #
    def _create_consolidated_dict(self, biomarker_dict_list):
        consolidated_biomarker_dict = {}
        consolidated_biomarker_name_list = []
        for biomarker_dict in biomarker_dict_list:
            consolidated_biomarker_name_list.extend(list(biomarker_dict.keys()))
        consolidated_biomarker_name_list = \
            list(set(consolidated_biomarker_name_list))
        for biomarker_name in consolidated_biomarker_name_list:
            consolidated_biomarker_dict[biomarker_name] = {}
            consolidated_biomarker_dict[biomarker_name]['BLOCK'] = []
            consolidated_biomarker_dict[biomarker_name]['PERCENTAGE'] = []
            consolidated_biomarker_dict[biomarker_name]['SCORE'] = []
            consolidated_biomarker_dict[biomarker_name]['STATUS'] = []
            consolidated_biomarker_dict[biomarker_name]['VARIABILITY'] = []
            consolidated_biomarker_dict[biomarker_name]['SNIPPET'] = []
        for biomarker_dict in biomarker_dict_list:
            for biomarker_name in biomarker_dict.keys():
                for key in biomarker_dict[biomarker_name].keys():
                    if key != 'SNIPPET':
                        consolidated_biomarker_dict[biomarker_name][key].extend(biomarker_dict[biomarker_name][key])
                    else:
                        consolidated_biomarker_dict[biomarker_name][key].append(biomarker_dict[biomarker_name][key])
        for biomarker_name in consolidated_biomarker_dict.keys():
            if len(consolidated_biomarker_dict[biomarker_name]['BLOCK']) > 1 or \
               len(consolidated_biomarker_dict[biomarker_name]['PERCENTAGE']) > 1 or \
               len(consolidated_biomarker_dict[biomarker_name]['SCORE']) > 1 or \
               len(consolidated_biomarker_dict[biomarker_name]['STATUS']) > 1 or \
               len(consolidated_biomarker_dict[biomarker_name]['VARIABILITY']) > 1:
                   consolidated_biomarker_dict[biomarker_name]['BLOCK'] = \
                       self.manual_review
                   consolidated_biomarker_dict[biomarker_name]['PERCENTAGE'] = \
                       self.manual_review
                   consolidated_biomarker_dict[biomarker_name]['SCORE'] = \
                       self.manual_review
                   consolidated_biomarker_dict[biomarker_name]['STATUS'] = \
                       self.manual_review
                   consolidated_biomarker_dict[biomarker_name]['VARIABILITY'] = \
                       self.manual_review
                   consolidated_biomarker_dict[biomarker_name]['SNIPPET'] = \
                       self.manual_review
        return consolidated_biomarker_dict
    
    #
    def _create_value_dict_list(self, consolidated_biomarker_dict):
        value_dict_list = []
        for biomarker_name in consolidated_biomarker_dict.keys():
            value_dict = {}
            if len(consolidated_biomarker_dict[biomarker_name]['BLOCK']) > 0 or \
               len(consolidated_biomarker_dict[biomarker_name]['PERCENTAGE']) > 0 or \
               len(consolidated_biomarker_dict[biomarker_name]['SCORE']) > 0 or \
               len(consolidated_biomarker_dict[biomarker_name]['STATUS']) > 0 or \
               len(consolidated_biomarker_dict[biomarker_name]['VARIABILITY']) > 0:
                if len(consolidated_biomarker_dict[biomarker_name]['BLOCK']) > 0:
                    value_dict[biomarker_name + '_BLOCK'] = \
                        consolidated_biomarker_dict[biomarker_name]['BLOCK']
                if len(consolidated_biomarker_dict[biomarker_name]['PERCENTAGE']) > 0:
                    value_dict[biomarker_name + '_PERCENTAGE'] = \
                        consolidated_biomarker_dict[biomarker_name]['PERCENTAGE']
                if biomarker_name != 'KI67' and \
                   len(consolidated_biomarker_dict[biomarker_name]['SCORE']) > 0:
                    value_dict[biomarker_name + '_SCORE'] = \
                        consolidated_biomarker_dict[biomarker_name]['SCORE']
                if len(consolidated_biomarker_dict[biomarker_name]['STATUS']) > 0:
                    value_dict[biomarker_name + '_STATUS'] = \
                        consolidated_biomarker_dict[biomarker_name]['STATUS']
                if len(consolidated_biomarker_dict[biomarker_name]['VARIABILITY']) > 0:
                    value_dict[biomarker_name + '_VARIABILITY'] = \
                        consolidated_biomarker_dict[biomarker_name]['VARIABILITY']
                value_dict['SNIPPET'] = \
                        consolidated_biomarker_dict[biomarker_name]['SNIPPET']
                value_dict_list.append(value_dict)
        return value_dict_list
    
    #
    def _extract_data_value(self, value_list_dict):
        extracted_data_dict = {}
        for key in value_list_dict.keys():
            text_list = value_list_dict[key]
            biomarker_name_list = [ 'ER', 'GATA3', 'HER2', 'KI67', 'PR' ]
            biomarker_name_text_list = []
            biomarker_status_text_list = []
            biomarker_score_text_list = []
            biomarker_percentage_text_list = []
            snippet_text_list = []
            biomarker_name_offset_list = []
            for item in text_list[0]:
                biomarker_name_text_list.append(item[1].upper())
                biomarker_status_text_list.append(item[2])
                biomarker_score_text_list.append(item[3])
                biomarker_percentage_text_list.append(item[4])
                snippet_text_list.append(item[5])
                biomarker_name_offset_list.append(item[6])
            blocks_biomarker_name_text_list = []
            blocks_biomarker_block_text_list = []
            blocks_snippet_text_list = []
            blocks_biomarker_name_offset_list = []
            for item in text_list[1]:
                blocks_biomarker_name_text_list.append(item[1].upper())
                blocks_biomarker_block_text_list.append(item[2])
                blocks_snippet_text_list.append(item[3])
                blocks_biomarker_name_offset_list.append(item[4])
            variability_biomarker_name_text_list = []
            variability_biomarker_variability_text_list = []
            variability_snippet_text_list = []
            variability_biomarker_name_offset_list = []
            for item in text_list[2]:
                variability_biomarker_name_text_list.append(item[1].upper())
                variability_biomarker_variability_text_list.append(item[2])
                variability_snippet_text_list.append(item[3])
                variability_biomarker_name_offset_list.append(item[4])
            snippets = []
            for i in range(len(snippet_text_list)):
                snippets.append(snippet_text_list[i])
            for i in range(len(variability_snippet_text_list)):
                snippets.append(variability_snippet_text_list[i])
            unique_snippets = list(set(snippets))
            for i in range(len(unique_snippets)):
                unique_snippets[i] = ''.join(unique_snippets[i])
            biomarker_dict_list = []
            er_value_list = []
            her2_value_list = []
            ki67_value_list = []
            pr_value_list = []
            for snippet in unique_snippets:
                biomarker_dict = {}
                for biomarker_name in biomarker_name_list:
                    biomarker_dict[biomarker_name] = {}
                    biomarker_dict[biomarker_name]['STATUS'] = []
                    biomarker_dict[biomarker_name]['SCORE'] = []
                    biomarker_dict[biomarker_name]['PERCENTAGE'] = []
                    biomarker_dict[biomarker_name]['BLOCK'] = []
                    biomarker_dict[biomarker_name]['VARIABILITY'] = []
                snippet_found_flg = False
                for i in range(len(snippet_text_list)):
                    if snippet_text_list[i] == snippet:
                        snippet_found_flg = True
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
                        biomarker_variability = ''
                        for j in range(len(variability_biomarker_name_offset_list)):
                            variability_biomarker_offset = \
                                variability_biomarker_name_offset_list[j][1]
                            if biomarker_offset == variability_biomarker_offset:
                                biomarker_variability = \
                                    variability_biomarker_variability_text_list[j]
                        for j in range(len(blocks_biomarker_name_offset_list)):
                            blocks_biomarker_offset = \
                                blocks_biomarker_name_offset_list[j][1]
                            if biomarker_offset == blocks_biomarker_offset:
                                biomarker_block = blocks_biomarker_block_text_list[j]
                        if len(biomarker_block) > 0:
                            biomarker_dict[biomarker_name]['BLOCK'].append(biomarker_block.upper())
                        if len(biomarker_percentage) > 0:
                            biomarker_dict[biomarker_name]['PERCENTAGE'].append(biomarker_percentage.lower())
                        if len(biomarker_score) > 0:
                            biomarker_dict[biomarker_name]['SCORE'].append(biomarker_score.lower())
                        if len(biomarker_status) > 0:
                            biomarker_dict[biomarker_name]['STATUS'].append(biomarker_status.lower())
                        if len(biomarker_variability) > 0:
                            biomarker_dict[biomarker_name]['VARIABILITY'].append(biomarker_variability.lower())
                    for biomarker_name in biomarker_name_list:
                        biomarker_dict[biomarker_name]['STATUS'] = \
                            list(set(biomarker_dict[biomarker_name]['STATUS']))
                        biomarker_dict[biomarker_name]['SCORE'] = \
                            list(set(biomarker_dict[biomarker_name]['SCORE']))
                        biomarker_dict[biomarker_name]['PERCENTAGE'] = \
                            list(set(biomarker_dict[biomarker_name]['PERCENTAGE']))
                        biomarker_dict[biomarker_name]['BLOCK'] = \
                            list(set(biomarker_dict[biomarker_name]['BLOCK']))
                        biomarker_dict[biomarker_name]['VARIABILITY'] = \
                            list(set(biomarker_dict[biomarker_name]['VARIABILITY']))
                        biomarker_dict[biomarker_name]['SNIPPET'] = snippet
                if False: #snippet_found_flg == False:
                    for i in range(len(variability_snippet_text_list)):
                        if variability_snippet_text_list[i] == snippet:
                            biomarker_name = variability_biomarker_name_text_list[i]
                            biomarker_status = ''
                            biomarker_score = ''
                            biomarker_percentage = ''
                            biomarker_block = ''
                            biomarker_variability = \
                                variability_biomarker_variability_text_list[i]
                            if len(biomarker_block) > 0:
                                biomarker_dict[biomarker_name]['BLOCK'].append(biomarker_block.upper())
                            if len(biomarker_percentage) > 0:
                                biomarker_dict[biomarker_name]['PERCENTAGE'].append(biomarker_percentage.lower())
                            if len(biomarker_score) > 0:
                                biomarker_dict[biomarker_name]['SCORE'].append(biomarker_score.lower())
                            if len(biomarker_status) > 0:
                                biomarker_dict[biomarker_name]['STATUS'].append(biomarker_status.lower())
                            if len(biomarker_variability) > 0:
                                biomarker_dict[biomarker_name]['VARIABILITY'].append(biomarker_variability.lower())
                    for biomarker_name in biomarker_name_list:
                        biomarker_dict[biomarker_name]['STATUS'] = \
                            list(set(biomarker_dict[biomarker_name]['STATUS']))
                        biomarker_dict[biomarker_name]['SCORE'] = \
                            list(set(biomarker_dict[biomarker_name]['SCORE']))
                        biomarker_dict[biomarker_name]['PERCENTAGE'] = \
                            list(set(biomarker_dict[biomarker_name]['PERCENTAGE']))
                        biomarker_dict[biomarker_name]['BLOCK'] = \
                            list(set(biomarker_dict[biomarker_name]['BLOCK']))
                        biomarker_dict[biomarker_name]['VARIABILITY'] = \
                            list(set(biomarker_dict[biomarker_name]['VARIABILITY']))
                        biomarker_dict[biomarker_name]['SNIPPET'] = snippet
                if bool(biomarker_dict):
                    biomarker_dict_list.append(biomarker_dict)
            consolidated_biomarker_dict = \
                self._create_consolidated_dict(biomarker_dict_list)
            value_dict_list = \
                self._create_value_dict_list(consolidated_biomarker_dict)
            extracted_data_dict[key] = value_dict_list
        return extracted_data_dict
    
    #
    def _process_percentage(self, percentage):
        match = re.search('[0-9]+%-[0-9]+%', percentage)
        if match is not None:
            percentage = \
                self.lambda_manager.lambda_conversion('(?<=%)-(?=[0-9])',
                                                      match.group(0), ',')
            percentage = '(' + percentage + ')'
        return percentage
    
    #
    def _process_score(self, score):
        score = self.lambda_manager.lambda_conversion(' \+', score, '+')
        score = \
            self.lambda_manager.lambda_conversion(' (/|(out )?of) [0-4](\+)?',
                                                  score, '')
        match = re.search('[0-4](\+)? (\-|to) [0-4](\+)?', score)
        if match is not None:
            score = \
                self.lambda_manager.lambda_conversion(' (\-|to) ',
                                                      match.group(0), ',')
            score = '(' + score +')'
        match = re.search('(?i)no staining', score)
        if match is not None:
            score = '0'
        return score
        
    #
    def _process_status(self, biomarker_name, status):
        if biomarker_name in [ 'ER', 'GATA3', 'HER2', 'PR' ]:
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
    def _process_ER(self):
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)\nERs', self.text, '\nER')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)\sERs', self.text, ' ER')
        self.text = \
            self.lambda_manager.lambda_conversion('[\n\s]+ER-', self.text, ' ER ')
        search_str = 'ER ' + self._receptor_predicate() + s()
        for _ in range(3):
            self.text = \
                self.lambda_manager.lambda_conversion('(?i)\n' + search_str, self.text, '\nER')
            self.text = \
                self.lambda_manager.lambda_conversion('(?i)\s' + search_str, self.text, ' ER')
            self.text = \
                self.lambda_manager.lambda_conversion('(?i)' + search_str, self.text, 'ER')
        search_str = 'ER,? ' + self._receptor_predicate() + s() + ' [a-zA-Z0-9]*'
        for _ in range(2):
            self.text = \
                self.lambda_manager.deletion_lambda_conversion('(?i)[\n\s]+\( ' + search_str + ' \)', self.text)
            self.text = \
                self.lambda_manager.deletion_lambda_conversion('(?i)[\n\s]+' + search_str, self.text)
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)\nER( :)?( )?-', self.text, '\nER negative')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)\sER( :)?( )?-', self.text, ' ER negative')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)\nER( :)?( )?\+', self.text, '\nER positive')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)\sER( :)?( )?\+', self.text, ' ER positive')
        
    #
    def _process_HER2(self):
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)HER2( :)?( )?-', self.text, 'HER2 negative')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)HER2neg', self.text, 'HER2 negative')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)HER2( :)?( )?\+', self.text, 'HER2 positive')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)HER2pos', self.text, 'HER2 negative')
        for _ in range(7):
            search_str = '(?i)HER2 ([a-z]* for )?' + \
                         self._receptor_predicate() + s()
            self.text = \
                self.lambda_manager.lambda_conversion(search_str, self.text, 'HER2')
        for _ in range(7):
            search_str = self._receptor_predicate() + s() + '\s' + 'for HER2'
            self.text = \
                self.lambda_manager.lambda_conversion(search_str, self.text, 'for HER2')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)' + self._receptor_predicate() + ' of HER2', self.text, 'HER2')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)HER2 ' + self._receptor_predicate(), self.text, 'HER2')
        
    #
    def _process_PR(self):
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)\nPRs', self.text, '\nPR')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)\sPRs', self.text, ' PR')
        self.text = \
            self.lambda_manager.lambda_conversion('[\n\s]+PR-', self.text, ' PR ')
        search_str = 'PR ' + self._receptor_predicate() + s()
        for _ in range(3):
            self.text = \
                self.lambda_manager.lambda_conversion('(?i)\n' + search_str, self.text, '\nPR')
            self.text = \
                self.lambda_manager.lambda_conversion('(?i)\s' + search_str, self.text, ' PR')
            self.text = \
                self.lambda_manager.lambda_conversion('(?i)' + search_str, self.text, 'PR')
        search_str = 'PR,? ' + self._receptor_predicate() + s() + ' [a-zA-Z0-9]*'
        for _ in range(2):
            self.text = \
                self.lambda_manager.deletion_lambda_conversion('(?i)[\n\s]+\( ' + search_str + ' \)', self.text)
            self.text = \
                self.lambda_manager.deletion_lambda_conversion('(?i)[\n\s]+' + search_str, self.text)
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)\nPR( :)?( )?-', self.text, '\nPR negative')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)\sPR( :)?( )?-', self.text, ' PR negative')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)\nPR( :)?( )?\+', self.text, '\nPR positive')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)\sPR( :)?( )?\+', self.text, ' PR positive')
        
    #
    def _remove_extraneous_text(self):
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i) \( Hereceptest \)', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)by IHC', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)' + article() + ' positive ER or PR result requires.*moderate to strong nuclear staining( \.)?', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)(, )?Pathway TM', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i) \( PATHWAYTMHER2 kit , 4B5 \)', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)\( PATHWAY(TMHER2| \( TM \) HER2) Kit( , clone [0-9A-Z]+)? \)', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)\* ' + article() + ' asterisk indicates that ' + article() + ' IHC.*computer assisted quantitative image analysis( \.)?', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)\( analyte specific reagents.*clinical lab testing( \.)? \)( \.)?', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)\( analyte specific reagents.*FDA( \.)? \)( \.)?', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)IHC stains are performed on formalin\-fixed(.*\n)*.*appropriate positive and negative controls( \.)?', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)Scoring and interpretation are per(.*\n)*.*\( interpretation : positive \)( \.)?', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)' + article() + ' ER and PR stains are considered(.*\n)*.*Arch Pathol Lab Med 134\(6\) : 907 \- 22 \. 2010( \.)?', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)' + article() + ' ER and PR stains are considered(.*\n)*.*Indeterminate recommend repeat on another specimen( \.)?', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)' + article() + ' ER and PR IHC stains are performed(.*\n)*.*10% of ' + article() + ' tumor cells( \.)?', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)Brightfield Dual ISH analysis(.*\n)*.*positive and negative controls( \.)?', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)HER2 IHC staining is performed with(.*\n)*.*Arch Pathol Lab Med 131:18 \- 43 \. 2007( \.)?', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)HER2 IHC staining is performed with(.*\n)*.*specimens[\- ]are fixed longer than 1 hour( \.)?', self.text)           
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)HER2 scoring and interpretation are per(.*\n)*.*proficiency testing for ER , PR and HER2 IHC( \.)?', self.text)  
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)HER2 (expression )?' + be() + ' expressed by ' + article() + ' ACIS score(.*\n)*.*confirm HER2 DNA amplification( \.)?', self.text)  
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)' + article() + ' HER2 analysis is done(.*\n)*.*tissue sent for confirmation by FISH analysis( \.)?', self.text) 
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)' + article() + ' ER , PR and HER2 IHC stains are performed(.*\n)*.*Inadequate specimens[\- ]are not reported \.', self.text) 
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i); see ISH results below', self.text) 
        
    #
    def run_preprocessor(self):
        self._process_ER()
        self._process_HER2()
        self._process_PR()
        self._remove_extraneous_text()