# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 13:28:29 2020

@author: haglers
"""

#
from nlp_lib.py.document_preprocessing_lib.base_class_lib.preprocessor_base_class \
	import Preprocessor_base

#
class Deidentifier(Preprocessor_base):
    
    #
    def _remove_age(self):
        self._general_command('(?i)\d+(-| )(year|yr)?(s)?(-| )old', {None : 'PHI_AGE'})
        self._general_command('(?i)\d+( )?(yo|y\.o\.|y/o)', {None : 'PHI_AGE'})
        
    #
    def _remove_date(self):
        self._general_command('(?i)date: \d+/(\d+|\*+)/\d+', {'\d+/(\d+|\*+)/\d+' : 'PHI_DATE'})
        self._general_command('(?i)(date of birth|dob): \d+/(\d+|\*+)/\d+', {'\d+/(\d+|\*+)/\d+' : 'PHI_DATE'})
        self._general_command('(?i)on \d+/(\d+|\*+)/\d+', {'\d+/(\d+|\*+)/\d+' : 'PHI_DATE'})
        self._general_command('(?i)on \d+/\d+', {'\d+/\d+' : 'PHI_DATE'})
    
    #
    def _remove_gender(self):
        self._general_command('(?i)(\n| )(fe)?male(\n|\.| )', {'(?i)(fe)?male' : 'PHI_GENDER'})
        self._general_command('(?i)(\n| )(wo)?man(\n|\.| )', {'(?i)(wo)?man' : 'PHI_GENDER'})
        self._general_command('(?i)(\n| )h(er|im|is)(\n|\.| )', {'(?i)h(er|im|is)' : 'PHI_HER_HIM_HIS'})
        self._general_command('(?i)(\n| )(s)?he(\n|\.| )', {'(?i)(s)?he' : 'PHI_HE_SHE'})

    #
    def _remove_mrn(self):
        self._general_command('(?i)mr: \d{8} ', {'\d{8}' : 'PHI_MRN'})
        
    #
    def _remove_telephone_number(self):
        self._general_command('\(\d{3}\) \d{3}-\d{4}', {'\(\d{3}\) \d{3}-\d{4}' : 'PHI_TELEPHONE_NUMBER'})
        self._general_command('\d{3} \d{3} \d{4}', {'\d{3} \d{3} \d{4}' : 'PHI_TELEPHONE_NUMBER'})
    
    #
    def remove_phi(self):
        self._remove_age()
        if self.static_data['remove_date']:
            self._remove_date()
        self._remove_gender()
        self._remove_mrn()
        self._remove_telephone_number()