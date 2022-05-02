# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 13:12:48 2021

@author: haglers
"""

#
from nlp_pipeline_lib.py.base_lib.preprocessor_base_class \
    import Preprocessor_base
from tool_lib.py.query_tools_lib.cancer_tools \
    import Text_preparation as Text_preparation_cancer
    
#
class Text_cleanup(Preprocessor_base):
    
    #
    def process_document(self, text):
        self.text = text
        self._normalize_whitespace()
        text_preparation = Text_preparation_cancer(self.static_data)
        text_preparation.push_text(self.text)
        text_preparation.cleanup_text()
        self.text = text_preparation.pull_text()
        self._normalize_whitespace()
        return self.text