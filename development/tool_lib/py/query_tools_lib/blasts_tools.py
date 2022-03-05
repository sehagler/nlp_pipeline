# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 13:49:19 2019

@author: haglers
"""

#
import re
import statistics

#
from nlp_lib.py.base_lib.postprocessor_base_class \
    import Postprocessor_base
from nlp_lib.py.base_lib.preprocessor_base_class \
    import Preprocessor_base
    
#
class Named_entity_recognition(Preprocessor_base):
    
    #
    def run_preprocessor(self):
        self._normalize_whitespace()
        self._general_command('(?i)immunohistochemi(cal|stry)', {None : 'IHC'})

#
class Postprocessor(Postprocessor_base):

    #
    def _extract_data_value(self, text_list):
        blast_values = []
        for item in text_list[0]:
            blast_values.append(item[0])
        value_flg = False
        value_list = []
        for blast_value in blast_values:
            blast_value = re.sub('%', '', blast_value)
            if re.search('((<|>|~) )?[0-9]+(\.[0-9]+)?(-[0-9]+(\.[0-9]+)?)?', blast_value) is not None:
                match = re.search('((<|>|~) )?[0-9]+(\.[0-9]+)?(-[0-9]+(\.[0-9]+)?)?', blast_value)
                value_list.append(match.group(0))
                if re.search('(?i)(blast|cell|involve|WBC)', blast_value):
                    value_flg = True
            elif re.search('(?i)(occasional|no definitive|rare)', blast_value) is not None:
                value_list.append('0')
                if re.search('(?i)(blast|cell|involve|WBC)', blast_value):
                    value_flg = True
            else:
                pass
        if value_flg:
            value_list = self._normalize_value_list(value_list)
        else:
            value_list = []
        return value_list
                    
    #
    def _get_include_approximately_list(self, value_list_out, approximately_list):
        include_approximately_list = []
        if len(approximately_list) > 0:
            for approximately in approximately_list:
                match = re.search('[0-9]+(\.[0-9]+)?', approximately)
                approximately_num = float(match.group(0))
                include_approximately = False
                for value in value_list_out:
                    match = re.search('[0-9]+(\.[0-9]+)?', value)
                    value_num = float(match.group(0))
                    if approximately_num != value_num:
                        include_approximately = True
                if include_approximately:
                    include_approximately_list.append(approximately)
        return include_approximately_list
                    
    #
    def _get_include_greater_than_list(self, value_list_out, greater_than_list):
        include_greater_than_list = []
        if len(greater_than_list) > 0:
            for greater_than in greater_than_list:
                match = re.search('[0-9]+(\.[0-9]+)?', greater_than)
                greater_than_num = float(match.group(0))
                include_greater_than = False
                for value in value_list_out:
                    match = re.search('[0-9]+(\.[0-9]+)?', value)
                    value_num = float(match.group(0))
                    if greater_than_num > value_num:
                        include_greater_than = True
                if include_greater_than:
                    include_greater_than_list.append(greater_than)
        return include_greater_than_list
    
    #
    def _get_include_less_than_list(self, value_list_out, less_than_list):
        include_less_than_list = []
        if len(less_than_list) > 0:
            for less_than in less_than_list:
                match = re.search('[0-9]+(\.[0-9]+)?', less_than)
                less_than_num = float(match.group(0))
                include_less_than = False
                for value in value_list_out:
                    match = re.search('[0-9]+(\.[0-9]+)?', value)
                    value_num = float(match.group(0))
                    if less_than_num < value_num:
                        include_less_than = True
                if include_less_than:
                    include_less_than_list.append(less_than)
        return include_less_than_list
    
    #
    def _get_include_range_list(self, value_list_out, range_list):
        include_range_list = []
        if len(range_list) > 0:
            for range_span in range_list:
                match = re.search('[0-9]+(\.[0-9]+)?(?=-)', range_span)
                lower_bound = float(match.group(0))
                match = re.search('(?<=-)[0-9]+(\.[0-9]+)?', range_span)
                upper_bound = float(match.group(0))
                include_range_span = False
                for value in value_list_out:
                    match = re.search('[0-9]+(\.[0-9]+)?', value)
                    value_num = float(match.group(0))
                    if not (value_num > lower_bound and value_num < upper_bound):
                        include_range_span = True
                if include_range_span:
                    include_range_list.append(range_span)
        return include_range_list
                
    #
    def _normalize_value_list(self, value_list_in):
        value_list_out = []
        value_list_in = list(set(value_list_in))
        for idx in range(len(value_list_in)):
            value_list_in[idx] = re.sub('%', '', value_list_in[idx])
        if len(value_list_in) > 1:
            approximately_list = []
            exact_list = []
            greater_than_list = []
            less_than_list = []
            range_list = []
            for value in value_list_in:
                if re.search('-', value) is not None:
                    if value[:2] == '~ ':
                        range_list.append(value[2:])
                    else:
                        range_list.append(value)
                elif value[:2] == '~ ' and re.search('-', value) is None:
                    approximately_list.append(value)
                elif value[:2] == '> ':
                    greater_than_list.append(value)
                elif value[:2] == '< ':
                    less_than_list.append(value)
                else:
                    exact_list.append(value)
            value_list_out = exact_list
            if len(value_list_out) > 0:
                include_approximately_list = \
                    self._get_include_approximately_list(value_list_out, approximately_list)
                value_list_out.extend(include_approximately_list)
            else:
                value_list_out = approximately_list
            include_greater_than_list = \
                self._get_include_greater_than_list(value_list_out, greater_than_list)
            include_less_than_list = \
                self._get_include_less_than_list(value_list_out, less_than_list)
            include_range_list = \
                self._get_include_range_list(value_list_out, range_list)
            value_list_out.extend(include_greater_than_list)
            value_list_out.extend(include_less_than_list)
            value_list_out.extend(include_range_list)
            if len(value_list_out) == 0:
                value_list_out = value_list_in
        else:
            value_list_out = value_list_in
            for idx in range(len(value_list_out)):
                if value_list_out[idx][:2] == '~ ' and re.search('-', value_list_out[idx]):
                    value_list_out[idx] = value_list_out[idx][2:]
        value_dict_list = []
        for value in value_list_out:
            value_dict = {}
            value_dict['BLAST_PERCENTAGE'] = value
            value_dict_list.append(value_dict)
        return value_dict_list
    
#
class Summarization(Preprocessor_base):
    
    #
    def run_preprocessor(self):
        self._clear_command_list()
        self._general_command('(?i)[\n\s]+by IHC', {None : ''})
        self._general_command('(?i)[\n\s]+by immunostain', {None : ''})
        self._process_command_list()

#
def get_blast_value(blast_value_list):
    for i in range(len(blast_value_list)):
        blast_value_list[i] = re.sub('(?<=(~|>|<))', ' ', blast_value_list[i])
        blast_value_list[i] = re.sub(' +', ' ', blast_value_list[i])
    approximately_list = []
    exact_value_list = []
    less_than_list = []
    greater_than_list = []
    range_list = []
    for blast_value in blast_value_list:
        if blast_value[:2] == '~ ':
            if '-' in blast_value:
                range_list.append(blast_value[2:])
            else:
                approximately_list.append(blast_value[2:])
        elif blast_value[:2] == '< ':
            less_than_list.append(blast_value[2:])
        elif blast_value[:2] == '> ':
            greater_than_list.append(blast_value[2:])
        elif '-' in blast_value:
            range_list.append(blast_value)
        else:
            exact_value_list.append(blast_value)
    approximately_list = list(set(approximately_list))
    exact_value_list = list(set(exact_value_list))
    less_than_list = list(set(less_than_list))
    greater_than_list = list(set(greater_than_list))
    range_list = list(set(range_list))
    if len(less_than_list) > 1:
        for i in range(len(less_than_list)):
            less_than_list[i] = float(less_than_list[i])
        less_than_list = [ str(min(less_than_list)) ]
    if len(greater_than_list) > 1:
        for i in range(len(greater_than_list)):
            greater_than_list[i] = float(greater_than_list[i])
        greater_than_list = [ str(max(greater_than_list)) ]
    for i in range(len(range_list)):
        match = re.search('[0-9]+(?=-)', range_list[i])
        lower_bound = float(match.group(0))
        match = re.search('(?<=-)[0-9]+', range_list[i])
        upper_bound = float(match.group(0))
        range_list[i] = str(statistics.mean([lower_bound, upper_bound]))
    blast_value = []
    blast_value.extend(approximately_list)
    blast_value.extend(exact_value_list)
    blast_value.extend(range_list)
    blast_value = list(set(blast_value))
    if len(blast_value) > 0:
        if len(less_than_list) > 0:
            drop_less_than = True
            for value in blast_value:
                if float(value) > float(less_than_list[0]):
                    drop_less_than = False
            if drop_less_than:
                less_than_list = []
        if len(greater_than_list) > 0:
            drop_greater_than = True
            for value in blast_value:
                if float(value) < float(greater_than_list[0]):
                    drop_less_than = False
            if drop_greater_than:
                greater_than_list = []
    try:
        blast_value.append('< ' + less_than_list[0])
    except:
        pass
    try:
        blast_value.append('> ' + greater_than_list[0])
    except:
        pass
    if len(blast_value) == 1:
        return blast_value[0]
    elif len(blast_value) > 1:
        return 'MANUAL_REVIEW'
    else:
        return None