# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 13:28:29 2020

@author: haglers
"""

#
from nlp_text_normalization_lib.base_lib.preprocessor_base_class \
	import Preprocessor_base

#
class Deidentifier(Preprocessor_base):
    
    #
    def _deidentify_age(self):
        self.text = \
            self.lambda_manager.lambda_conversion('\d+(-| )(year|yr)?(s)?(-| )old', self.text, 'PHI_AGE')
        self.text = \
            self.lambda_manager.lambda_conversion('\d+( )?(yo|y\.o\.|y/o)', self.text, 'PHI_AGE')
        
    #
    def _deidentify_date(self):
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('date: \d+/(\d+|\*+)/\d+', '\d+/(\d+|\*+)/\d+', self.text, 'PHI_DATE')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(date of birth|dob): \d+/(\d+|\*+)/\d+', '\d+/(\d+|\*+)/\d+', self.text, 'PHI_DATE')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('on \d+/(\d+|\*+)/\d+', '\d+/(\d+|\*+)/\d+', self.text, 'PHI_DATE')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('on \d+/\d+', '\d+/\d+', self.text, 'PHI_DATE')
    
    #
    def _deidentify_gender(self):
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(\n| )(fe)?male(\n|\.| )', '(?i)(fe)?male', self.text, 'PHI_GENDER')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(\n| )(wo)?man(\n|\.| )', '(?i)(wo)?man', self.text, 'PHI_GENDER')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(\n| )h(er|im|is)(\n|\.| )', '(?i)h(er|im|is)', self.text, 'PHI_HER_HIM_HIS')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(\n| )(s)?he(\n|\.| )', '(?i)(s)?he', self.text, 'PHI_HE_SHE')

    #
    def _deidentify_mrn(self):
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('mr: \d{8} ', '\d{8}', self.text, 'PHI_MRN')
        
    #
    def _deidentify_telephone_number(self):
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('\(\d{3}\) \d{3}-\d{4}', '\(\d{3}\) \d{3}-\d{4}', self.text, 'PHI_TELEPHONE_NUMBER')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('\d{3} \d{3} \d{4}', '\d{3} \d{3} \d{4}', self.text, 'PHI_TELEPHONE_NUMBER')
    
    #
    def remove_phi(self):
        self._deidentify_age()
        if self.static_data['remove_date']:
            self._deidentify_date()
        self._deidentify_gender()
        self._deidentify_mrn()
        self._deidentify_telephone_number()