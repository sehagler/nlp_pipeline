# -*- coding: utf-8 -*-
"""
Created on Mon May 20 12:25:32 2019

@author: haglers
"""

#
class Preprocessor_base(object):
    
    #
    def pull_text(self):
        return self.text
     
    #
    def push_text(self, text):
        self.text = text