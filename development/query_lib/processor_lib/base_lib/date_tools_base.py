# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 14:00:26 2019

@author: haglers
"""

#
from datetime import datetime, timedelta
from dateutil.parser import parse
import re
import traceback

#
import lambda_lib.tool_lib.lambda_tools as lambda_tools
from base_lib.postprocessor_base_class \
    import Postprocessor_base
from base_lib.preprocessor_base_class import Preprocessor_base

#
class Postprocessor(Postprocessor_base):
  
    #
    def _extract_data_value(self, value_list_dict):
        extracted_data_dict = {}
        for key in value_list_dict.keys():
            text_list = value_list_dict[key]
            date_text_list = []
            for item in text_list[0]:
                date_text_list.append(item[0])
            value_list = []
            for date_text in date_text_list:
                date_text = normalize_month(date_text)
                date_text = \
                    lambda_tools.lambda_conversion('[A-Za-z]+-?[0-9]+ - [0-9]{4}', date_text, '')
                date_text = \
                    lambda_tools.lambda_conversion('[,\-\.]', date_text, '/')
                date_text = \
                    lambda_tools.lambda_conversion('(?<=[0-9]) of (?=[0-9])', date_text, ' / ')
                match_str0 = '('
                match_str0 += '(?<= )[0-9]{1,2} (/ [0-9]{1,2} )?/ [0-9]{2}([0-9]{2})?(?=( |$))'
                match_str0 += ')'
                match0 = re.search(match_str0, date_text)
                match_str1 = '('
                match_str1 += '(?i)(?<= )(early )?[0-9]{4}(?=( |$))'
                match_str1 += ')'
                match1 = re.search(match_str1, date_text)
                if match0 is not None:
                    value_tmp = match0.group(0)
                    value_tmp = \
                        lambda_tools.lambda_conversion(' \- ', value_tmp, '-')
                    value_tmp = \
                        lambda_tools.lambda_conversion(' / ', value_tmp, '/')
                    value_list.append(value_tmp)
                elif match1 is not None:
                    value_tmp = match1.group(0)
                    value_list.append(value_tmp)
            value_dict_list = []
            for value in value_list:
                value_dict = {}
                value_dict['DATE'] = value
                value_dict_list.append(value_dict)
            extracted_data_dict[key] = value_dict_list
        return extracted_data_dict
    
#
class Tokenizer(Preprocessor_base):
    
    #
    def process_month(self):
        month_list = [ 'Jan', 'Feb', 'Mar', 'Apr', 'Jun', 'Jul', 'Aug', 'Sep',
                       'Oct', 'Nov', 'Dec' ]
        for month in month_list:  
            self.text = \
                lambda_tools.deletion_lambda_conversion('(?i)(?<=' + month + ')\.(?= [0-9])', self.text)

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
    except Exception:
        traceback.print_exc()
    try:
        if len(year1) == 4:
            year1 = year1[2:]
    except Exception:
        traceback.print_exc()
    try:
        month0 = str(int(month0))
    except Exception:
        traceback.print_exc()
    try:
        day0 = str(int(day0))
    except Exception:
        traceback.print_exc()
    try:
        month1 = str(int(month1))
    except Exception:
        traceback.print_exc()
    try:
        day1 = str(int(day1))
    except Exception:
        traceback.print_exc()
    return_flg = False
    try:
        if ( year0 == year1 ) and ( month0 == month1 ):
            return_flg = True
    except Exception:
        traceback.print_exc()
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
            text = \
                lambda_tools.lambda_conversion(match.group(0), text, str(month_dict[month]))
        text = \
            lambda_tools.lambda_conversion('(?i)(?<=[0-9]) (?=[0-9])', text, ' / ')
    return text