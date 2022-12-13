# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 11:45:17 2020

@author: haglers
"""

#
from base_lib.preprocessor_base_class import Preprocessor_base

#
class Preprocessor(Preprocessor_base):
    
    #
    def _process_mitotic_rate(self):
        self.text = \
            self.lambda_object.lambda_conversion('(?i)(points )?for mito(s(e|i)s|tic)( (activity|count|figure(s)?|index|rate))', self.text, 'for mitoses')
        match_str0 = '(?i)mito(s(e|i)s|tic)( (activity|count|figure(s)?|index|rate))? \( \d \)'
        match_str1 = '(?i)mito(s(e|i)s|tic)( (activity|count|figure(s)?|index|rate))?'
        self.text = \
            self.lambda_object.contextual_lambda_conversion(match_str0, match_str1, self.text, 'mitoses = ')
        match_str0 = '(?i)mito(s(e|i)s|tic)( (activity|count|figure(s)?|index|rate))?' + \
                     '(:)?((\s)?(grade|score)?( of)?)? \d'
        match_str1 = '(?i)mito(s(e|i)s|tic)( (activity|count|figure(s)?|index|rate))?' + \
                     '(:)?((\s)?(grade|score)?( of)?)?'
        self.text = \
            self.lambda_object.contextual_lambda_conversion(match_str0, match_str1, self.text, 'mitoses = ')
        self.text = \
            self.lambda_object.lambda_conversion('(?i)mito(ses|sis|tic) (activity|count|figure(s)?|index|rate)', self.text, 'mitoses')
        self.text = \
            self.lambda_object.lambda_conversion('(?i)mitos(e|i)s', self.text, 'mitoses')
        self.text = \
            self.lambda_object.lambda_conversion('(?i)mito(ses|sis|tic) (activity|count|figure(s)?|index|rate)', self.text, 'mitoses')
        self.text = \
            self.lambda_object.lambda_conversion('(?i) mitoses per ', self.text, '/')
        self.text = \
            self.lambda_object.lambda_conversion(' a mitoses', self.text, ' mitoses')
        
    #
    def _process_nuclear_pleomorphism(self):
        self.text = \
            self.lambda_object.lambda_conversion('(?i)pleomorphism', self.text, 'nuclear pleomorphism')
        self.text = \
            self.lambda_object.lambda_conversion('(?i)nuclear nuclear', self.text, 'nuclear')
        self.text = \
            self.lambda_object.lambda_conversion('(?i)(points )?for nuclear (atypia|grade|pleomorphism|score)', self.text, 'for nuclei')
        match_str = '(?i)nuclear (atypia|grade|pleomorphism|score) \( \d \)'
        self.text = \
            self.lambda_object.contextual_lambda_conversion(match_str, ' \)', self.text, '')
        match_str = '(?i)nuclear (atypia|grade|pleomorphism|score) \( \d'
        self.text = \
            self.lambda_object.contextual_lambda_conversion(match_str, '\( ', self.text, '')
        match_str0 = '(?i)nuclear (atypia|grade|pleomorphism|score) \d'
        match_str1 = '(?i)nuclear (atypia|grade|pleomorphism|score)'
        self.text = \
            self.lambda_object.contextual_lambda_conversion(match_str0, match_str1, self.text, 'nuclei = ')
        match_str0 = '(?i)nucle(ar|i)( (atypia|grade|pleomorphism|score))?' + \
                    '(:)?((\s)?(grade|score)?( of)?)? \d'
        match_str1 = '(?i)nucle(ar|i)( (atypia|grade|pleomorphism|score))?' + \
                    '(:)?((\s)?(grade|score)?( of)?)?'
        self.text = \
            self.lambda_object.contextual_lambda_conversion(match_str0, match_str1, self.text, 'nuclei = ')
        self.text = \
            self.lambda_object.lambda_conversion('(?i)nuclei', self.text, 'nuclei')
        self.text = \
            self.lambda_object.lambda_conversion('(?i)nuclear (atypia|grade|pleomorphism|score)', self.text, 'nuclei')
        self.text = \
            self.lambda_object.lambda_conversion(' a nuclei', self.text, ' nuclei')
        
    #
    def _process_tubule_formation(self):
        match_str = '(?i)(points )?for (glandular )?(\(acinar\)-)?tub(al|ular|ule(s)?)' + \
                    '( (differentiation|formation))?'
        self.text = \
            self.lambda_object.lambda_conversion(match_str, self.text, 'for tubules')
        match_str = '(?i)(glandular )?(\(acinar\)-)?tub(al|ular|ule(s)?)' + \
                    '( (differentiation|formation))? \( \d \)'
        self.text = \
            self.lambda_object.contextual_lambda_conversion(match_str, ' \)', self.text, '')
        match_str = '(?i)(glandular )?(\(acinar\)-)?tub(al|ular|ule(s)?)' + \
                    '( (differentiation|formation))? \( \d'
        self.text = \
            self.lambda_object.contextual_lambda_conversion(match_str, '\( ', self.text, '')
        match_str0 = '(?i)(glandular )?(\(acinar\)-)?tub(al|ular|ule(s)?)' + \
                     '( (differentiation|formation))? \d'
        match_str1 = '(?i)(glandular )?(\(acinar\)-)?tub(al|ular|ule(s)?)' + \
                     '( (differentiation|formation))?'
        self.text = \
            self.lambda_object.contextual_lambda_conversion(match_str0, match_str1, self.text, 'tubules = ')
        match_str0 = '(?i)(glandular )?(\(acinar\)-)?tub(al|ular|ule(s)?)' + \
                     '( (differentiation|formation))?' + \
                     '(:)?((\s)?(grade|score)?( of)?)? \d'
        match_str1 = '(?i)(glandular )?(\(acinar\)-)?tub(al|ular|ule(s)?)' + \
                     '( (differentiation|formation))?' + \
                     '(:)?((\s)?(grade|score)?( of)?)?'
        self.text = \
            self.lambda_object.contextual_lambda_conversion(match_str0, match_str1, self.text, 'tubules = ')
        match_str = '(?i)(glandular )?(\(acinar\)-)?tub(al|ular|ule(s)?)' + \
                    '( (differentiation|formation))'
        self.text = \
            self.lambda_object.lambda_conversion(match_str, self.text, 'tubules')
        self.text = \
            self.lambda_object.lambda_conversion(' a tubules', self.text, ' tubules')
        
    #
    def run_preprocessor(self):
        self.text = \
            self.lambda_object.lambda_conversion('(?<= )I( / | of )III(?=( |\n))', self.text, '1 / 3')
        self.text = \
            self.lambda_object.lambda_conversion('(?<= )II( / | of )III(?=( |\n))', self.text, '2 / 3')
        self.text = \
            self.lambda_object.lambda_conversion('(?<= )III( / | of )III(?=( |\n))', self.text, '3 / 3')
        self.text = \
            self.lambda_object.lambda_conversion('(?<= )1 of 3(?=( |\n))', self.text, '1 / 3')
        self.text = \
            self.lambda_object.lambda_conversion('(?<= )2 of 3(?=( |\n))', self.text, '2 / 3')
        self.text = \
            self.lambda_object.lambda_conversion('(?<= )3 of 3(?=( |\n))', self.text, '3 / 3')
        text_list = []
        text_list.append('(?i)modified Scarff(-| )Bloom(-| )(and(-| ))?Richardson( \(mSBR\))?')
        text_list.append('(?i)modified Bloom(-| )(and(-| ))?Richardson( \(mBR\))?')
        text_list.append('(?i)Scarff(-| )Bloom(-| )(and(-| ))?Richardson( \(SBR\))?')
        text_list.append('(?i)modified Richardson')
        text_list.append('(?i)Bloom(-| )(and(-| ))?Richardson( \(BR\))?')
        for item in text_list:
            self.text = \
                self.lambda_object.lambda_conversion(item, self.text, 'mSBR')
        self._process_mitotic_rate()
        self._process_nuclear_pleomorphism()
        self._process_tubule_formation()