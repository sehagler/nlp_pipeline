# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 12:50:00 2020

@author: haglers
"""

#
import os
import re

#
from base_lib.postprocessor_base_class \
    import _build_data_dictionary, _build_document_frame, Postprocessor_base
import lambda_lib.tool_lib.lambda_tools as lambda_tools
from tools_lib.processing_tools_lib.function_processing_tools \
    import sequential_composition
from tools_lib.regex_lib.regex_tools \
    import (
        article,
        be,
        colon,
        comma,
        left_parenthesis,
        minus_sign,
        right_parenthesis,
        s,
        slash,
        space
    )
    
#
def _normalize_AR(text):
    text = \
        lambda_tools.initialism_lambda_conversion('androgen receptor', text, 'AR')
    return text

#
def _normalize_BCL2(text):
    text = \
        lambda_tools.lambda_conversion('BCL(( ?- ?)| )2', text, 'BCL2')
    return text
    
#
def _normalize_ER(text):
    text = \
        lambda_tools.initialism_lambda_conversion('estrogen receptor', text, 'ER')
    text = \
        lambda_tools.contextual_lambda_conversion('(?<![a-z])ER ' + left_parenthesis() + 'ER' + comma() + 'clone [A-Z0-9]+' + right_parenthesis(), 'ER' + comma() + 'clone', text, '')
    text = \
        lambda_tools.contextual_lambda_conversion('(?<![a-z])ER results' + comma() + 'clone [A-Z0-9]+', 'results' + comma() + 'clone', text, '')
    text = \
        lambda_tools.space_correction_lambda_conversion('(?<![a-z])ERs', text, 'ER')
    search_str = '(?<![a-z])ER ' + _receptor_predicate() + s()
    for _ in range(3):
        text = \
            lambda_tools.space_correction_lambda_conversion('(?<![a-z])' + search_str, text, 'ER')
    search_str = '(?<![a-z])ER(' + comma() + ')?' + _receptor_predicate() + s() + ' [a-zA-Z0-9]*'
    text = \
        lambda_tools.deletion_lambda_conversion(search_str, text)
    text = \
        lambda_tools.space_correction_lambda_conversion('(?<![a-z])ER(' + colon() + '|' + space() + ')?-', text, 'ER negative')
    text = \
        lambda_tools.space_correction_lambda_conversion('(?<![a-z])ER(' + colon() + '|' + space() + ')?neg(?![a-z])', text, 'ER negative')
    text = \
        lambda_tools.space_correction_lambda_conversion('(?<![a-z])ER(' + colon() + '|' + space() + ')?\+', text, 'ER positive')
    text = \
        lambda_tools.space_correction_lambda_conversion('(?<![a-z])ER(' + colon() + '|' + space() + ')?pos(?![a-z])', text, 'ER positive')
    return text

#
def _normalize_GATA3(text):
    text = \
        lambda_tools.lambda_conversion('(?<![a-z])GATA3', text, 'GATA3')
    text = \
        lambda_tools.lambda_conversion('(?<![a-z])GATA' + minus_sign() + '3', text, 'GATA3')
    return text

#
def _normalize_HER2(text):
    text = \
        lambda_tools.space_correction_lambda_conversion('(?<![a-z])HER(' + minus_sign() + '|' + slash() + ')?2(( |' + minus_sign() + '|' + slash() +')?(c' + minus_sign() + ')?neu)?( ?' + left_parenthesis() + 'cerb2' + right_parenthesis() + ')?', text,  'HER2')
    text = \
        lambda_tools.space_correction_lambda_conversion('(?<![a-z])HER2' + minus_sign() + slash() + '(c' + minus_sign() + ')?neu( ' + left_parenthesis() + 'cerb2' + right_parenthesis() + ')?', text, 'HER2')
    text = \
        lambda_tools.initialism_lambda_conversion('C' + minus_sign() + 'ERB B2 ' + left_parenthesis() + 'HER2' + right_parenthesis(), text, 'HER2')
    text = \
        lambda_tools.initialism_lambda_conversion('(?<![a-z])HER 2', text, 'HER2')
    text = \
        lambda_tools.space_correction_lambda_conversion('(?<![a-z])HER2(' + colon() + '|' + space() + ')?-', text, 'HER2 negative')
    text = \
        lambda_tools.space_correction_lambda_conversion('(?<![a-z])HER2(' + colon() + '|' + space() + ')?neg(?![a-z])', text, 'HER2 negative')
    text = \
        lambda_tools.space_correction_lambda_conversion('(?<![a-z])HER2(' + colon() + '|' + space() + ')?\+', text, 'HER2 positive')
    text = \
        lambda_tools.space_correction_lambda_conversion('(?<![a-z])HER2(' + colon() + '|' + space() + ')?pos(?![a-z])', text, 'HER2 positive')
    for _ in range(7):
        search_str = '(?<![a-z])HER2 ([a-z]* for )?' + \
                     _receptor_predicate() + s()
        text = \
            lambda_tools.space_correction_lambda_conversion(search_str, text, 'HER2')
    for _ in range(7):
        search_str = _receptor_predicate() + s() + '\s' + 'for HER2'
        text = \
            lambda_tools.space_correction_lambda_conversion(search_str, text, 'for HER2')
    text = \
        lambda_tools.space_correction_lambda_conversion(_receptor_predicate() + ' of HER2', text, 'HER2')
    text = \
        lambda_tools.space_correction_lambda_conversion('(?<![a-z])HER2 ' + _receptor_predicate(), text, 'HER2')
    return text

#
def _normalize_KI67(text):
    text = \
        lambda_tools.lambda_conversion('Ki' + minus_sign() + '67', text, 'KI67')
    text = \
        lambda_tools.lambda_conversion('KI67( ' + left_parenthesis() + 'mm-1' + right_parenthesis() + ')?', text, 'KI67')
    text = \
        lambda_tools.initialism_lambda_conversion('KI67', text, 'KI67')
    text = \
        lambda_tools.lambda_conversion('(KI67 )?(proliferati(on|ve))? (index|rate)', text, 'KI67')
    return text
#
def _normalize_PDL1(text):
    text = \
        lambda_tools.lambda_conversion('PD(( ?- ?)| )L1', text, 'PDL1')
    return text

#
def _normalize_PR(text):
    text = \
        lambda_tools.initialism_lambda_conversion('progesterone receptor', text, 'PR')
    text = \
        lambda_tools.contextual_lambda_conversion('(?<![a-z])PR ' + left_parenthesis() + 'PR' + comma() + 'clone [A-Z0-9]+' + right_parenthesis(), 'PR' + comma() + 'clone', text, '')
    text = \
        lambda_tools.contextual_lambda_conversion('(?<![a-z])PR results' + comma() + 'clone [A-Z0-9]+', 'results' + comma() + 'clone', text, '')
    text = \
        lambda_tools.space_correction_lambda_conversion('(?<![a-z])PRs', text, 'PR')
    search_str = '(?<![a-z])PR ' + _receptor_predicate() + s()
    for _ in range(3):
        text = \
            lambda_tools.space_correction_lambda_conversion('(?<![a-z])' + search_str, text, 'PR')
    search_str = '(?<![a-z])PR(' + comma() + ')?' + _receptor_predicate() + s() + ' [a-zA-Z0-9]*'
    text = \
        lambda_tools.deletion_lambda_conversion(search_str, text)
    text = \
        lambda_tools.space_correction_lambda_conversion('(?<![a-z])PR(' + colon() + '|' + space() + ')?-', text, 'PR negative')
    text = \
        lambda_tools.space_correction_lambda_conversion('(?<![a-z])PR(' + colon() + '|' + space() + ')?neg(?![a-z])', text, 'PR negative')
    text = \
        lambda_tools.space_correction_lambda_conversion('(?<![a-z])PR(' + colon() + '|' + space() + ')?\+', text, 'PR positive')
    text = \
        lambda_tools.space_correction_lambda_conversion('(?<![a-z])PR(' + colon() + '|' + space() + ')?pos(?![a-z])', text, 'PR positive')
    return text

#
def _normalize_biomarker_strength(text):
    text = \
        lambda_tools.initialism_lambda_conversion('dim - intermediate', text, 'dim-intermediate')
    text = \
        lambda_tools.initialism_lambda_conversion('dim - moderate', text, 'dim-moderate')
    text = \
        lambda_tools.initialism_lambda_conversion('dim - strong', text, 'dim-strong')
    text = \
        lambda_tools.initialism_lambda_conversion('intermediate ?- ?dim', text, 'dim-intermediate')
    text = \
        lambda_tools.initialism_lambda_conversion('intermediate - strong', text, 'intermediate-strong')
    text = \
        lambda_tools.initialism_lambda_conversion('intermediate ?- ?weak', text, 'weak-intermediate')
    text = \
        lambda_tools.initialism_lambda_conversion('moderate - dim', text, 'dim-moderate')
    text = \
        lambda_tools.initialism_lambda_conversion('moderate - strong', text, 'moderate-strong')
    text = \
        lambda_tools.initialism_lambda_conversion('moderate ?- ?weak', text, 'weak-moderate')
    text = \
        lambda_tools.initialism_lambda_conversion('strong ?- ?dim', text, 'dim-strong')
    text = \
        lambda_tools.initialism_lambda_conversion('strong ?- ?intermediate', text, 'intermediate-strong')
    text = \
        lambda_tools.initialism_lambda_conversion('strong ?- ?moderate', text, 'moderate-strong')
    text = \
        lambda_tools.initialism_lambda_conversion('strong ?- ?weak', text, 'weak-strong')
    text = \
        lambda_tools.initialism_lambda_conversion('weak - intermediate', text, 'weak-intermediate')
    text = \
        lambda_tools.initialism_lambda_conversion('weak - moderate', text, 'weak-moderate')
    text = \
        lambda_tools.initialism_lambda_conversion('weak - strong', text, 'weak-strong')
    return text

#
def _normalize_multiple_biomarkers(text):
    text = \
        lambda_tools.lambda_conversion('triple negative', text, 'ER negative, PR negative, HER2 negative')
    text = \
        lambda_tools.lambda_conversion('estrogen and progesterone( receptor' + s() + ')?', text, 'ER and PR')
    text = \
        lambda_tools.lambda_conversion('progesterone and estrogen( receptor' + s() + ')?', text, 'PR and ER')
    return text

#
def _receptor_predicate():
    return('(ampification|antigen|clone|(over)?expression|immunoreactivity|protein|receptor|status)')

#
def _remove_extraneous_text(text):
    text = \
        lambda_tools.deletion_lambda_conversion(left_parenthesis() + 'Hereceptest' + right_parenthesis(), text)
    text = \
        lambda_tools.deletion_lambda_conversion('by IHC', text)
    text = \
        lambda_tools.deletion_lambda_conversion(article() + ' positive ER or PR result requires.*moderate to strong nuclear staining( \.)?', text)
    text = \
        lambda_tools.lambda_conversion('(, )?Pathway TM', text, ' ')
    text = \
        lambda_tools.deletion_lambda_conversion(left_parenthesis() + 'PATHWAYTMHER2 kit ?, ?4B5' + right_parenthesis(), text)
    text = \
        lambda_tools.deletion_lambda_conversion(left_parenthesis() + 'PATHWAY(TMHER2| ' + left_parenthesis() + 'TM' + right_parenthesis() + ' HER2 ?) Kit( ?, clone [0-9A-Z]+)?' + right_parenthesis(), text)
    text = \
        lambda_tools.deletion_lambda_conversion('\* ' + article() + ' asterisk indicates that ' + article() + ' IHC.*computer assisted quantitative image analysis( \.)?', text)
    text = \
        lambda_tools.deletion_lambda_conversion(left_parenthesis() + 'analyte specific reagents.*clinical lab testing( \.)?' + right_parenthesis() + '( \.)?', text)
    text = \
        lambda_tools.deletion_lambda_conversion(left_parenthesis() + 'analyte specific reagents.*FDA( \.)?' + right_parenthesis() + '( \.)?', text)
    text = \
        lambda_tools.deletion_lambda_conversion('IHC stains are performed on formalin\-fixed(.*\n)*.*appropriate positive and negative controls( \.)?', text)
    text = \
        lambda_tools.deletion_lambda_conversion('Scoring and interpretation are per(.*\n)*.*' + left_parenthesis() + 'interpretation : positive' + right_parenthesis() + '( \.)?', text)
    text = \
        lambda_tools.deletion_lambda_conversion(article() + ' ER and PR stains are considered(.*\n)*.*Arch Pathol Lab Med 134\(6\) : 907 \- 22 \. 2010( \.)?', text)
    text = \
        lambda_tools.deletion_lambda_conversion(article() + ' ER and PR stains are considered(.*\n)*.*Indeterminate recommend repeat on another specimen( \.)?', text)
    text = \
        lambda_tools.deletion_lambda_conversion(article() + ' ER and PR IHC stains are performed(.*\n)*.*10% of ' + article() + ' tumor cells( \.)?', text)
    #text = \
    #    lambda_tools.deletion_lambda_conversion('Brightfield Dual ISH analysis(.*\n)*.*positive and negative controls( \.)?', text)
    text = \
        lambda_tools.deletion_lambda_conversion('HER2 IHC staining is performed with(.*\n)*.*Arch Pathol Lab Med 131:18 \- 43 \. 2007( \.)?', text)
    text = \
        lambda_tools.deletion_lambda_conversion('HER2 IHC staining is performed with(.*\n)*.*specimens[\- ]are fixed longer than 1 hour( \.)?', text)           
    text = \
        lambda_tools.deletion_lambda_conversion('HER2 scoring and interpretation are per(.*\n)*.*proficiency testing for ER , PR and HER2 IHC( \.)?', text)  
    text = \
        lambda_tools.deletion_lambda_conversion('HER2 (expression )?' + be() + ' expressed by ' + article() + ' ACIS score(.*\n)*.*confirm HER2 DNA amplification( \.)?', text)  
    text = \
        lambda_tools.deletion_lambda_conversion(article() + ' HER2 analysis is done(.*\n)*.*tissue sent for confirmation by FISH analysis( \.)?', text) 
    text = \
        lambda_tools.deletion_lambda_conversion(article() + ' ER , PR and HER2 IHC stains are performed(.*\n)*.*Inadequate specimens[\- ]are not reported \.', text) 
    text = \
        lambda_tools.deletion_lambda_conversion('; see ISH results below', text)
    return text
    
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
            consolidated_biomarker_dict[biomarker_name]['STRENGTH'] = []
            consolidated_biomarker_dict[biomarker_name]['VARIABILITY'] = []
            consolidated_biomarker_dict[biomarker_name]['SNIPPET'] = []
        for biomarker_dict in biomarker_dict_list:
            for biomarker_name in biomarker_dict.keys():
                for key in biomarker_dict[biomarker_name].keys():
                    if key != 'SNIPPET':
                        consolidated_biomarker_dict[biomarker_name][key].extend(biomarker_dict[biomarker_name][key])
                    else:
                        consolidated_biomarker_dict[biomarker_name][key].append(biomarker_dict[biomarker_name][key])
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
               len(consolidated_biomarker_dict[biomarker_name]['STRENGTH']) > 0 or \
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
                if biomarker_name != 'KI67' and \
                   len(consolidated_biomarker_dict[biomarker_name]['STRENGTH']) > 0:
                    value_dict[biomarker_name + '_STRENGTH'] = \
                        consolidated_biomarker_dict[biomarker_name]['STRENGTH']
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
            biomarker_name_list = [ 'AR', 'BCL2', 'CD4', 'CD8', 'ER', 'GATA3',
                                    'HER2', 'KI67', 'PDL1', 'PR' ]
            biomarker_name_text_list = []
            biomarker_status_text_list = []
            biomarker_strength_text_list = []
            biomarker_score_text_list = []
            biomarker_percentage_text_list = []
            snippet_text_list = []
            biomarker_name_offset_list = []
            for item in text_list[0]:
                biomarker_name_text_list.append(item[1].upper())
                biomarker_status_text_list.append(item[2])
                biomarker_strength_text_list.append(item[3])
                biomarker_score_text_list.append(item[4])
                biomarker_percentage_text_list.append(item[5])
                snippet_text_list.append(item[6])
                biomarker_name_offset_list.append(item[7])
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
            for snippet in unique_snippets:
                biomarker_dict = {}
                for biomarker_name in biomarker_name_list:
                    biomarker_dict[biomarker_name] = {}
                    biomarker_dict[biomarker_name]['STATUS'] = []
                    biomarker_dict[biomarker_name]['STRENGTH'] = []
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
                        biomarker_strength = \
                            self._process_strength(biomarker_strength_text_list[i])
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
                        if len(biomarker_strength) > 0:
                            biomarker_dict[biomarker_name]['STRENGTH'].append(biomarker_strength.lower())
                        if len(biomarker_variability) > 0:
                            biomarker_dict[biomarker_name]['VARIABILITY'].append(biomarker_variability.lower())
                    for biomarker_name in biomarker_name_list:
                        biomarker_dict[biomarker_name]['STATUS'] = \
                            list(set(biomarker_dict[biomarker_name]['STATUS']))
                        biomarker_dict[biomarker_name]['STRENGTH'] = \
                            list(set(biomarker_dict[biomarker_name]['STRENGTH']))
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
                            biomarker_strength = ''
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
                            if len(biomarker_strength) > 0:
                                biomarker_dict[biomarker_name]['STRENGTH'].append(biomarker_strength.lower())
                            if len(biomarker_variability) > 0:
                                biomarker_dict[biomarker_name]['VARIABILITY'].append(biomarker_variability.lower())
                    for biomarker_name in biomarker_name_list:
                        biomarker_dict[biomarker_name]['STATUS'] = \
                            list(set(biomarker_dict[biomarker_name]['STATUS']))
                        biomarker_dict[biomarker_name]['STRENGTH'] = \
                            list(set(biomarker_dict[biomarker_name]['STRENGTH']))
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
        if len(percentage) > 0:
            percentage += '%'
            percentage = re.sub('%+', '%', percentage)
        percentage = re.sub('> ?=', '>', percentage)
        percentage = re.sub('< ?=', '<', percentage)
        match = re.search('[0-9]+%-[0-9]+%', percentage)
        if match is not None:
            percentage = match.group(0)
        return percentage
    
    #
    def _process_score(self, score):
        score = lambda_tools.lambda_conversion(' \+', score, '+')
        score = \
            lambda_tools.lambda_conversion(' (/|(\( )?(out )?of) [0-4](\+)?( \))?', score, '')
        match = re.search('[0-4](\+)? (\-|to) [0-4](\+)?', score)
        if match is not None:
            score = \
                lambda_tools.lambda_conversion(' (\-|to) ', match.group(0), '-')
        score = re.sub(' (nuclear )?intensity', '', score)
        score = re.sub(' (nuclear )?staining', '', score)
        return score
        
    #
    def _process_status(self, biomarker_name, status):
        status = status.lower()
        status = re.sub(',', '', status)
        status = re.sub('( nuclear)? staining', '', status)
        status = re.sub('focal ', 'focally ', status)
        if biomarker_name in [ 'AR', 'BCL2', 'CD4', 'CD8', 'ER', 'GATA3',
                               'HER2', 'PDL1', 'PR' ]:
            for term in [ 'borderline', 'negative / positive' ]:
                status = re.sub(term, 'equivocal', status)
            for term in [ 'negativity', 'non-amplified', 'nonreactive',
                          'not amplified', 'unamplified', 'unfavorable',
                          'without immunoreactivity' ]:
                status = re.sub(term, 'negative', status)
            for term in [ 'amplified', 'favorable', 'immunoreactive',
                          'immunoreactivity', 'positivity', 'reactive',
                          'stains' ]:
                status = re.sub(term, 'positive', status)
        return status
    
    #
    def _process_strength(self, strength):
        strength = strength.lower()
        strength = re.sub('no (nuclear )?staining', 'none', strength)
        strength = re.sub('zero( (nuclear )?staining)?', 'none', strength)
        strength = re.sub(' immunoreactivity', '', strength)
        strength = re.sub(' (nuclear )?intensity', '', strength)
        strength = re.sub(' (nuclear )?staining', '', strength)
        strength = re.sub('no [a-z0-9]+ expression', 'none', strength)
        strength = re.sub(' [a-z0-9]+ expression', '', strength)
        strength = re.sub('high expression', 'high', strength)
        strength = re.sub('lacks? expression', 'none', strength)
        strength = re.sub('low expression', 'low', strength)
        strength = re.sub('no expression', 'none', strength)
        return strength
    
    #
    def push_data_dict(self, postprocessor_name, filename, data_dict,
                       sections_data_dict, document_list):
        data_dict_list = _build_data_dictionary(data_dict, document_list)
        sections_data_dict_list = _build_data_dictionary(sections_data_dict,
                                                         document_list)
        postprocessor_name = re.sub('postprocessor_', '', postprocessor_name)
        if postprocessor_name == filename:
            self.data_dict_list[0] = data_dict_list
            self.sections_data_dict = sections_data_dict_list
            self.filename = filename
        postprocessor_name_split = postprocessor_name.split('_')
        postprocessor_blocks_name = postprocessor_name_split[:-1]
        postprocessor_blocks_name.append('blocks')
        postprocessor_blocks_name.append(postprocessor_name_split[-1])
        postprocessor_blocks_name = '_'.join(postprocessor_blocks_name)
        if postprocessor_blocks_name == filename:
            self.data_dict_list[1] = data_dict_list
        postprocessor_name_split = postprocessor_name.split('_')
        postprocessor_variability_name = postprocessor_name_split[:-1]
        postprocessor_variability_name.append('variability')
        postprocessor_variability_name.append(postprocessor_name_split[-1])
        postprocessor_variability_name = '_'.join(postprocessor_variability_name)
        if postprocessor_variability_name == filename:
            self.data_dict_list[2] = data_dict_list

#
class Preprocessor(object):
    
    #
    def run_object(self, text):
        text = sequential_composition([_normalize_multiple_biomarkers,
                                       _normalize_AR,
                                       _normalize_BCL2,
                                       _normalize_ER,
                                       _normalize_GATA3,
                                       _normalize_HER2,
                                       _normalize_KI67,
                                       _normalize_PDL1,
                                       _normalize_PR,
                                       _normalize_biomarker_strength,
                                       _remove_extraneous_text], text)
        return text