# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 14:55:53 2019

@author: haglers
"""

#
import re
import itertools

#
from base_lib.postprocessor_base_class import Postprocessor_base
from base_lib.preprocessor_base_class import Preprocessor_base
import lambda_lib.tool_lib.lambda_tools as lambda_tools
from tools_lib.processing_tools_lib.function_processing_tools \
    import sequential_composition

#
def _create_template_list(prefix_list, base_list, suffix_list):
    template_list = []
    for prefix in prefix_list:
        for base in base_list:
            for suffix in suffix_list:
                template_list.append(prefix + base + suffix)
    return template_list

#
def _normalize_staging(staging):
    if staging is not None:
        staging = lambda_tools.lambda_conversion('[Oo]', staging, '0')
        staging = lambda_tools.lambda_conversion('x', staging, 'X')
        staging = lambda_tools.lambda_conversion('n/a', staging, '(n/a)')
        staging = lambda_tools.lambda_conversion('\(\(', staging, '(')
        staging = lambda_tools.lambda_conversion('\)\)', staging, ')')
    return staging

#
def _permutation_list(elements_list):
    permutations = list(itertools.permutations(elements_list))
    permutation_list = []
    for permutation in permutations:
        permutation_list.append(''.join(permutation))
    return permutation_list

#
def _permutation_string(elements_list):
    permutations = list(itertools.permutations(elements_list))
    permutation_string = '('
    for i in range(len(permutations)):
        permutation_string += ''.join(permutations[i]) + '|'
    permutation_string = permutation_string[0:-1]
    permutation_string += ')?'
    return permutation_string

#
def _process_tnm_staging(text):
    text_list = []
    text_list.append('(?i)(pathologic( tumor)?|TNM) stag(e|ing)')
    text_list.append('(?i)stage summary')
    for text_str in text_list:
        text = lambda_tools.lambda_conversion(text_str, text, 'Stage')
    return text

#
def _remove_extraneous_text(text):
    text = \
        lambda_tools.deletion_lambda_conversion('(?i)(\( )?(AJCC )?\d(\d)?th Ed(ition|.)( \))?', text)
    text = \
        lambda_tools.deletion_lambda_conversion('(?i)(\( )?AJCC( \))?', text)
    return text

#
def m_stage_base():
    m_stage_base_list = [ 'M([OoXx0-1]|( ?\( ?)?n ?/ ?a( ?\) ?)?)' ]
    return m_stage_base_list

#
def m_stage_template():
    m_stage_base_list = m_stage_base()
    m_stage_prefix_elements = \
        [ '(( ?(\[|\() ?)?(SN|sn)( ?(\]|\)) ?)? ?)?',
          '(( ?(\[|\() ?)?[AaCcRrUuYy]{1,2}( ?(\]|\)) ?)? ?)?',
          '(( ?(\[|\() ?)?[Pp]( ?(\]|\)) ?)? ?)?' ]
    m_stage_prefix_list = _permutation_list(m_stage_prefix_elements)
    m_stage_prefix_string = _permutation_string(m_stage_prefix_elements)
    m_stage_suffix_list = [ '' ]
    m_stage_tmplt_1_list = _create_template_list([ m_stage_prefix_string ],
                                                 m_stage_base_list,
                                                 m_stage_suffix_list)
    m_stage_tmplt_2_list = _create_template_list(m_stage_prefix_list,
                                                 m_stage_base_list,
                                                 m_stage_suffix_list)
    return m_stage_tmplt_1_list, m_stage_tmplt_2_list

#
def n_stage_base():
    n_stage_base_1_list = \
        [ 'N([OoXx0-4]([A-Da-d]( ?[1-4])?( ?[iv]+)?)?|( ?\( ?)?n ?/ ?a( ?\) ?)?)' ]
    n_stage_base_2_list = \
        [ 'N([Xx0-4]([A-Da-d]( ?[1-4])?( ?[iv]+)?)?|( ?\( ?)?n ?/ ?a( ?\) ?)?)' ]
    n_stage_base_3_list = \
        [ 'pN([Xx0-4]([A-Da-d]( ?[1-4])?( ?[iv]+)?)?|( ?\( ?)?n ?/ ?a( ?\) ?)?)' ]
    return n_stage_base_1_list, n_stage_base_2_list, n_stage_base_3_list

#
def n_stage_template():
    n_stage_base_1_list = \
        [ 'N([OoXx0-4]([A-Da-d][1-4]?([iv]+)?)?|( ?\( ?)?n ?/ ?a( ?\) ?)?)' ]
    n_stage_base_2_list = \
        [ 'N([Xx0-4]([A-Da-d][1-4]?([iv]+)?)?|( ?\( ?)?n ?/ ?a( ?\) ?)?)' ]
    n_stage_base_3_list = \
        [ 'pN([Xx0-4]([A-Da-d][1-4]?([iv]+)?)?|( ?\( ?)?n ?/ ?a( ?\) ?)?)' ]
    n_stage_base_1_list, n_stage_base_2_list, n_stage_base_3_list = \
        n_stage_base()
    n_stage_prefix_elements = \
        [ '(( ?(\[|\() ?)?[AaCcRrSsUuYy]{1,2}( ?(\]|\)) ?)? ?)?',
          '(( ?(\[|\() ?)?[Pp]( ?(\]|\)) ?)? ?)?',
          '(( ?(\[|\() ?)?(SN|sn)( ?(\]|\)) ?)? ?)?' ]
    n_stage_prefix_list = _permutation_list(n_stage_prefix_elements)
    n_stage_prefix_string = _permutation_string(n_stage_prefix_elements)
    n_stage_suffix_elements = \
        [ '(( ?(\[|\() ?)?(MIC?|mic?)( ?(\]|\)) ?)? ?)?', 
          '(( ?(\[|\() ?)?(SN|sn)( ?(\]|\)) ?)? ?)?',
          '(( ?(\[|\() ?)?ih?c?(-|\+)( ?(\]|\)) ?)? ?)?' ]
    n_stage_suffix_list = _permutation_list(n_stage_suffix_elements)
    n_stage_suffix_string = _permutation_string(n_stage_suffix_elements)
    n_stage_tmplt_1_list = _create_template_list([ n_stage_prefix_string ],
                                                 n_stage_base_1_list,
                                                 n_stage_suffix_list)
    n_stage_tmplt_2_list = _create_template_list([ n_stage_prefix_string ],
                                                 n_stage_base_2_list,
                                                 n_stage_suffix_list)
    n_stage_tmplt_3_list = _create_template_list(n_stage_prefix_list,
                                                 n_stage_base_3_list,
                                                 n_stage_suffix_list)
    return n_stage_tmplt_1_list, n_stage_tmplt_2_list, n_stage_tmplt_3_list

#
def t_stage_base():
    t_stage_base_1_list = \
        [ 'T((IS|is)|(MIC?|mic?)|[OoXx0-4][A-Da-d]?|( ?\( ?)?n ?/ ?a( ?\) ?)?)' ]
    t_stage_base_2_list = \
        [ '((IS|is)|(MIC?|mic?)|[OoXx0-4][A-Da-d]?|( ?\( ?)?n ?/ ?a( ?\) ?)?)' ]
    t_stage_base_3_list = \
        [ 'T((IS|is)|(MIC?|mic?)|[Xx0-4][A-Da-d]|( ?\( ?)?n ?/ ?a( ?\) ?)?)',
          'pT((IS|is)|(MIC?|mic?)|[OoXx0-4][A-Da-d]?|( ?\( ?)?n ?/ ?a( ?\) ?)?)' ]
    return t_stage_base_1_list, t_stage_base_2_list, t_stage_base_3_list

#
def t_stage_template():
    t_stage_base_1_list, t_stage_base_2_list, t_stage_base_3_list = \
        t_stage_base()
    t_stage_prefix_elements = \
        [ '(( ?(\[|\() ?)?[AaCcMmRrUuYy]{1,2}( ?(\]|\)) ?)? ?)?',
          '(( ?(\[|\() ?)?[Pp]( ?(\]|\)) ?)? ?)?' ]
    t_stage_prefix_list = _permutation_list(t_stage_prefix_elements)
    t_stage_prefix_string = _permutation_string(t_stage_prefix_elements)
    t_stage_suffix_elements = \
        [ '(( ?(\[|\() ?)?[Mm]( ?(\]|\)) ?)? ?)?'
          '(( ?(\[|\() ?)?DCIS( ?(\]|\)) ?)? ?)?',
          '(( ?(\[|\() ?)?(MIC?|mic?)( ?(\]|\)) ?)? ?)?' ]
    t_stage_suffix_list = _permutation_list(t_stage_suffix_elements)
    t_stage_suffix_string = _permutation_string(t_stage_suffix_elements)
    t_stage_tmplt_1_list = _create_template_list(t_stage_prefix_list,
                                                 t_stage_base_1_list,
                                                 [ t_stage_suffix_string ])
    t_stage_tmplt_2_list = _create_template_list(t_stage_prefix_list,
                                                 t_stage_base_2_list,
                                                 [ t_stage_suffix_string ])
    t_stage_tmplt_3_list = _create_template_list(t_stage_prefix_list,
                                                 t_stage_base_3_list,
                                                 t_stage_suffix_list)
    return t_stage_tmplt_1_list, t_stage_tmplt_2_list, t_stage_tmplt_3_list

#
def simple_template():
    tmplt_prefix = '(?<![A-Za-z0-9])'
    tmplt_suffix = '(?![A-Za-z0-9])'
    t_stage_tmplt_1_list, t_stage_tmplt_2_list, t_stage_tmplt_3_list = \
        t_stage_template()
    n_stage_tmplt_1_list, n_stage_tmplt_2_list, n_stage_tmplt_3_list = \
        n_stage_template()
    m_stage_tmplt_1_list, m_stage_tmplt_2_list = m_stage_template()
    template_list = []
    for t_stage_tmplt in t_stage_tmplt_1_list:
        for n_stage_tmplt in n_stage_tmplt_1_list:
            for m_stage_tmplt in m_stage_tmplt_1_list:
                template_tmp = \
                    tmplt_prefix + t_stage_tmplt + \
                    ' ?,? ?' + n_stage_tmplt + \
                    '(' + ' ?,? ?' + m_stage_tmplt + ')?' + \
                    tmplt_suffix
                template_list.append(template_tmp)
    for t_stage_tmplt in t_stage_tmplt_2_list:
        for n_stage_tmplt in n_stage_tmplt_2_list:
            for m_stage_tmplt in m_stage_tmplt_1_list:
                template_tmp = \
                    tmplt_prefix + t_stage_tmplt + \
                    ' ?,? ?' + n_stage_tmplt + \
                    '(' + ' ?,? ?' + m_stage_tmplt + ')?' + \
                    tmplt_suffix
                template_list.append(template_tmp)
    for t_stage_tmplt in t_stage_tmplt_3_list:
        template_tmp = tmplt_prefix + t_stage_tmplt + tmplt_suffix
        template_list.append(template_tmp)
    for n_stage_tmplt in n_stage_tmplt_3_list:
        template_tmp = tmplt_prefix + n_stage_tmplt + tmplt_suffix
        template_list.append(template_tmp)
    for m_stage_tmplt in m_stage_tmplt_2_list:
        template_tmp = tmplt_prefix + m_stage_tmplt + tmplt_suffix
        template_list.append(template_tmp)
    sections_list = None
    template_dict = {}
    template_dict['primary_template_list'] = template_list
    template_dict['sections_list'] = sections_list
    template_dict['template_headers'] = [ 'TNM Staging' ]
    return template_dict

#
class Postprocessor(Postprocessor_base):
    
    #
    def _assemble_tnm_from_singletons(self, data_table):
        all_singletons_flg = True
        for data_row in data_table:
            if not self._is_tnm_singleton(data_row[1]):
                all_singletons_flg = False
        if all_singletons_flg:
            key_list = []
            t_stage_singletons_list = []
            n_stage_singletons_list = []
            m_stage_singletons_list = []
            for data_row in data_table:
                t_stage_base_1_list, t_stage_base_2_list, t_stage_base_3_list = \
                    t_stage_base()
                match = re.search(t_stage_base_1_list[0], data_row[1])
                if match:
                    key_list.append(data_row[0])
                    t_stage_singletons_list.append(data_row[1])
                n_stage_base_1_list, n_stage_base_2_list, n_stage_base_3_list = \
                    n_stage_base()
                match = re.search(n_stage_base_1_list[0], data_row[1])
                if match:
                    n_stage_singletons_list.append(data_row[1])
                m_stage_base_list = m_stage_base()
                match = re.search(m_stage_base_list[0], data_row[1])
                if match:
                    m_stage_singletons_list.append(data_row[1])
            if len(t_stage_singletons_list) == 1 and \
               len(n_stage_singletons_list) == 1 and \
               len(m_stage_singletons_list) < 2:
                key = key_list[0]
                tnm_staging = t_stage_singletons_list[0] + \
                              n_stage_singletons_list[0]
                if len(m_stage_singletons_list) == 1:
                    tnm_staging += m_stage_singletons_list[0]
                data_table.append([ key, tnm_staging, '' ])
        return data_table
    
    #
    def _cleanup_data_table(self, data_table):
        for i in range(len(data_table)):
            data_table[i][1] = \
                lambda_tools.lambda_conversion(',', data_table[i][1], '')
            data_table[i][1] = \
                lambda_tools.lambda_conversion(' +', data_table[i][1], '')
        return data_table
                                        
    #
    def _extract_data_value(self, value_list_dict):
        data_table = self._generate_data_table(value_list_dict)
        data_table = self._cleanup_data_table(data_table)
        data_table = self._unique_tnm_staging(data_table)
        data_table = self._trim_tnm_singletons(data_table)
        data_table = self._assemble_tnm_from_singletons(data_table)
        data_table = self._trim_tnm_singletons(data_table)
        data_table = self._unique_tnm_staging(data_table)
        data_table = self._trim_mx_singleton(data_table)
        data_table_keys = self._get_data_table_keys(data_table)
        extracted_data_dict = {}
        for key in data_table_keys:
            data_table_key = self._generate_data_subtable(data_table, key)
            value_dict_list = []
            for i in range(len(data_table_key)):
                tnm_staging_text = data_table_key[i][1]
                snippet_text = data_table_key[i][2]
                value_dict = {}
                value_dict['TNM_STAGING'] = tnm_staging_text
                t_staging = self._extract_t_staging(tnm_staging_text)
                if t_staging is not None:
                    value_dict['T_STAGING'] = t_staging
                n_staging = self._extract_n_staging(tnm_staging_text)
                if n_staging is not None:
                    value_dict['N_STAGING'] = n_staging
                m_staging = self._extract_m_staging(tnm_staging_text)
                if m_staging is not None:
                    value_dict['M_STAGING'] = m_staging
                value_dict['SNIPPET'] = snippet_text
                value_dict_list.append(value_dict)
            extracted_data_dict[key] = value_dict_list
        return extracted_data_dict
    
    #
    def _extract_m_staging(self, tnm_staging_text):
        m_stage_base_list = m_stage_base()
        match = re.search(m_stage_base_list[0], tnm_staging_text)
        if match:
            m_staging = match.group(0)
        else:
            m_staging = None
        if m_staging is not None and bool(re.search('n/a', m_staging)):
            m_staging = None
        m_staging = _normalize_staging(m_staging)
        return m_staging
    
    #
    def _extract_n_staging(self, tnm_staging_text):
        n_stage_base_1_list, n_stage_base_2_list, n_stage_base_3_list = \
            n_stage_base()
        match = re.search(n_stage_base_1_list[0], tnm_staging_text)
        if match:
            n_staging = match.group(0)
        else:
            n_staging = None
        if n_staging is not None and bool(re.search('n/a', n_staging)):
            n_staging = None
        n_staging = _normalize_staging(n_staging)
        return n_staging
        
    #
    def _extract_t_staging(self, tnm_staging_text):
        t_stage_base_1_list, t_stage_base_2_list, t_stage_base_3_list = \
            t_stage_base()
        match = re.search(t_stage_base_1_list[0], tnm_staging_text)
        if match:
            t_staging = match.group(0)
        else:
            t_staging = None
        if t_staging is not None and bool(re.search('n/a', t_staging)):
            t_staging = None
        t_staging = _normalize_staging(t_staging)
        return t_staging
    
    #
    def _extract_tnm_singleton_base(self, tnm_singleton):
        extraction_ctr = 0
        t_stage_base_1_list, t_stage_base_2_list, t_stage_base_3_list = \
            t_stage_base()
        match = re.search(t_stage_base_1_list[0], tnm_singleton)
        if match:
            t_staging = match.group(0)
            extraction_ctr += 1
        else:
            t_staging = None
        n_stage_base_1_list, n_stage_base_2_list, n_stage_base_3_list = \
            n_stage_base()
        match = re.search(n_stage_base_1_list[0], tnm_singleton)
        if match:
            n_staging = match.group(0)
            extraction_ctr += 1
        else:
            n_staging = None
        m_stage_base_list = m_stage_base()
        match = re.search(m_stage_base_list[0], tnm_singleton)
        if match:
            m_staging = match.group(0)
            extraction_ctr += 1
        else:
            m_staging = None
        if extraction_ctr == 1:
            if t_staging is not None:
                singleton_base = t_staging
            elif n_staging is not None:
                singleton_base = n_staging
            elif m_staging is not None:
                singleton_base = m_staging
        else:
             singleton_base = tnm_singleton
        return singleton_base
    
    #
    def _is_tnm_singleton(self, tnm_staging_text):
        t_stage_base_1_list, t_stage_base_2_list, t_stage_base_3_list = \
            t_stage_base()
        t_match = re.search(t_stage_base_1_list[0], tnm_staging_text)
        n_stage_base_1_list, n_stage_base_2_list, n_stage_base_3_list = \
            n_stage_base()
        n_match = re.search(n_stage_base_1_list[0], tnm_staging_text)
        m_stage_base_list = m_stage_base()
        m_match = re.search(m_stage_base_list[0], tnm_staging_text)
        match_ctr = bool(t_match) + bool(n_match) + bool(m_match)
        if match_ctr == 1:
            ret_val = True
        else:
            ret_val = False
        return ret_val
    
    #
    def _trim_mx_singleton(self, data_table):
        delete_idxs = []
        for i in range(len(data_table)):
            if data_table[i][1].lower() == 'mx':
                delete_idxs.append(i)
        delete_idxs = list(set(delete_idxs))
        if len(delete_idxs) > 0:
            delete_idxs = sorted(delete_idxs, reverse=True)
        for i in range(len(delete_idxs)):
            del data_table[delete_idxs[i]]
        return data_table
    
    #
    def _trim_tnm_singletons(self, data_table):
        tnm_singleton_list = []
        for data_row in data_table:
            if self._is_tnm_singleton(data_row[1]):
                tnm_singleton_list.append(data_row[1])
        thm_singleton_list = list(set(tnm_singleton_list))
        delete_idxs = []
        for item0 in tnm_singleton_list:
            delete_singleton_flg = False
            item0_base = self._extract_tnm_singleton_base(item0)
            for data_row in data_table:
                if not self._is_tnm_singleton(data_row[1]):
                    if item0_base.lower() in data_row[1].lower():
                        delete_singleton_flg = True
            if delete_singleton_flg:
                for i in range(len(data_table)):
                    if item0 == data_table[i][1]:
                        delete_idxs.append(i)
        delete_idxs = list(set(delete_idxs))
        if len(delete_idxs) > 0:
            delete_idxs = sorted(delete_idxs, reverse=True)
        for i in range(len(delete_idxs)):
            del data_table[delete_idxs[i]]
        return data_table
    
    #
    def _unique_tnm_staging(self, data_table):
        delete_idxs = []
        for i in range(len(data_table)-1):
            item0 = data_table[i][1]
            for j in range(i+1, len(data_table)):
                item1 = data_table[j][1]
                if item0.lower() == item1.lower():
                    delete_idxs.append(j)
        delete_idxs = list(set(delete_idxs))
        if len(delete_idxs) > 0:
            delete_idxs = sorted(delete_idxs, reverse=True)
        for i in range(len(delete_idxs)):
            del data_table[delete_idxs[i]]
        return data_table

#
class Preprocessor(Preprocessor_base):
    
    #
    def run_preprocessor(self):
        normalize_text = sequential_composition(_remove_extraneous_text,
                                            _process_tnm_staging)
        self.text = normalize_text(self.text)