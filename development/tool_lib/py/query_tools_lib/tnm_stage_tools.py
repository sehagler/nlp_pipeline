# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 14:55:53 2019

@author: haglers
"""

#
import re

#
from nlp_lib.py.base_lib.postprocessor_base_class \
    import Postprocessor_base
from nlp_lib.py.base_lib.preprocessor_base_class \
    import Preprocessor_base

#
class Postprocessor(Postprocessor_base):

    #
    def __init__(self, static_data, data_file):
        Postprocessor_base.__init__(self, static_data, data_file)
  
    #
    def _atomize_tnm_stage(self):
        t_stage_tmplt_1, t_stage_tmplt_2 = t_stage_template()
        n_stage_tmplt = n_stage_template()
        m_stage_tmplt = m_stage_template()
        t_stage_m_str_1 = re.compile(t_stage_tmplt_1)
        t_stage_m_str_2 = re.compile(t_stage_tmplt_2)
        n_stage_m_str = re.compile(n_stage_tmplt)
        m_stage_m_str = re.compile(m_stage_tmplt)
        for i in range(len(self.data_dict_list)):
            for key in self.data_dict_list[i]['DATA'].keys():
                if self.data_key_map['EXTRACTED_TEXT'] in self.data_dict_list[i]['DATA'][key].keys():
                    stage = [ [], [], [] ]
                    for text in self.data_dict_list[i]['DATA'][key][self.data_key_map['EXTRACTED_TEXT']]:
                        for match in t_stage_m_str_1.finditer(text):
                            stage[0] += [match.group(0)]
                        for match in n_stage_m_str.finditer(text):
                            stage[1] += [match.group(0)]
                        for match in m_stage_m_str.finditer(text):
                            stage[2] += [match.group(0)]
                        if len(stage[0]) == 0 and len(stage[1]) > 0:
                            for item in stage[1]:
                                for match in re.finditer(item, text):
                                    tnm_stage_tmp = text[:match.start()]
                                    if tnm_stage_tmp != '':
                                        for match in t_stage_m_str_2.finditer(tnm_stage_tmp):
                                            stage[0] += [match.group(0)]
                        for k in range(3):
                            if len(stage[k]) > 0:
                                if self.data_key_map[str(k)] in self.data_dict_list[i]['DATA'][key].keys():
                                    self.data_dict_list[i]['DATA'][key][self.data_key_map[str(k)]] +=\
                                        stage[k]
                                else:
                                    self.data_dict_list[i]['DATA'][key][self.data_key_map[str(k)]] =\
                                        stage[k]
                                        
    #
    def _remove_commas_from_extracted_text(self):
        for i in range(len(self.data_dict_list)):
            for key in self.data_dict_list[i]['DATA'].keys():
                if self.data_key_map['EXTRACTED_TEXT'] in self.data_dict_list[i]['DATA'][key].keys():
                    for j in range(len(self.data_dict_list[i]['DATA'][key][self.data_key_map['EXTRACTED_TEXT']])):
                        self.data_dict_list[i]['DATA'][key][self.data_key_map['EXTRACTED_TEXT']][j] = \
                            self.data_dict_list[i]['DATA'][key][self.data_key_map['EXTRACTED_TEXT']][j].replace(',', '')

#
class Summarization(Preprocessor_base):
    
    #
    def _process_tnm_staging(self):
        self._clear_command_list()
        text_list = []
        text_list.append('(?i)(pathologic( tumor)?|TNM) stag(e|ing)')
        text_list.append('(?i)stage summary')
        for text_str in text_list:
            self._general_command(text_str, {None : 'Stage'})
        self._process_command_list()
        
    #
    def _remove_extraneous_text(self):
        self._clear_command_list()
        self._general_command('(?i)(\( )?(AJCC )?\d(\d)?th Ed(ition|.)( \))?', {None : ''})
        self._general_command('(?i)(\( )?AJCC( \))?', {None : ''})
        self._process_command_list()
    
    #
    def _remove_tnm_staging(self):
        self._general_command('(?i) \( pTNM \)', {None : ''})
        self._general_command('(?i) \( pT \)', {None : ''})
        self._general_command('(?i) \( pN \)', {None : ''})
        self._general_command('(?i) \( p?M \)', {None : ''})
        
    #
    def run_preprocessor(self):
        self._process_tnm_staging()
        self._remove_extraneous_text()
        self._remove_tnm_staging()

#
def m_stage_template():
    m_stage_prefix = '[AaCcPpRrUuYy]{0,2}'
    m_stage_primary_suffix = '([OoXx0-1]|\(n/a\))'
    m_stage_secondary_suffix = '(\([^\)]+\))?'
    m_stage_tmplt = m_stage_prefix + 'M' + m_stage_primary_suffix + \
                    m_stage_secondary_suffix
    return m_stage_tmplt

#
def n_stage_template():
    n_stage_prefix = '(SN|sn)?[AaCcRrSsUuYy]{0,2}(\((SN|sn)\))?[Pp]?'
    n_stage_primary_suffix = '([OoXx0-4]|\(n/a\))'
    n_stage_secondary_suffix = \
        '(\(?(MI|mi)\)?|[A-Da-d])?[1-4]?([iv]+)?(i(-|\+)?)?(\[^\)]+\))?'
    n_stage_tmplt = n_stage_prefix + 'N' + n_stage_primary_suffix + \
                    n_stage_secondary_suffix
    return n_stage_tmplt

#
def t_stage_template():
    t_stage_prefix = '([AaCcMmRrUuYy]{1,2} ?)?[Pp]?'
    t_stage_primary_suffix = '((IS|is)|(MIC?|mic?)|[Xx0-4]|\(n/a\))'
    t_stage_secondary_suffix = '((MIC?|mic?)|[A-Da-d])?(\([^\)]+\))?'
    t_stage_tmplt_1 = t_stage_prefix + 'T' + t_stage_primary_suffix + \
                      t_stage_secondary_suffix
    t_stage_tmplt_2 = t_stage_prefix + t_stage_primary_suffix + \
                      t_stage_secondary_suffix
    return t_stage_tmplt_1, t_stage_tmplt_2