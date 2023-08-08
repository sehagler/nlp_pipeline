# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 12:35:50 2019

@author: haglers
"""

#
from base_lib.manager_base_class import Manager_base
from tools_lib.processing_tools_lib.file_processing_tools \
    import write_file

#
class Dynamic_data_manager(Manager_base):
    
    #
    def __init__(self, static_data_object, directory_object, logger_object,
                 processing_data_dir):
        Manager_base.__init__(self, static_data_object, directory_object,
                              logger_object)
        static_data = self.static_data_object.get_static_data()
        project_name = static_data['project_name']
        keywords_filename = project_name + ".keywords.txt"
        self.keywords_filename = processing_data_dir + '/' + keywords_filename
        self.clear_keywords_text()
        
    #
    def append_keywords_text(self, keyword, index_flg):
        if index_flg == 0:
            self.keywords_list.append(keyword)
        elif index_flg == 1: 
            self.keywords_list.append(keyword + ' \d+')
        self.keywords_list = list(set(self.keywords_list))
        
    #
    def clear_keywords_text(self):
        self.keywords_list = []
        
    #
    def generate_keywords_file(self):
        text = ''
        self.keywords_list.sort()
        for keyword in self.keywords_list:
            text += keyword + '\n'
        write_file(self.keywords_file(), text, False, False)
        
    #
    def keywords_file(self):
        return self.keywords_filename
        
    #
    def get_keywords_list(self):
        return self.keywords_list
    
    #
    def merge_copy(self, dynamic_data_manager):
        self.keywords_list.extend(dynamic_data_manager.get_keywords_list())
        self.keywords_list = list(set(self.keywords_list))
        
    #
    def remove_from_keywords_text(self, keyword, index_flg):
        if index_flg == 0:
            self.keywords_list.remove(keyword)
        elif index_flg == 1: 
            self.keywords_list.remove(keyword + ' \d+')
        self.keywords_list = list(set(self.keywords_list))