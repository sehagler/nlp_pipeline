# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 13:28:29 2020

@author: haglers
"""

#
import lambda_lib.object_lib.lambda_object_class as lambda_lib
from tools_lib.processing_tools_lib.function_processing_tools \
    import composite_function

#
def _deidentify_age(text):
    text = \
        lambda_lib.lambda_conversion('[0-9]+( - | )?y/o', text, 'PHI_AGE')
    return text

#
def _deidentify_gender(text):
    text = \
        lambda_lib.contextual_lambda_conversion('(\n| )(fe)?male(\n|\.| )', '(fe)?male', text, 'PHI_GENDER')
    text = \
        lambda_lib.contextual_lambda_conversion('(\n| )(wo)?man(\n|\.| )', '(wo)?man', text, 'PHI_GENDER')
    text = \
        lambda_lib.contextual_lambda_conversion('(\n| )boy(\n|\.| )', 'boy', text, 'PHI_GENDER')
    text = \
        lambda_lib.contextual_lambda_conversion('(\n| )girl(\n|\.| )', 'girl', text, 'PHI_GENDER')
    return text

#
def _deidentify_mrn(text):
    text = \
        lambda_lib.contextual_lambda_conversion('mrn: \d{8} ', '\d{8}', text, 'PHI_MRN')
    return text
        
#
def _deidentify_personal_name(text):
    '''
    text = \
        lambda_lib.contextual_lambda_conversion('[A-Za-z]+ [A-Z]\. [A-Za-z]+, M(\.)?D(\.)?',
                                                         ' [A-Z]\.(?!D)', text, '')
    '''
    return text
        
#
def _deidentify_pronouns(text):
    text = \
        lambda_lib.contextual_lambda_conversion('(\n| )h(er|im|is)(\n|\.| )', 'h(er|im|is)', text, 'PHI_HER_HIM_HIS')
    text = \
        lambda_lib.contextual_lambda_conversion('(\n| )(s)?he(\n|\.| )', '(s)?he', text, 'PHI_HE_SHE')
    return text
    
#
def _deidentify_telephone_number(text):
    text = \
        lambda_lib.contextual_lambda_conversion('\(\d{3}\) \d{3}-\d{4}', '\(\d{3}\) \d{3}-\d{4}', text, 'PHI_TELEPHONE_NUMBER')
    text = \
        lambda_lib.contextual_lambda_conversion('\d{3} \d{3} \d{4}', '\d{3} \d{3} \d{4}', text, 'PHI_TELEPHONE_NUMBER')
    return text
    
#
def deidentifier(text):
    deidentify_text = composite_function(_deidentify_telephone_number,
                                         _deidentify_pronouns,
                                         _deidentify_personal_name,
                                         _deidentify_mrn,
                                         _deidentify_gender,
                                         _deidentify_age)
    text = deidentify_text(text)
    return text

#
def deidentify_date(text):
    text = \
        lambda_lib.lambda_conversion('[0-9]{1,2}/[0-9]{1,2}/(19|20)[0-9]{2}', text, 'PHI_DATE')
    text = \
        lambda_lib.contextual_lambda_conversion('date: [0-9]{1,2}(/[0-9]{1,2})?/(19|20)?[0-9]{2}', '[0-9]{1,2}(/[0-9]{1,2})?/(19|20)?[0-9]{2}', text, 'PHI_DATE')
    text = \
        lambda_lib.contextual_lambda_conversion('(date of birth|dob): [0-9]{1,2}(/[0-9]{1,2})?/(19|20)?[0-9]{2}', '[0-9]{1,2}(/[0-9]{1,2})?/(19|20)?[0-9]{2}', text, 'PHI_DATE')
    text = \
        lambda_lib.contextual_lambda_conversion('on [0-9]{1,2}(/[0-9]{1,2})?/(19|20)?[0-9]{2}', '[0-9]{1,2}(/[0-9]{1,2})?/(19|20)?[0-9]{2}', text, 'PHI_DATE')
    return text