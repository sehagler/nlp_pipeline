# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 10:49:48 2021

@author: haglers
"""

#
from tool_lib.py.processing_tools_lib.text_processing_tools \
    import amend, article, be, datetime, diagnosis, medication, review_item, s

#
class Section_header_structure_tools(object):
    
    #
    def _post_punct(self):
        return('(:|\.|\n)([\n\s]*|$)')
        
    #
    def _pre_punct(self):
        return('(?i)(^|\n)')
    
    #
    def _section_header_dict(self):
        section_header_dict = {}
        regex_list = []
        regex_list.append('allergies')
        section_header_dict['ALLERGIES'] = regex_list
        regex_list = []
        regex_list.append('(?i)\n' + article() + ' ([a-z]+ )?' + amend() + \
                          ' ' +  '(' + be() + '|reports)')
        regex_list.append('(?i)\n' + article() + ' ' + review_item() + \
                         ' ' + be() + ' (additionally|further|re)?( )?' + amend())
        regex_list.append('(?i)\n(' + article() + ' )?([a-z]+ )?' + \
                         amend() + '( ' + review_item() + ')?(' + self._post_punct() + '|\n)')
        regex_list.append('(?i)(' + article() + ' )?' + amend() + '( ' + \
                          review_item() + ')?\s?#\d' + self._post_punct())
        section_header_dict['AMENDMENT'] = regex_list
        regex_list = []
        regex_list.append(self._pre_punct() + '(' + article() + ' )?([a-z]+ )?' + \
                         amend() + ' comment' + s() + self._post_punct())
        regex_list.append(self._pre_punct() + amend() + ' comment' + s() + self._post_punct())
        regex_list.append(self._pre_punct() + amend() + ' comment' + s() + ' (\([^\)]*\))?' + self._post_punct())
        regex_list.append('(?i)(?<!see )' + amend() + ' comment' + s() + ' #\d' + self._post_punct())
        regex_list.append('(?i)(?<!see )' + amend() + ' note' + s() + self._post_punct())
        section_header_dict['AMENDMENT COMMENT'] = regex_list
        regex_list = []
        regex_list.append(self._pre_punct() + 'anti(bodie|gen)s tested' + self._post_punct())
        regex_list.append('(?i)' + article() + ' following antibodies were used' + self._post_punct())
        regex_list.append('(?i)using ' + article() + ' following antibody combination' + self._post_punct())
        regex_list.append('(?i)please see below for (' + article() + ' list of )?antibodies tested' + self._post_punct() + '(?=CD)')
        section_header_dict['ANTIBODIES TESTED'] = regex_list
        regex_list = []
        regex_list.append('((impression and|nutrition) )?assessment')
        regex_list.append('(nutrition )?assessment(/| and )plan')
        regex_list.append('findings')
        regex_list.append('plan of care')
        regex_list.append('((activity|current therapy treatment)? )?plan')
        regex_list.append('treatment')
        section_header_dict['ASSESSMENT'] = regex_list
        regex_list = []
        regex_list.append('(background (and )?)?(information|method)' + s())
        section_header_dict['BACKGROUND'] = regex_list
        regex_list = []
        regex_list.append(self._pre_punct() + 'bone marrow aspirate( smear' + s() + ')?' + self._post_punct())
        regex_list.append(self._pre_punct() + 'bone marrow (aspirate and )?touch prep(aration' + s() + ')?' + self._post_punct())
        regex_list.append(self._pre_punct() + '(bilateral )?bone marrow aspirate' + s() + '(, (left|right) and (left|right))?' + self._post_punct())
        section_header_dict['BONE MARROW ASPIRATE SMEARS'] = regex_list
        regex_list = []
        regex_list.append(self._pre_punct() + 'bone marrow (core )?(biopsy(/| and ))?clot section' + self._post_punct())
        regex_list.append(self._pre_punct() + '(bilateral )?bone marrow (biopsies|biopsy cores) and clot section' + \
                         s() + '(, (left|right) and (left|right))?' + self._post_punct())
        regex_list.append(self._pre_punct() + 'bone marrow (core )?biopsy' + self._post_punct())
        regex_list.append(self._pre_punct() + 'clot section' + self._post_punct())
        section_header_dict['BONE MARROW CLOT SECTION'] = regex_list
        regex_list = []
        regex_list.append(self._pre_punct() + '(' + article() + ' )?(bone marrow( aspirate)?|manual) differential(( count)? (\(.+\) )?includes)?[\n\s]*' + self._post_punct())
        regex_list.append(self._pre_punct() + article() + ' differential count [ A-Za-z]+ includes[\n\s]*' + self._post_punct())
        section_header_dict['BONE MARROW DIFFERENTIAL'] = regex_list
        regex_list = []
        regex_list.append('cytogenetic analysis summary')
        section_header_dict['CYTOGENETIC ANALYSIS SUMMARY'] = regex_list
        regex_list = []
        regex_list.append('cytochemical stain' + s())
        regex_list.append('cytogenetic and fish studies')
        section_header_dict['CYTOGENETIC AND FISH STUDIES'] = regex_list
        regex_list = []
        regex_list.append('(?i)(?<!(.. no| quit|start|.. to) )' + datetime() + '( of (' + diagnosis() + '|' + datetime(mode_flg='modifier') + '))?(:|;) PHI_DATE')
        regex_list.append('(?i)(?<!(.. no| quit|start|.. to) )' + datetime() + '( of (' + diagnosis() + '|' + datetime(mode_flg='modifier') + '))?(:|;)')
        regex_list.append('(?i)start of care(:|;) PHI_DATE')
        regex_list.append('(?i)start of care(:|;)')
        section_header_dict['DATETIME'] = regex_list
        regex_list = []
        regex_list.append('dx/rx')
        regex_list.append('(referred for )?' + diagnosis())
        regex_list.append('intraoperative consult \(frozen section\) diagnosis')
        regex_list.append('frozen section diagnosis')
        section_header_dict['DIAGNOSIS'] = regex_list
        regex_list = []
        regex_list.append('(radiographic )?evaluation')
        section_header_dict['EVALUATION'] = regex_list
        regex_list = []
        regex_list.append('explanation of interpretation')
        section_header_dict['EXPLANATION'] = regex_list
        regex_list = []
        regex_list.append('((brief|past) )?' + '(family history|FH)')
        section_header_dict['FAMILY HISTORY'] = regex_list
        regex_list = []
        regex_list.append('(interphase )?fish analysis summary')
        section_header_dict['FISH ANALYSIS SUMMARY'] = regex_list
        regex_list = []
        regex_list.append('flow cytometr(ic (immunologic)?analysis|y)')
        section_header_dict['FLOW CYTOMETRIC ANALYSIS'] = regex_list
        regex_list = []
        regex_list.append('goals')
        section_header_dict['GOALS'] = regex_list
        regex_list = []
        regex_list.append('hospital course')
        section_header_dict['HOSPITAL COURSE'] = regex_list
        regex_list = []
        regex_list.append('(' + diagnosis() + '/)?icd-9')
        section_header_dict['ICD-9'] = regex_list
        regex_list = []
        regex_list.append('(microscopic description/)?immunohistochemi(cal stain' + s() + '|stry)')
        section_header_dict['IMMUNOHISTOCHEMICAL STAINS'] = regex_list
        regex_list = []
        regex_list.append('immunologic analysis')
        section_header_dict['IMMUNOLOGIC ANALYSIS'] = regex_list
        text_list = []
        regex_list.append('discharge recommendation' + s())
        regex_list.append('impression' + s() + ' and recommendation' + s())
        section_header_dict['IMPRESSION AND RECOMMENDATION'] = regex_list
        regex_list = []
        regex_list.append('insurance')
        section_header_dict['INSURANCE'] = regex_list
        regex_list = []
        regex_list.append('interpretation')
        section_header_dict['INTERPRETATION'] = regex_list
        regex_list = []
        regex_list.append('(therapeutic )?exercise')
        regex_list.append('current therapy')
        regex_list.append('(description of )?(intervention|procedure)' + s())
        section_header_dict['INTERVENTION'] = regex_list
        regex_list = []
        regex_list.append('karyotype' + s())
        section_header_dict['KARYOTYPE'] = regex_list
        regex_list = []
        regex_list.append('cbc')
        regex_list.append('laboratory data([ \-]+CBC)?([ \-]+\d\d?/\d\d?/\d\d\d\d)?')
        regex_list.append('(nutrition related )?labs to\n\nnote')
        section_header_dict['LAB DATA'] = regex_list
        regex_list = []
        regex_list.append(medication() + ' and lab(oratory)? tests')
        section_header_dict['LAB DATA AND MEDICATION'] = regex_list
        regex_list = []
        regex_list.append('materials received' + s())
        section_header_dict['MATERIALS RECEIVED'] = regex_list
        regex_list = []
        regex_list.append('(current )?' + medication())
        section_header_dict['MEDICATION'] = regex_list
        regex_list = []
        regex_list.append('method' + s())
        section_header_dict['METHOD'] = regex_list
        regex_list = []
        regex_list.append('molecular studies')
        section_header_dict['MOLECULAR STUDIES'] = regex_list
        regex_list = []
        regex_list.append('anthropometrics')
        regex_list.append('(brief )?(physical )?exam')
        regex_list.append('(last )?vitals( seated pre-treatment)?')
        section_header_dict['OBJECTIVE'] = regex_list
        regex_list = []
        regex_list.append('modules accepted')
        regex_list.append('read back done')
        section_header_dict['OTHER'] = regex_list
        regex_list = []
        regex_list.append('(?i)(?<!SUMMARY\n)\n(' + article() + ' )?peripheral blood (differential count includes|morphology|smear)' + self._post_punct())
        section_header_dict['PERIPHERAL BLOOD MORPHOLOGY'] = regex_list
        regex_list = []
        regex_list.append('pre( |-)' + amend() + ' (final )?(pathologic(al)? )?diagnosis')
        section_header_dict['PREAMENDMENT DIAGNOSIS'] = regex_list
        regex_list = []
        regex_list.append('((chief|main) complaint| cc)')
        regex_list.append('problem')
        regex_list.append('reason for (admission|(requested )?consultation|referral|(office )?visit)')
        section_header_dict['REASON'] = regex_list
        regex_list = []
        regex_list.append('reference' + s())
        section_header_dict['REFERENCES'] = regex_list
        regex_list = []
        regex_list.append('service')
        section_header_dict['SERVICE'] = regex_list
        regex_list = []
        regex_list.append('special stain' + s())
        section_header_dict['SPECIAL STAINS'] = regex_list
        regex_list = []
        base = '(impression|subjective|symptom)' + s()
        modifier = '(current)'
        term = '(' + modifier + ' )?' + base
        regex_list.append(term)
        section_header_dict['SUBJECTIVE'] = regex_list
        regex_list = []
        regex_list.append('surgical pathology summary')
        section_header_dict['SURGICAL PATHOLOGY SUMMARY'] = regex_list
        regex_list = []
        regex_list.append('synopsis')
        section_header_dict['SYNOPSIS'] = regex_list
        regex_list = []
        regex_list.append('technique')
        section_header_dict['TECHNIQUE'] = regex_list
        regex_list = []
        regex_list.append('24( hour|( )?h(r)?) events')
        section_header_dict['TWENTY-FOUR HOUR EVENTS'] = regex_list
        return section_header_dict