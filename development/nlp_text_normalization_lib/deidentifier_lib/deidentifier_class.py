# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 13:28:29 2020

@author: haglers
"""

#

from lambda_lib.lambda_manager_class import Lambda_manager

#
class Deidentifier(object):
    
    #
    def __init__(self, static_data):
        self.static_data = static_data
        self.lambda_manager = Lambda_manager()
    
    #
    def _deidentify_age(self):
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('[0-9]+( - | )?y/o', '[0-9]+', self.text, 'PHI_AGE')
        
    #
    def _deidentify_date(self):
        self.text = \
            self.lambda_manager.lambda_conversion('[0-9]{1,2}/[0-9]{1,2}/(19|20)[0-9]{2}', self.text, 'PHI_DATE')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('date: [0-9]{1,2}(/[0-9]{1,2})?/(19|20)?[0-9]{2}', '[0-9]{1,2}(/[0-9]{1,2})?/(19|20)?[0-9]{2}', self.text, 'PHI_DATE')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(date of birth|dob): [0-9]{1,2}(/[0-9]{1,2})?/(19|20)?[0-9]{2}', '[0-9]{1,2}(/[0-9]{1,2})?/(19|20)?[0-9]{2}', self.text, 'PHI_DATE')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('on [0-9]{1,2}(/[0-9]{1,2})?/(19|20)?[0-9]{2}', '[0-9]{1,2}(/[0-9]{1,2})?/(19|20)?[0-9]{2}', self.text, 'PHI_DATE')
    
    #
    def _deidentify_gender(self):
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(\n| )(fe)?male(\n|\.| )', '(fe)?male', self.text, 'PHI_GENDER')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(\n| )(wo)?man(\n|\.| )', '(wo)?man', self.text, 'PHI_GENDER')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(\n| )boy(\n|\.| )', 'boy', self.text, 'PHI_GENDER')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(\n| )girl(\n|\.| )', 'girl', self.text, 'PHI_GENDER')

    #
    def _deidentify_mrn(self):
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('mrn: \d{8} ', '\d{8}', self.text, 'PHI_MRN')
            
    #
    def _deidentify_personal_name(self):
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('[A-Za-z]+ [A-Z]\. [A-Za-z]+, M(\.)?D(\.)?',
                                                             ' [A-Z]\.(?!D)', self.text, '')
            
    #
    def _deidentify_pronouns(self):
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(\n| )h(er|im|is)(\n|\.| )', 'h(er|im|is)', self.text, 'PHI_HER_HIM_HIS')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(\n| )(s)?he(\n|\.| )', '(s)?he', self.text, 'PHI_HE_SHE')
        
    #
    def _deidentify_telephone_number(self):
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('\(\d{3}\) \d{3}-\d{4}', '\(\d{3}\) \d{3}-\d{4}', self.text, 'PHI_TELEPHONE_NUMBER')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('\d{3} \d{3} \d{4}', '\d{3} \d{3} \d{4}', self.text, 'PHI_TELEPHONE_NUMBER')
    
    #
    def deidentify_text(self, text):
        self.text = text
        self._deidentify_age()
        if self.static_data['remove_date']:
            self._deidentify_date()
        self._deidentify_gender()
        self._deidentify_mrn()
        #self._deidentify_personal_name()
        self._deidentify_pronouns()
        self._deidentify_telephone_number()
        return self.text