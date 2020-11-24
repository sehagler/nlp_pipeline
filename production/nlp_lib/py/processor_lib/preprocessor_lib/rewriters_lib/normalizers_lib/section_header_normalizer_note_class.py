# -*- coding: utf-8 -*-
"""
Created on Mon May 11 17:32:51 2020

@author: haglers
"""

#
from nlp_lib.py.base_class_lib.section_header_normalizer_base_class \
    import Section_header_normalizer_base
from nlp_lib.py.tool_lib.processing_tools_lib.text_processing_tools \
    import datetime, diagnosis, medication, s

#
class Section_header_normalizer_note(Section_header_normalizer_base):
    
    #
    def allergies_section_header(self, mode_flg):
        text_list = []
        text_list.append('allergies')
        self._normalize_section_header(mode_flg, text_list, 'ALLERGIES', no_punctuation_flg=True)
        
    #
    def assessment_section_header(self, mode_flg):
        text_list = []
        text_list.append('((impression and|nutrition) )?assessment')
        text_list.append('(nutrition )?assessment(/| and )plan')
        text_list.append('findings')
        text_list.append('plan of care')
        text_list.append('((activity|current therapy treatment)? )?plan')
        text_list.append('treatment')
        self._normalize_section_header(mode_flg, text_list, 'ASSESSMENT', no_punctuation_flg=True)

    #
    def datetime_section_header(self, mode_flg):
        text_list = []
        text_list.append('(?i)(?<!(.. no| quit|start|.. to) )' + datetime() + '( of (' + diagnosis() + '|' + datetime(mode_flg='modifier') + '))?(:|;) PHI_DATE')
        text_list.append('(?i)start of care(:|;) PHI_DATE')
        self._general_command(text_list, self._tagged_section_header('DATETIME'), True)
        text_list = []
        text_list.append('(?i)(?<!(.. no| quit|start|.. to) )' + datetime() + '( of (' + diagnosis() + '|' + datetime(mode_flg='modifier') + '))?(:|;)')
        text_list.append('(?i)start of care(:|;)')
        self._general_command(text_list, self._tagged_section_header('DATETIME'), True)
        
    #
    def diagnosis_section_header(self, mode_flg):
        text_list = []
        text_list.append('dx/rx')
        self._normalize_section_header(mode_flg, text_list, 'DIAGNOSIS')
        text_list = []
        text_list.append('(referred for )?' + diagnosis())
        self._normalize_section_header(mode_flg, text_list, 'DIAGNOSIS', no_punctuation_flg=True)
        
    #
    def evaluation_section_header(self, mode_flg):
        text_list = []
        text_list.append('(radiographic )?evaluation')
        self._normalize_section_header(mode_flg, text_list, 'EVALUATION', no_punctuation_flg=True)
    
    #
    def goals_section_header(self, mode_flg):
        text_list = []
        text_list.append('goals')
        self._normalize_section_header(mode_flg, text_list, 'GOALS', no_punctuation_flg=True)
        
    #
    def hospital_course_section_header(self, mode_flg):
        text_list = []
        text_list.append('hospital course')
        self._normalize_section_header(mode_flg, text_list, 'HOSPITAL COURSE', no_punctuation_flg=True)
        
    #
    def icd9_section_header(self, mode_flg):
        text_list = []
        text_list.append('(' + diagnosis() + '/)?icd-9')
        self._normalize_section_header(mode_flg, text_list, 'ICD-9', no_punctuation_flg=True)
        
    #
    def insurance_section_header(self, mode_flg):
        text_list = []
        text_list.append('insurance')
        self._normalize_section_header(mode_flg, text_list, 'INSURANCE',
                                       no_punctuation_flg=True)
        
    #
    def intervention_section_header(self, mode_flg):
        text_list = []
        text_list.append('(therapeutic )?exercise')
        text_list.append('current therapy')
        text_list.append('(description of )?(intervention|procedure)' + s())
        self._normalize_section_header(mode_flg, text_list, 'INTERVENTION',
                                       no_punctuation_flg=True)
    
    #
    def lab_test_and_medication_section_header(self, mode_flg):
        text_list = []
        text_list.append(medication() + ' and lab(oratory)? tests')
        self._normalize_section_header(mode_flg, text_list, 'LAB TEST AND MEDICATION', no_punctuation_flg=True)
        text_list = []
        text_list.append('(nutrition related )?labs to\n\nnote')
        self._normalize_section_header(mode_flg, text_list, 'LAB TEST', no_punctuation_flg=True)
        text_list = []
        text_list.append('(current )?' + medication())
        self._normalize_section_header(mode_flg, text_list, 'MEDICATION')
        
    #
    def objective_section_header(self, mode_flg):
        text_list = []
        text_list.append('anthropometrics')
        text_list.append('(brief )?(physical )?exam')
        text_list.append('(last )?vitals( seated pre-treatment)?')
        self._normalize_section_header(mode_flg, text_list, 'OBJECTIVE', no_punctuation_flg=True)
        
    #
    def other_section_header(self, mode_flg):
        text_list = []
        text_list.append('modules accepted')
        text_list.append('read back done')
        self._normalize_section_header(mode_flg, text_list, 'OTHER', no_punctuation_flg=True)
    
    #
    def reason_section_header(self, mode_flg):
        text_list = []
        text_list.append('((chief|main) complaint| cc)')
        text_list.append('problem')
        text_list.append('reason for (admission|(requested )?consultation|referral|(office )?visit)')
        self._normalize_section_header(mode_flg, text_list, 'REASON', no_punctuation_flg=True)
        
    #
    def service_section_header(self, mode_flg):
        text_list = []
        text_list.append('service')
        self._normalize_section_header(mode_flg, text_list, 'SERVICE')
        
    #
    def subjective_section_header(self, mode_flg):
        text_list = []
        base = '(impression|subjective|symptom)' + s()
        modifier = '(current)'
        term = '(' + modifier + ' )?' + base
        text_list.append(term)
        self._normalize_section_header(mode_flg, text_list, 'SUBJECTIVE', no_punctuation_flg=True)
        
    #
    def technique_section_header(self, mode_flg):
        text_list = []
        text_list.append('technique')
        self._normalize_section_header(mode_flg, text_list, 'TECHNIQUE', no_punctuation_flg=True)
        
    #
    def twenty_four_hour_events_section_header(self, mode_flg):
        text_list = []
        text_list.append('24( hour|( )?h(r)?) events')
        self._normalize_section_header(mode_flg, text_list, 'TWENTY-FOUR HOUR EVENTS', no_punctuation_flg=True)