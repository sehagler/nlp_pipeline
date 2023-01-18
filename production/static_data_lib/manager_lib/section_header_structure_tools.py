# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 10:' + self.max_pattern_repetitions + '9:' + self.max_pattern_repetitions + '8 2021

@author: haglers
"""

#
from tools_lib.regex_lib.regex_tools \
    import (
        s
    )
from query_lib.processor_lib.antigens_tools \
    import Section_header_structure as Antigens_section_header_structure
from query_lib.processor_lib.fish_analysis_summary_tools \
    import Section_header_structure as Fish_analysis_summary_section_header_structure
from query_lib.processor_lib.karyotype_tools \
    import Section_header_structure as Karyotype_section_header_structure
from query_lib.processor_lib.base_lib.blasts_tools_base \
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
        self._section_header_dict()
    
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
        regex_list.append(self.prefix_str + 'adequacy')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        section_header_dict['ADEQUACY'] = regex_dict
        '''
        regex_dict = {}
        regex_list = []
        regex_list.append(self.prefix_str + 'analysis')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        section_header_dict['ANALYSIS'] = regex_dict
        '''
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
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        section_header_dict['DX'] = regex_dict
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
        section_header_dict['HX'] = regex_dict
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
    def get_section_header_dict(self):
        return self.section_header_dict