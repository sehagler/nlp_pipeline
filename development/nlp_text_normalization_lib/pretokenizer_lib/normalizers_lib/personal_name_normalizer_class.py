# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 12:56:51 2021

@author: haglers
"""

#
from nlp_text_normalization_lib.base_lib.preprocessor_base_class \
    import Preprocessor_base

#
class Personal_name_normalizer(Preprocessor_base):

    #
    def process_text(self, text):
        self.push_text(text)
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('[A-Za-z]+ [A-Z]\. [A-Za-z]+, M(\.)?D(\.)?',
                                                             ' [A-Z]\.(?!D)', self.text, '')
        text = self.pull_text()
        return text