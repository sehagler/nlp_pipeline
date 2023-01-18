# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 16:44:15 2021

@author: haglers
"""

#
class Json_structure_tools(object):
    
    #
    def __init__(self):
        self.json_structure_dict = {}
        self.json_structure_dict['document_wrapper_key'] = 'DOCUMENT'
        self.json_structure_dict['documents_wrapper_key'] = 'DOCUMENTS'
        self.json_structure_dict['metadata_key'] = 'METADATA'
        self.json_structure_dict['nlp_data_key'] = 'NLP_DATA'
        self.json_structure_dict['nlp_datetime_key'] = 'DATETIME'
        self.json_structure_dict['nlp_datum_key'] = 'NLP_ELEMENT'
        self.json_structure_dict['nlp_metadata_key'] = 'NLP_METADATA'
        self.json_structure_dict['nlp_performance_key'] = 'NLP_PERFORMANCE'
        self.json_structure_dict['nlp_performance_metadata_key'] = \
            'NLP_PERFORMANCE_METADATA'
        self.json_structure_dict['nlp_query_key'] = 'QUERY'
        self.json_structure_dict['nlp_section_key'] = 'SECTION'
        self.json_structure_dict['nlp_specimen_key'] = 'SPECIMEN'
        self.json_structure_dict['nlp_source_text_key'] = 'NLP_SOURCE_TEXT'
        self.json_structure_dict['nlp_text_element_key'] = 'TEXT_ELEMENT_'
        self.json_structure_dict['nlp_text_key'] = 'TEXT'
        self.json_structure_dict['nlp_tool_output_key'] = \
            'LINGUAMATICS_I2E_OUTPUT'
        self.json_structure_dict['nlp_value_key'] = 'NLP_OUTPUT'
        
        # to be moved to appropriate location
        self.json_structure_dict['manual_review'] = 'MANUAL_REVIEW'
        #
        
    #
    def pull_key(self, key):
        return self.json_structure_dict[key]