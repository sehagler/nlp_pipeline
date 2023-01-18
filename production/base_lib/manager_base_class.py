# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 09:04:42 2022

@author: haglers
"""

#
class Manager_base(object):
    
    def __init__(self, static_data_object):
        self.static_data_object = static_data_object
        static_data = self.static_data_object.get_static_data()
        self.json_structure_tools = static_data['json_structure_tools']
        self.document_wrapper_key = \
            self.json_structure_tools.pull_key('document_wrapper_key')
        self.documents_wrapper_key = \
            self.json_structure_tools.pull_key('documents_wrapper_key')
        self.manual_review = \
            self.json_structure_tools.pull_key('manual_review')
        self.metadata_key = \
            self.json_structure_tools.pull_key('metadata_key')
        self.nlp_data_key = \
            self.json_structure_tools.pull_key('nlp_data_key')
        self.nlp_datetime_key = \
            self.json_structure_tools.pull_key('nlp_datetime_key')
        self.nlp_datum_key = \
            self.json_structure_tools.pull_key('nlp_datum_key')
        self.nlp_metadata_key = \
            self.json_structure_tools.pull_key('nlp_metadata_key')
        self.nlp_performance_key = \
            self.json_structure_tools.pull_key('nlp_performance_key')
        self.nlp_performance_metadata_key = \
            self.json_structure_tools.pull_key('nlp_performance_metadata_key')
        self.nlp_query_key = \
            self.json_structure_tools.pull_key('nlp_query_key')
        self.nlp_section_key = \
            self.json_structure_tools.pull_key('nlp_section_key')
        self.nlp_specimen_key = \
            self.json_structure_tools.pull_key('nlp_specimen_key')
        self.nlp_source_text_key = \
            self.json_structure_tools.pull_key('nlp_source_text_key')
        self.nlp_text_element_key = \
            self.json_structure_tools.pull_key('nlp_text_element_key')
        self.nlp_text_key = \
            self.json_structure_tools.pull_key('nlp_text_key')
        self.nlp_tool_output_key = \
            self.json_structure_tools.pull_key('nlp_tool_output_key')
        self.nlp_value_key = \
            self.json_structure_tools.pull_key('nlp_value_key')