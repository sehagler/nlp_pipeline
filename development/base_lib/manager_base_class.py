# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 09:04:42 2022

@author: haglers
"""

#
class Manager_base(object):
    
    def __init__(self, static_data_object, directory_object, logger_object):
        self.static_data_object = static_data_object
        self.directory_object = directory_object
        self.logger_object = logger_object
        self.ab_fields_text_dir = \
            directory_object.pull_directory('ab_fields_text_dir')
        self.ab_fields_training_dir = \
            directory_object.pull_directory('ab_fields_training_dir')
        self.common_queries_dir = \
            directory_object.pull_directory('linguamatics_i2e_common_queries_dir')
        self.general_queries_dir = \
            directory_object.pull_directory('linguamatics_i2e_general_queries_dir')
        self.linguamatics_i2e_preprocessing_data_out_dir = \
            directory_object.pull_directory('linguamatics_i2e_preprocessing_data_out')
        self.ohsu_nlp_preprocessing_data_out_dir = \
            directory_object.pull_directory('ohsu_nlp_preprocessing_data_out')
        self.ohsu_nlp_project_simple_templates_dir = \
            directory_object.pull_directory('ohsu_nlp_project_simple_templates_dir')
        self.ohsu_nlp_project_AB_fields_dir = \
            directory_object.pull_directory('ohsu_nlp_project_AB_fields_dir')
        self.postprocessing_data_in_dir = \
            directory_object.pull_directory('postprocessing_data_in')
        self.postprocessing_data_out_dir = \
            directory_object.pull_directory('postprocessing_data_out')
        self.preprocessing_data_out_dir = \
            directory_object.pull_directory('linguamatics_i2e_preprocessing_data_out')
        self.processing_data_dir = \
            directory_object.pull_directory('processing_data_dir')
        self.production_data_dir = \
            directory_object.pull_directory('production_data_dir')
        self.project_queries_dir = \
            directory_object.pull_directory('linguamatics_i2e_project_queries_dir')
        self.software_dir = directory_object.pull_directory('software_dir')
        self.raw_data_dir = directory_object.pull_directory('raw_data_dir')
        self.source_data_dir = directory_object.pull_directory('source_data')
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