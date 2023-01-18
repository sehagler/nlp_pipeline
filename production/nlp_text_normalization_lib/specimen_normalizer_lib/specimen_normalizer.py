# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 15:49:43 2020

@author: haglers
"""

#
import lambda_lib.tool_lib.lambda_tools as lambda_tools              

#
def specimen_normalizer(text):
    text = \
        lambda_tools.contextual_lambda_conversion('[ \t][a-z]\.[ \t]', '\.', text, ':')
    text = \
        lambda_tools.contextual_lambda_conversion('[ \t][a-z]\.[ \t]', '(?i)[ \t](?=[a-z])', text, '\n\n')
    text = \
        lambda_tools.contextual_lambda_conversion('(\n[A-Z]\: +)(?=[A-Za-z])', '\n', text, '\nSPECIMEN ')
    return text