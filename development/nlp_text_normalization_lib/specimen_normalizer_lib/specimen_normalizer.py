# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 15:49:43 2020

@author: haglers
"""

#
from lambda_lib.object_lib.lambda_object_class import Lambda_object
                
#
def specimen_normalizer(text):
    lambda_object = Lambda_object()
    text = \
        lambda_object.contextual_lambda_conversion('[ \t][a-z]\.[ \t]', '\.', text, ':')
    text = \
        lambda_object.contextual_lambda_conversion('[ \t][a-z]\.[ \t]', '(?i)[ \t](?=[a-z])', text, '\n\n')
    text = \
        lambda_object.contextual_lambda_conversion('(\n[A-Z]\: +)(?=[A-Za-z])', '\n', text, '\nSPECIMEN ')
    return text