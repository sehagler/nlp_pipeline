# -*- coding: utf-8 -*-
"""
Created on Mon May 20 12:25:32 2019

@author: haglers
"""

#
import re

#
from lambda_lib.lambda_manager_class import Lambda_manager

#
class Preprocessor_base(object):
    
    #
    def __init__(self, static_data):
        self.static_data = static_data
        self.lambda_manager = Lambda_manager()
        self.command_list = []
        self.text = ''
        
    #
    def _append_keywords_text(self, keyword, index_flg=1):
        keyword = re.sub(self.section_header_pre_tag, '', keyword)
        keyword = re.sub(self.section_header_post_tag, '', keyword)
        self.dynamic_data_manager.append_keywords_text(keyword, index_flg)
        
    #
    def _insert_whitespace(self, match_str, whitespace):
        match = 0
        m_str = re.compile(match_str)
        while match is not None:
            match = m_str.search(self.text, re.IGNORECASE)
            if match is not None:
                self.text = self.text[:match.start()] + whitespace + \
                            self.text[match.start()+1:]
    
    #
    def _normalize_whitespace(self):
        self.text = \
            self.lambda_manager.lambda_conversion('\n\t', self.text, '\n')
        self.text = \
            self.lambda_manager.lambda_conversion('\r\n', self.text, '\n')
        self.text = \
            self.lambda_manager.lambda_conversion('\n*\n\n', self.text, '\n\n')
        self.text = \
            self.lambda_manager.lambda_conversion('[\n\s]*\n\s*\n', self.text, '\n\n')
        self.text = \
            self.lambda_manager.lambda_conversion('\n *', self.text, '\n')
        self.text = \
            self.lambda_manager.lambda_conversion(' *\n', self.text, '\n')
        self.text = \
            self.lambda_manager.lambda_conversion('\n-', self.text, '\n\t-')
        self.text = \
            self.lambda_manager.lambda_conversion('\t+', self.text, '\t')
        self.text = \
            self.lambda_manager.lambda_conversion(' ?\t ?', self.text, '\t')
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('^[\n\s]*', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('[\n\s]*$', self.text)
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('^ +[-]', ' ', self.text, '')
        self.text = \
            self.lambda_manager.lambda_conversion(' +', self.text, ' ')
        for _ in range(2):
            self.text = \
                self.lambda_manager.lambda_conversion(' \n', self.text, '\n')
                
    #
    def _remove_from_keywords_text(self, keyword, index_flg=1):
        self.dynamic_data_manager.remove_from_keywords_text(keyword, index_flg)
     
    #
    def pull_dynamic_data_manager(self):
        return self.dynamic_data_manager
     
    #
    def pull_text(self):
        return self.text
    
    #
    def push_dynamic_data_manager(self, dynamic_data_manager):
        self.dynamic_data_manager = dynamic_data_manager
     
    #
    def push_text(self, text):
        self.text = text