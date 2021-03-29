# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 14:00:26 2019

@author: haglers
"""

#
from datetime import datetime, timedelta
from dateutil.parser import parse
import re

#
from nlp_lib.py.base_class_lib.postprocessor_base_class import Postprocessor_base
from nlp_lib.py.base_class_lib.preprocessor_base_class import Preprocessor_base

#
class Postprocessor(Postprocessor_base):
    
    #
    def __init__(self, project_data, data_file, data_key_map, data_value_map,
                 label):
        Postprocessor_base.__init__(self, project_data, label, data_file,
                                    data_key_map, data_value_map)
        self._get_date()
        
    #
    def _get_date(self):
        for i in range(len(self.data_dict_list)):
            for key in self.data_dict_list[i][self.nlp_data_key]:
                value_list = []
                try:
                    text_list = self.data_dict_list[i][self.nlp_data_key][key][self.label][self.nlp_text_key]
                except:
                    text_list = []
                for text in text_list:
                    text = normalize_month(text)
                    text = re.sub('[A-Za-z]+-?[0-9]+ - [0-9]{4}', '', text)
                    text = re.sub('[,\-\.]', '/', text)
                    text = re.sub('(?<=[0-9]) of (?=[0-9])', ' / ', text)
                    match_str0 = '('
                    match_str0 += '(?<= )[0-9]{1,2} (/ [0-9]{1,2} )?/ [0-9]{2}([0-9]{2})?(?=( |$))'
                    match_str0 += ')'
                    match0 = re.search(match_str0, text)
                    match_str1 = '('
                    match_str1 += '(?i)(?<= )(early )?[0-9]{4}(?=( |$))'
                    match_str1 += ')'
                    match1 = re.search(match_str1, text)
                    if match0 is not None:
                        value_tmp = match0.group(0)
                        value_tmp = re.sub(' \- ', '-', value_tmp)
                        value_tmp = re.sub(' / ', '/', value_tmp)
                        value_list.append(value_tmp)
                    elif match1 is not None:
                        value_tmp = match1.group(0)
                        value_list.append(value_tmp)
                self._append_data(i, key, value_list)
    
#
class Tokenizer(Preprocessor_base):
    
    #
    def process_month(self):
        month_list = [ 'Jan', 'Feb', 'Mar', 'Apr', 'Jun', 'Jul', 'Aug', 'Sep',
                       'Oct', 'Nov', 'Dec' ]
        for month in month_list:  
            self._general_command('(?i)(?<=' + month + ')\.(?= [0-9])', {None : ''})

#
def atomize_date(date_str):
    month = None
    day = None
    year = None
    date_str = date_str.replace('early', '')
    date_str = date_str.replace(' ', '')
    if re.search('\-', date_str):
        date_str = date_str.split('-')
    elif re.search('/', date_str):
        date_str = date_str.split('/')
    if len(date_str) == 1:
        year = date_str[0]
    elif len(date_str) == 2:
        month = date_str[0]
        year = date_str[1]
    elif len(date_str) == 3:
        month = date_str[0]
        day = date_str[1]
        year = date_str[2]
    return month, day, year

#
def compare_dates(date0, date1):
    month0, day0, year0 = atomize_date(date0)
    month1, day1, year1 = atomize_date(date0)
    try:
        if len(year0) == 4:
            year0 = year0[2:]
    except:
        pass
    try:
        if len(year1) == 4:
            year1 = year1[2:]
    except:
        pass
    try:
        month0 = str(int(month0))
    except:
        pass
    try:
        day0 = str(int(day0))
    except:
        pass
    try:
        month1 = str(int(month1))
    except:
        pass
    try:
        day1 = str(int(day1))
    except:
        pass
    return_flg = False
    try:
        if ( year0 == year1 ) and ( month0 == month1 ):
            return_flg = True
    except:
        pass
    return return_flg

#
def datetime2matlabdn(dt):
   ord = dt.toordinal()
   mdn = dt + timedelta(days = 366)
   frac = (dt-datetime(dt.year,dt.month,dt.day,0,0,0)).seconds / (24.0 * 60.0 * 60.0)
   return mdn.toordinal() + frac

#
def get_date_difference(date_str0, date_str1):
    d0 = parse(date_str0)
    d1 = parse(date_str1)
    delta = d0 - d1
    return delta.days

#
def normalize_month(text):
    month_dict = { 'Jan(uary)?' : 1,  'Feb(ruary)?' : 2, 'Mar(ch)?' : 3,
                   'Apr(il)?' : 4, 'May' : 5, 'Jun(e)?' : 6, 'Jul(y)?' : 7,
                   'Aug(ust)?' : 8, 'Sep(tember)?' : 9, 'Oct(ober)?' : 10,
                   'Nov(ember)?' : 11, 'Dec(ember)?' : 12 }
    for month in month_dict.keys():
        if re.search('(?i)' + month, text) is not None:
            match = re.search('(?i)' + month, text)
            text = re.sub(match.group(0), str(month_dict[month]), text)
        text = re.sub('(?i)(?<=[0-9]) (?=[0-9])', ' / ', text)
    return text