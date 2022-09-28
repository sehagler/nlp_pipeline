# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 10:49:48 2021

@author: haglers
"""

#
import re

#
from lambda_lib.lambda_manager_class import Lambda_manager
from regex_lib.regex_tools \
    import amend, article, be, datetime, diagnosis, medication, review_item, s

#
class Section_header_structure_tools(object):
    
    #
    def __init__(self):
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
                            text.append('(^|\n| )' + text_in[i] + '(:|\.|\n)')
                    else:
                        text.append('(^|\n| )' + text_in + '(:|\.|\n)')
                elif 'PRE_PUNCT' in key:
                    if isinstance(text_in, list):
                        for i in range(len(text_in)):
                            text.append('(^|\n| )' + text_in[i])
                    else:
                        text.append('(^|\n| )' + text_in)
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
                    text.append('(^|\n| )' + text_in[i] + '(:|\.|\n)')
            else:
                text.append('(^|\n| )' + text_in + '(:|\.|\n)')
            text_list.append(text)
        return text_list
        
    '''
    #
    def _add_punctuation_unformatted(self, regex_dict, no_punctuation_flg):
        text_list = []
        if isinstance(regex_dict, dict):
            for key in regex_dict.keys():
                text = []
                text_in = regex_dict[key]
                if isinstance(text_in, list):
                    for i in range(len(text_in)):
                            text.append('( |\n)' + text_in[i] + '(( updated)? \d+/\d+/\d+)?( )?(:|;)')
                else:
                    text.append('( |\n)' + text_in + '(( updated)? \d+/\d+/\d+)?( )?(:|;)')
                if no_punctuation_flg:
                    if isinstance(text_in, list):
                        for i in range(len(text_in)):
                            text_in_upper = text_in[i].upper()
                            text_in_upper = \
                                self.lambda_manager.lambda_conversion('\(\?I\)', text_in_upper, '(?i)')
                            text.append('(?<!<<<)' + text_in_upper)
                    else:
                        text_in_upper = text_in.upper()
                        text_in_upper = \
                            self.lambda_manager.lambda_conversion('\(\?I\)', text_in_upper, '(?i)')
                        text.append('(?<!<<<)' + text_in_upper)
                text_list.append(text)
        else:
            text_in = regex_dict
            text = []
            if isinstance(text_in, list):
                for i in range(len(text_in)):
                    text.append('( |\n)' + text_in[i] + '(( updated)? \d+/\d+/\d+)?( )?(:|;)')
            else:
                text.append('( |\n)' + text_in + '(( updated)? \d+/\d+/\d+)?( )?(:|;)')
            if no_punctuation_flg:
                if isinstance(text_in, list):
                    for i in range(len(text_in)):
                        text_in_upper = text_in[i].upper()
                        text_in_upper = \
                            self.lambda_manager.lambda_conversion('\(\?I\)', text_in_upper, '(?i)')
                        text.append('(?<!<<<)' + text_in_upper)
                else:
                    text_in_upper = text_in.upper()
                    text_in_upper = \
                        self.lambda_manager.lambda_conversion('\(\?I\)', text_in_upper, '(?i)')
                    text.append('(?<!<<<)' + text_in_upper)
            text_list.append(text)
        return text_list
    '''
    
    #
    def _post_punct(self):
        return('(:|\.|\n)')
        
    #
    def _pre_punct(self):
        return('(^|\n| )')
    
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
        
        '''
        regex_dict = {}
        regex_list = []
        regex_list.append(self._pre_punct() + '(' + article() + ' )?([a-z]+ )?' + \
                         amend() + ' comment' + s() + self._post_punct())
        regex_list.append(self._pre_punct() + amend() + ' comment' + s() + self._post_punct())
        regex_list.append(self._pre_punct() + amend() + ' comment' + s() + ' (\([^\)]*\))?' + self._post_punct())
        regex_list.append('(?i)(?<!see )' + amend() + ' comment' + s() + ' #\d' + self._post_punct())
        regex_list.append('(?i)(?<!see )' + amend() + ' note' + s() + self._post_punct())
        self.section_header_amendment_dict['AMENDMENT COMMENT'] = regex_list
        '''
    
    #
    def _section_header_dict(self):
        self.section_header_dict = {}
        regex_dict = {}
        regex_list = []
        regex_list.append('allergies')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['ALLERGIES'] = regex_dict
        
        '''
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
        regex_dict['ADD PRE_PUNCT'] = regex_list
        self.section_header_dict['AMENDMENT'] = regex_dict
        '''
        
        regex_dict = {}
        regex_list = []
        regex_list.append(self._pre_punct() + '(' + article() + ' )?([a-z]+ )?' + \
                         amend() + ' comment' + s() + self._post_punct())
        regex_list.append(self._pre_punct() + amend() + ' comment' + s() + self._post_punct())
        regex_list.append(self._pre_punct() + amend() + ' comment' + s() + ' (\([^\)]*\))?' + self._post_punct())
        regex_list.append('(?i)(?<!see )' + amend() + ' comment' + s() + ' #\d' + self._post_punct())
        regex_list.append('(?i)(?<!see )' + amend() + ' note' + s() + self._post_punct())
        regex_dict['ADD PRE_PUNCT'] = regex_list
        self.section_header_dict['AMENDMENT COMMENT'] = regex_dict

        regex_dict = {}
        regex_list = []
        regex_list.append('(?i)' + article() + ' following antibodies were used')
        regex_list.append('(?i)using ' + article() + ' following antibody combination')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        regex_dict = {}
        regex_list = []
        regex_list.append('anti(bodie|gen)s tested(?= CD)?')
        regex_list.append('(?i)please see below for (' + article() + ' list of )?antibodies tested' + self._post_punct() + '(?=CD)')
        regex_dict['ADD PRE_PUNCT'] = regex_list
        self.section_header_dict['ANTIBODIES TESTED'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('((impression and|nutrition) )?assessment')
        regex_list.append('(nutrition )?assessment(/| and )plan')
        regex_list.append('findings')
        regex_list.append('plan of care')
        regex_list.append('((activity|current therapy treatment)? )?plan')
        regex_list.append('treatment')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['ASSESSMENT'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('(background (and )?)?(information|method)' + s())
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['BACKGROUND'] = regex_dict
        
        '''
        regex_dict = {}
        regex_list = []
        regex_list.append('er, pr and her-2/neu immunohistochemical stains by computer assisted quantitative image analysis')
        regex_list.append('er, pr and her-2/neu tests')
        regex_list.append('er and pr tests')
        regex_list.append('Her-2/neu ISH\n')
        regex_dict['NEITHER'] = regex_list
        self.section_header_dict['BIOMARKERS TESTS'] = regex_dict
        '''
        
        regex_dict = {}
        regex_list = []
        regex_list.append('bone marrow aspirate( smear(' + s() + ')?)?')
        regex_list.append('bone marrow (aspirate and )?touch prep(aration' + s() + ')?')
        regex_list.append('(bilateral )?bone marrow aspirate' + s() + '(, (left|right) and (left|right))?')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['BONE MARROW ASPIRATE'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('bone marrow (core )?(biopsy(/| and ))?clot section')
        regex_list.append('(bilateral )?bone marrow (biopsies|biopsy cores) and clot section' + \
                          s() + '(, (left|right) and (left|right))?')
        regex_list.append('bone marrow (core )?biopsy')
        regex_list.append('clot section')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['BONE MARROW CLOT SECTION'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('(' + article() + ' )?(bone marrow( aspirate)?|manual) differential(( count)? (\(.+\) )?includes)?[\n\s]*')
        regex_list.append(article() + ' differential count [ A-Za-z]+ includes[\n\s]*')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['BONE MARROW DIFFERENTIAL'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('cytogenetic analysis summary')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['CYTOGENETIC ANALYSIS SUMMARY'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('cytochemical stain' + s())
        regex_list.append('cytogenetic and fish studies')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['CYTOGENETIC AND FISH STUDIES'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('(?i)(?<!(.. no| quit|start|.. to) )' + datetime() + '( of (' + diagnosis() + '|' + datetime(mode_flg='modifier') + '))?(:|;) PHI_DATE')
        regex_list.append('(?i)(?<!(.. no| quit|start|.. to) )' + datetime() + '( of (' + diagnosis() + '|' + datetime(mode_flg='modifier') + '))?(:|;)')
        regex_list.append('(?i)start of care(:|;) PHI_DATE')
        regex_list.append('(?i)start of care(:|;)')
        regex_dict['UNCHANGED'] = regex_list
        self.section_header_dict['DATETIME'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('dx/rx')
        regex_list.append('(referred for )?' + diagnosis())
        regex_list.append('intraoperative consult \(frozen section\) diagnosis')
        regex_list.append('frozen section diagnosis')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['DIAGNOSIS'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('(radiographic )?evaluation')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['EVALUATION'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('explanation of interpretation')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['EXPLANATION'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('((brief|past) )?' + '(family history|FH)')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['FAMILY HISTORY'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('(interphase )?fish analysis summary')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['FISH ANALYSIS SUMMARY'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('flow cytometr(ic (immunologic)?analysis|y)')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['FLOW CYTOMETRIC ANALYSIS'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('goals')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['GOALS'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('hospital course')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['HOSPITAL COURSE'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('(' + diagnosis() + '/)?icd-9')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['ICD-9'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('(microscopic description/)?immunohistochemi(cal stain' + s() + '|stry)')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['IMMUNOHISTOCHEMICAL STAINS'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('immunologic analysis')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['IMMUNOLOGIC ANALYSIS'] = regex_dict
        regex_dict = {}
        text_list = []
        regex_list.append('discharge recommendation' + s())
        regex_list.append('impression' + s() + ' and recommendation' + s())
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['IMPRESSION AND RECOMMENDATION'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('insurance')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['INSURANCE'] = regex_dict
        
        '''
        regex_dict = {}
        regex_list = []
        regex_list.append('interpretation')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['INTERPRETATION'] = regex_dict
        '''
        
        regex_dict = {}
        regex_list = []
        regex_list.append('(therapeutic )?exercise')
        regex_list.append('current therapy')
        regex_list.append('(description of )?(intervention|procedure)' + s())
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['INTERVENTION'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('karyotype' + s())
        regex_list.append('karyotype result' + s())
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['KARYOTYPE'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('cbc')
        regex_list.append('laboratory data([ \-]+CBC)?([ \-]+\d\d?/\d\d?/\d\d\d\d)?')
        regex_list.append('(nutrition related )?labs to\n\nnote')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['LAB DATA'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append(medication() + ' and lab(oratory)? tests')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['LAB DATA AND MEDICATION'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('materials received' + s())
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['MATERIALS RECEIVED'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('(current )?' + medication())
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['MEDICATION'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('method' + s())
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['METHOD'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('molecular studies')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['MOLECULAR STUDIES'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('anthropometrics')
        regex_list.append('(brief )?(physical )?exam')
        regex_list.append('(last )?vitals( seated pre-treatment)?')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['OBJECTIVE'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('modules accepted')
        regex_list.append('read back done')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['OTHER'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('(?i)(?<!SUMMARY\n)\n(' + article() + ' )?peripheral blood (differential count includes|morphology|smear)')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['PERIPHERAL BLOOD MORPHOLOGY'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('pre( |-)' + amend() + ' (final )?(pathologic(al)? )?diagnosis')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['PREAMENDMENT DIAGNOSIS'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('((chief|main) complaint| cc)')
        regex_list.append('problem')
        regex_list.append('reason for (admission|(requested )?consultation|referral|(office )?visit)')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['REASON'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('reference' + s())
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['REFERENCES'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('service')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['SERVICE'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('special stain' + s())
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['SPECIAL STAINS'] = regex_dict
        regex_dict = {}
        regex_list = []
        base = '(impression|subjective|symptom)' + s()
        modifier = '(current)'
        term = '(' + modifier + ' )?' + base
        regex_list.append(term)
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['SUBJECTIVE'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('surgical pathology summary')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['SURGICAL PATHOLOGY SUMMARY'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('synopsis')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['SYNOPSIS'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('technique')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['TECHNIQUE'] = regex_dict
        regex_dict = {}
        regex_list = []
        regex_list.append('24( hour|( )?h(r)?) events')
        regex_dict['ADD PRE_PUNCT AND POST_PUNCT'] = regex_list
        self.section_header_dict['TWENTY-FOUR HOUR EVENTS'] = regex_dict
        
    #
    def get_amendment_text_list(self, section_header):
        regex_list = self.section_header_amendment_dict[section_header]
        text_list = regex_list
        return text_list
        
    #
    def get_text_list(self, section_header, mode_flg):
        regex_list = self.section_header_dict[section_header]
        if mode_flg == 'formatted':
            no_punctuation_flg = False
        elif mode_flg == 'unformatted':
            no_punctuation_flg = True
        else:
            no_punctuation_flg = False
        text_list = self._add_punctuation_formatted(regex_list)
        if mode_flg == 'formatted':
            text_list = self._add_punctuation_formatted(regex_list)
        elif mode_flg == 'unformatted':
            text_list = self._add_punctuation_formatted(regex_list)
            #text_list = self._add_punctuation_unformatted(regex_list, 
            #                                              no_punctuation_flg)
        else:
            text_list = regex_list
        return text_list, no_punctuation_flg
        
    #
    def get_section_header_list(self):
        section_header_list = list(self.section_header_dict.keys())
        section_header_list.sort(key=len, reverse=True)
        return section_header_list
    
    '''
    #
    def person_section_header(self, mode_flg):
        regex_list = []
        if mode_flg == 'formatted':
            regex_list.append('discussed with[^ \d]')
            regex_list.append(review_item() + ' (' + amend() + '|' + clinician_reviewed() + ') by')
            regex_list.append(amend() + ' ' + clinician_reviewed() + ' by')
            regex_list.append('(frozen section diagnosis|intraoperative consult(ation)? diagnosis) ' + \
                             clinician_reviewed() + ' by')
            regex_list.append(clinician_reviewed() + ' by[^ \d]?')
        elif mode_flg == 'unformatted':
            regex_list.append(patient())
            regex_list.append('name of ' + clinician() + '/clinical support person notified')
            regex_list.append(patient() + ' (identification|name)')
            regex_list.append('(addended|performed|referred|requested) by')
            regex_list.append(clinician())
            regex_list.append('(primary care ' + clinician() + '|pcp)')
        self._normalize_section_header(mode_flg, regex_list, 'PERSON')
    '''