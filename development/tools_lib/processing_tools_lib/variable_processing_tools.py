# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 15:25:14 2020

@author: haglers
"""

#
import traceback

#
def delete_key(dictionary, key):
    if key in dictionary.keys():
        del dictionary[key]
    
#
def nlp_to_tuple(value):
    if value is not None:
        value = list(value)
        for i in range(len(value)):
            value[i] = value[i].replace(' ', '')
        value_tuple = tuple(value)
    else:
        value_tuple = None
    return value_tuple

#
def trim_data_value(data_value):
    data_value_tmp = data_value
    data_value = []
    for item in data_value_tmp:
        data_value.extend(item)
    try:
        data_value = list(set(data_value))
    except Exception:
        pass
        #traceback.print_exc()
    return data_value

#
def validation_to_tuple(text):
    if text is not None:
        text = text.replace(' ', '')
        text = text.replace(',', '\',\'')
        text = text.replace('(', '(\'')
        text = text.replace(')', '\')')
        text = text.replace('\'(', '(')
        text = text.replace(')\'', ')')
        try:
            text_eval = '[\'' + text + '\']'
            text_list = eval(text_eval)
        except Exception:
            traceback.print_exc()
            text = text.replace('(\'', '(')
            text = text.replace('\')', ')')
            text_eval = '[\'' + text + '\']'
            text_list = eval(text_eval)
        for i in range(len(text_list)):
            if isinstance(text_list[i], tuple):
                text_list[i] = str(text_list[i])
                text_list[i] = text_list[i].replace('\'', '')
                text_list[i] = text_list[i].replace(' ', '')
        text_tuple = tuple(text_list)
    else:
        text_tuple = None
    return text_tuple