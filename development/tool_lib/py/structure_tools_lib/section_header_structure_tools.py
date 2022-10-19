# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 10:' + self.max_pattern_repetitions + '9:' + self.max_pattern_repetitions + '8 2021

@author: haglers
"""

#
import re

#
from lambda_lib.lambda_manager_class import Lambda_manager
from regex_lib.regex_tools \
    import (
        amend,
        article,
        be,
        colon,
        datetime,
        diagnosis,
        medication,
        period,
        review_item,
        s
    )
from tool_lib.py.query_tools_lib.antigens_tools \
    import Section_header_structure as Antigens_section_header_structure
from tool_lib.py.query_tools_lib.fish_analysis_summary_tools \
    import Section_header_structure as Fish_analysis_summary_section_header_structure
from tool_lib.py.query_tools_lib.karyotype_tools \
    import Section_header_structure as Karyotype_section_header_structure
from tool_lib.py.query_tools_lib.base_lib.blasts_tools_base \
    import Section_header_structure as Blasts_section_header_structure

#
class Section_header_structure_tools(object):
    
    #
    def __init__(self):
        max_pattern_repetitions = 4
        self.prefix_str = '([a-z\(\)]+ ?){0,' + str(max_pattern_repetitions) + '}'
        self.antigens_section_header_structure = \
            Antigens_section_header_structure()
        self.blasts_section_header_structure = \
            Blasts_section_header_structure()
        self.fish_analysis_summary_section_header_structure = \
            Fish_analysis_summary_section_header_structure()
        self.karyotype_section_header_structure = \
            Karyotype_section_header_structure()
        self.lambda_manager = Lambda_manager()
        self._section_header_amendment_dict()
        self._section_header_dict()
        
    #
    def _add_punctuation_formatted(self, regex_dict):
        text_list = []
        if isinstance(regex_dict, dict):
            for key in regex_dict.keys():
                text = []
                text_in = regex_dict[key]
                if 'PRE_PUNCT' in key and 'POST_PUNCT' in key:
                    if isinstance(text_in, list):
                        for i in range(len(text_in)):
                            text.append(self._pre_punct() + text_in[i] + self._post_punct())
                    else:
                        text.append(self._pre_punct() + text_in + self._post_punct())
                elif 'PRE_PUNCT' in key:
                    if isinstance(text_in, list):
                        for i in range(len(text_in)):
                            text.append(self._pre_punct() + text_in[i])
                    else:
                        text.append(self._pre_punct() + text_in)
                else:
                    if isinstance(text_in, list):
                        for i in range(len(text_in)):
                            text.append(text_in[i])
                    else:
                        text.append(text_in)
                text_list.append(text)
        else:
            text_in = regex_dict
            text = []
            if isinstance(text_in, list):
                for i in range(len(text_in)):
                    text.append(self._pre_punct() + text_in[i] + self._post_punct())
            else:
                text.append(self._pre_punct() + text_in + self._post_punct())
            text_list.append(text)
        return text_list
    
    #
    def _post_punct(self):
        return '(' + colon() + '|' + period() + '|\n)'
        
    #
    def _pre_punct(self):
        return '(^|\n| )'
    
    #
    def _section_header_amendment_dict(self):
        self.section_header_amendment_dict = {}
        regex_dict = {}
        regex_list = []
        regex_list.append('(?i)\n' + article() + ' ([a-z]+ )?' + amend() + \
                          ' ' +  '(' + be() + '|reports)')
        regex_list.append('(?i)\n' + article() + ' ' + review_item() + \
                         ' ' + be() + ' (additionally|further|re)?( )?' + amend())
        regex_list.append('(?i)\n(' + article() + ' )?([a-z]+ )?' + \
                         amend() + '( ' + review_item() + ')?(' + self._post_punct() + '|\n)')
        regex_list.append('(?i)(' + article() + ' )?' + amend() + '( ' + \
                          review_item() + ')?\s?#\d' + self._post_punct())
        self.section_header_amendment_dict['AMENDMENT'] = regex_list
        regex_dict = {}
        regex_list = []
        regex_list.append(self._pre_punct() + '(' + article() + ' )?([a-z]+ )?' + \
                         amend() + ' comment' + s() + self._post_punct())
        regex_list.append(self._pre_punct() + amend() + ' comment' + s() + self._post_punct())
        regex_list.append(self._pre_punct() + amend() + ' comment' + s() + ' (\([^\)]*\))?' + self._post_punct())
        regex_list.append('(?i)(?<!see )' + amend() + ' comment' + s() + ' #\d' + self._post_punct())
        regex_list.append('(?i)(?<!see )' + amend() + ' note' + s() + self._post_punct())
        regex_dict['ADD PRE_PUNCT'] = regex_list
        self.section_header_amendment_dict['AMENDMENT COMMENT'] = regex_dict 
    
    #
    def _section_header_dict(self):
        self.section_header_dict = {}
        self.section_header_dict = \
            self.antigens_section_header_structure.add_section_header(self.section_header_dict)
        self.section_header_dict = \
            self.blasts_section_header_structure.add_section_header(self.section_header_dict)
        self.section_header_dict = \
            self.fish_analysis_summary_section_header_structure.add_section_header(self.section_header_dict)
        self.section_header_dict = \
            self.karyotype_section_header_structure.add_section_header(self.section_header_dict)

        # kludge until a better place to put these is identified    
        regex_dict = {}
        regex_list = []
        regex_list.append(self.prefix_str + 'inflammation')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['INFLAMMATION'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('microorganisms')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['MICROORGANISMS'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('csf cell count and differential')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['CSF DIFFERENTIAL'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('cytochemical stain' + s())
        regex_list.append('cytogenetic and fish studies')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['CYTOGENETIC AND FISH STUDIES'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('flow cytometric( immunologic)? analysis')
        regex_list.append('flow cytometry( results)?')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['FLOW CYTOMETRY RESULTS'] = regex_dict
        # kludge until a better place to put these is identified 
        
        self.section_header_dict = \
            self._section_header_structure(self.section_header_dict)

    #
    def _section_header_structure(self, section_header_dict):
        regex_dict = {}
        regex_list = []
        regex_list.append(self.prefix_str + 'addendum( \d+)?')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        section_header_dict['ADDENDUM'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append(self.prefix_str + 'adequacy')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        section_header_dict['ADEQUACY'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append(self.prefix_str + 'analysis')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        section_header_dict['ANALYSIS'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append(self.prefix_str + 'assessment')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        section_header_dict['ASSESSMENT'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('body site')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        section_header_dict['BODY SITE'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append(self.prefix_str + 'description')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        section_header_dict['DESCRIPTION'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append(self.prefix_str + '(diagnosis|dx)')
        regex_dict['ADD PRE)_PUNCT AND POST_PUNCT'] = regex_list
        section_header_dict['DIAGNOSIS'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append(self.prefix_str + 'evaluation')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        section_header_dict['EVALUATION'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append(self.prefix_str + 'examination')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        section_header_dict['EXAMINATION'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append(self.prefix_str + 'finding' + s())
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        section_header_dict['FINDING'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append(self.prefix_str + '(history|hx)')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        section_header_dict['HISTORY'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('impression' + s() + ' and recommendation' + s())
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        section_header_dict['IMPRESSION AND RECOMMENDATION'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append(self.prefix_str + 'index')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        section_header_dict['INDEX'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append(self.prefix_str + 'information')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        section_header_dict['INFORMATION'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append(self.prefix_str + 'interpretation')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        section_header_dict['INTERPRETATION'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('lab(oratory)? (data|results)( for this specimen)?')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        section_header_dict['LABORATORY DATA'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('materials received')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        section_header_dict['MATERIALS RECEIVED'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('method' + s())
        regex_list.append('methodology')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        section_header_dict['METHODOLOGY'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append(self.prefix_str + 'procedure')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        section_header_dict['PROCEDURE'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('reference' + s())
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        section_header_dict['REFERENCES'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append(self.prefix_str + 'result' + s())
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        section_header_dict['RESULT'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('case reviewed by')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        section_header_dict['REVIEWERS'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append(self.prefix_str + 'stain' + s())
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        section_header_dict['STAIN'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append(self.prefix_str + 'stud(ies|y)')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        section_header_dict['STUDY'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append(self.prefix_str + 'submitted')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        section_header_dict['SUBMITTED'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append(self.prefix_str + 'summary')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        section_header_dict['SUMMARY'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append(self.prefix_str + 'synopsis')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        section_header_dict['SYNOPSIS'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append(self.prefix_str + 'system')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        section_header_dict['SYSTEM'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append(self.prefix_str + 'technique')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        section_header_dict['TECHNIQUE'] = regex_dict
        return section_header_dict
        
    #
    def get_amendment_text_list(self, section_header):
        regex_list = self.section_header_amendment_dict[section_header]
        text_list = regex_list
        return text_list
        
    #
    def get_text_list(self, section_header):
        regex_list = self.section_header_dict[section_header]
        text_list = self._add_punctuation_formatted(regex_list)
        return text_list
        
    #
    def get_section_header_list(self):
        section_header_list = list(self.section_header_dict.keys())
        section_header_list.sort(key=len, reverse=True)
        return section_header_list