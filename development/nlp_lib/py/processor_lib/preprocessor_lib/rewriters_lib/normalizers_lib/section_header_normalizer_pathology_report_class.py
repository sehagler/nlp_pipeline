# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 10:38:15 2020

@author: haglers
"""

#
from nlp_lib.py.base_class_lib.section_header_normalizer_base_class \
    import Section_header_normalizer_base
from nlp_lib.py.tool_lib.processing_tools_lib.text_processing_tools import article, be, s

#
class Section_header_normalizer_pathology_report(Section_header_normalizer_base):
        
    #
    def _post_punct(self):
        return('(:|\.|\n)([\n\s]*|$)')
        
    #
    def _pre_punct(self):
        return('(?i)(^|\n)')
    
    #
    def amendment(self, mode_flg):
        text_list = []
        text_list.append(self._pre_punct() + '(' + article() + ' )?([a-z]+ )?' + \
                         self._amend() + ' comment' + s() + self._post_punct())
        text_list.append(self._pre_punct() + self._amend() + ' comment' + s() + self._post_punct())
        text_list.append(self._pre_punct() + self._amend() + ' comment' + s() + ' (\([^\)]*\))?' + self._post_punct())
        text_list.append('(?i)(?<!see )' + self._amend() + ' comment' + s() + ' #\d' + self._post_punct())
        self._clear_command_list()
        self._pull_out_section_header_to_bottom_of_report(text_list, self._tagged_section_header('AMENDMENT COMMENT'), True)
        self._general_command(self._tagged_section_header('AMENDMENT COMMENT'), {None : self._tagged_section_header('AMENDMENT_COMMENT')})
        self._process_command_list()
        text_list = []
        text_list.append('(?i)(?<!see )' + self._amend() + ' note' + s() + self._post_punct())
        self._clear_command_list()
        self._pull_out_section_header_to_bottom_of_report(text_list, self._tagged_section_header('AMENDMENT COMMENT'), True)
        self._general_command(self._tagged_section_header('AMENDMENT COMMENT'), {None : self._tagged_section_header('AMENDMENT_COMMENT')})
        self._process_command_list()
        text_list = []
        text_list.append('(?i)\n' + article() + ' ([a-z]+ )?' + self._amend() + ' ' + \
                         '(' + be() + '|reports)')
        text_list.append('(?i)\n' + article() + ' ' + self._case() + \
                         ' ' + be() + ' (additionally|further|re)?( )?' + self._amend())
        text_list.append('(?i)\n(' + article() + ' )?([a-z]+ )?' + \
                         self._amend() + '( ' + self._case() + ')?(' + self._post_punct() + '|\n)')
        text_list.append('(?i)(' + article() + ' )?' + self._amend() + '( ' + self._case() + ')?\s?#\d' + self._post_punct())
        self._clear_command_list()
        self._pull_out_section_header_to_bottom_of_report(text_list, self._tagged_section_header('AMENDMENT'), True)
        self._general_command(self._tagged_section_header('AMENDMENT_COMMENT'), {None : self._tagged_section_header('AMENDMENT COMMENT')})
        self._process_command_list()
    
    #
    def antibodies_tested(self, mode_flg):
        text_list = []
        text_list.append(self._pre_punct() + 'anti(bodie|gen)s tested' + self._post_punct())
        text_list.append('(?i)' + article() + ' following antibodies were used' + self._post_punct())
        text_list.append('(?i)using ' + article() + ' following antibody combination' + self._post_punct())
        text_list.append('(?i)please see below for (' + article() + ' list of )?antibodies tested' + self._post_punct() + '(?=CD)')
        self._clear_command_list()
        self._general_command(text_list, self._tagged_section_header('ANTIBODIES TESTED'), True)
        self._process_command_list()
        
    #
    def background(self, mode_flg):
        text_list = []
        text_list.append('(background (and )?)?(information|method)' + s())
        self._normalize_section_header(mode_flg, text_list, 'BACKGROUND')
        
    #
    def bone_marrow(self, mode_flg):
        text_list = []
        text_list.append(self._pre_punct() + 'bone marrow aspirate( smear' + s() + ')?' + self._post_punct())
        text_list.append(self._pre_punct() + 'bone marrow (aspirate and )?touch prep(aration' + s() + ')?' + self._post_punct())
        text_list.append(self._pre_punct() + '(bilateral )?bone marrow aspirate' + s() + '(, (left|right) and (left|right))?' + self._post_punct())
        self._clear_command_list()
        self._general_command(text_list, self._tagged_section_header('BONE MARROW ASPIRATE SMEARS'), True)
        self._process_command_list()
        text_list = []
        text_list.append(self._pre_punct() + 'bone marrow (core )?(biopsy(/| and ))?clot section' + self._post_punct())
        text_list.append(self._pre_punct() + '(bilateral )?bone marrow (biopsies|biopsy cores) and clot section' + \
                         s() + '(, (left|right) and (left|right))?' + self._post_punct())
        text_list.append(self._pre_punct() + 'bone marrow (core )?biopsy' + self._post_punct())
        text_list.append(self._pre_punct() + 'clot section' + self._post_punct())
        self._clear_command_list()
        self._general_command(text_list, self._tagged_section_header('BONE MARROW CLOT SECTION'), True)
        self._process_command_list()
        text_list = []
        text_list.append(self._pre_punct() + '(' + article() + ' )?(bone marrow( aspirate)?|manual) differential(( count)? (\(.+\) )?includes)?[\n\s]*' + self._post_punct())
        text_list.append(self._pre_punct() + article() + ' differential count [ A-Za-z]+ includes[\n\s]*' + self._post_punct())
        self._clear_command_list()
        self._general_command(text_list, self._tagged_section_header('BONE MARROW DIFFERENTIAL'), True)
        self._process_command_list()
        
    #
    def cytogenetic_analysis_summary(self, mode_flg):
        text_list = []
        text_list.append('cytogenetic analysis summary')
        self._normalize_section_header(mode_flg, text_list, 'CYTOGENETIC ANALYSIS SUMMARY')
        
    #
    def cytogenetic_and_fish_studies(self, mode_flg):
        text_list = []
        text_list.append('cytochemical stain' + s())
        text_list.append('cytogenetic and fish studies')
        self._normalize_section_header(mode_flg, text_list, 'CYTOGENETIC AND FISH STUDIES')
        
    #
    def diagnosis(self, mode_flg):
        text_list = []
        text_list.append('pre( |-)' + self._amend() + ' (final )?(pathologic(al)? )?diagnosis')
        self._normalize_section_header(mode_flg, text_list, 'PREAMENDMENT DIAGNOSIS')
        text_list = []
        text_list.append('intraoperative consult \(frozen section\) diagnosis')
        text_list.append('frozen section diagnosis')
        self._normalize_section_header(mode_flg, text_list, 'DIAGNOSIS')
        
    #
    def explanation(self, mode_flg):
        text_list = []
        text_list.append('explanation of interpretation')
        self._normalize_section_header(mode_flg, text_list, 'EXPLANATION')
        
    #
    def fish_analysis_summary(self, mode_flg):
        text_list = []
        text_list.append('(interphase )?fish analysis summary')
        self._normalize_section_header(mode_flg, text_list, 'FISH ANALYSIS SUMMARY')

    #
    def flow_cytometric_analysis(self, mode_flg):
        text_list = []
        text_list.append('flow cytometr(ic (immunologic)?analysis|y)')
        self._normalize_section_header(mode_flg, text_list, 'FLOW CYTOMETRIC ANALYSIS')
        
    #
    def immunohistochemical_stains(self, mode_flg):
        text_list = []
        text_list.append('(microscopic description/)?immunohistochemi(cal stain' + s() + '|stry)')
        self._normalize_section_header(mode_flg, text_list, 'IMMUNOHISTOCHEMICAL STAINS')
        
    #
    def immunologic_analysis(self, mode_flg):
        text_list = []
        text_list.append('immunologic analysis')
        self._normalize_section_header(mode_flg, text_list, 'IMMUNOLOGIC ANALYSIS')
        
    #
    def interpretation(self, mode_flg):
        text_list = []
        text_list.append('interpretation')
        self._normalize_section_header(mode_flg, text_list, 'INTERPRETATION')
        
    #
    def karyotype(self, mode_flg):
        text_list = []
        text_list.append('karyotype' + s())
        self._normalize_section_header(mode_flg, text_list, 'KARYOTYPE')
        
    #
    def laboratory_data(self, mode_flg):
        text_list = []
        text_list.append('cbc')
        text_list.append('laboratory data([ \-]+CBC)?([ \-]+\d\d?/\d\d?/\d\d\d\d)?')
        self._normalize_section_header(mode_flg, text_list, 'LABORATORY DATA')
        
    #
    def materials_received(self, mode_flg):
        text_list = []
        text_list.append('materials received' + s())
        self._normalize_section_header(mode_flg, text_list, 'MATERIALS RECEIVED')
        
    #
    def method(self, mode_flg):
        text_list = []
        text_list.append('method' + s())
        self._normalize_section_header(mode_flg, text_list, 'METHOD')
        
    #
    def molecular_studies(self, mode_flg):
        text_list = []
        text_list.append('molecular studies')
        self._normalize_section_header(mode_flg, text_list, 'MOLECULAR STUDIES')
        
    #
    def peripheral_blood_morphology(self, mode_flg):
        self._clear_command_list()
        self._general_command([ '(?i)(?<!SUMMARY\n)\n(' + article() + ' )?peripheral blood (differential count includes|morphology|smear)' + self._post_punct() ], 
                              self._tagged_section_header('PERIPHERAL BLOOD MORPHOLOGY'), True)
        self._process_command_list()
        
    #
    def references(self, mode_flg):
        text_list = []
        text_list.append('reference' + s())
        self._normalize_section_header(mode_flg, text_list, 'REFERENCES')
        
    #
    def special_stains(self, mode_flg):
        text_list = []
        text_list.append('special stain' + s())
        self._normalize_section_header(mode_flg, text_list, 'SPECIAL STAINS')
        
    #
    def surgical_pathology_summary(self, mode_flg):
        text_list = []
        text_list.append('surgical pathology summary')
        self._normalize_section_header(mode_flg, text_list, 'SURGICAL PATHOLOGY SUMMARY')
        
    #
    def synopsis(self, mode_flg):
        text_list = []
        text_list.append('synopsis')
        self._normalize_section_header(mode_flg, text_list, 'SYNOPSIS')