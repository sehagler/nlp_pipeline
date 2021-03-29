# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 12:35:50 2019

@author: haglers
"""

#
class Dynamic_data_manager(object):
    
    #
    def __init__(self):
        self.clear_keywords_text()
        
    #
    def _append_keywords_text(self, keyword, index_flg):
        if index_flg == 0:
            self.keywords_list.append(keyword)
        elif index_flg == 1: 
            self.keywords_list.append(keyword + ' \d+')
        self.keywords_list = list(set(self.keywords_list))
        
    #
    def append_keywords_text(self, keyword):
        self._append_keywords_text(keyword, 0)
        
    #
    def clear_keywords_text(self):
        self.keywords_list = []
        
    #
    def get_keywords_list(self):
        return self.keywords_list
    
    #
    def merge_copy(self, dynamic_data_manager):
        self.keywords_list.extend(dynamic_data_manager.get_keywords_list())
        self.keywords_list = list(set(self.keywords_list))