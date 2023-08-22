# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 09:40:02 2022

@author: haglers
"""

#
from nlp_tools_lib.ohsu_nlp_template_lib.object_lib.AB_fields_object_class \
    import AB_fields_object
from nlp_tools_lib.ohsu_nlp_template_lib.object_lib.simple_template_object_class \
    import Simple_template_object
    
#
def _create_text_dict_postprocessing_data_in(sections, document_ids):
    text_dict = {}
    for document_id in document_ids:
        text_dict[document_id] = {}
        for i in range(1, len(sections)):
            row = sections[i]
            if row[0] == document_id:
                key = (row[2], row[3])
                section = row[4]
                offset_base = 0
                if section != '.*':
                    text_dict[document_id][key] = {}
                    text_dict[document_id][key]['OFFSET_BASE'] = offset_base
                    text_dict[document_id][key]['TEXT'] = section
    return text_dict

#
class Ohsu_nlp_template_object(object):
    
    #
    def __init__(self, static_data_object):
        self.ab_fields_object = AB_fields_object(static_data_object)
        self.simple_template_object = Simple_template_object()
    
    #
    def clear_simple_template_output(self):
        self.simple_template_object.clear_template_output()
        
    #
    def clear_template_output(self):
        self.template_output = []
        
    #
    def pull_simple_template_output(self):
        template_output = self.simple_template_object.pull_template_output()
        return template_output
    
    #
    def run_simple_template(self, argument_dict):
        doc_list = argument_dict['doc_list']
        sections = argument_dict['sections']
        template_object = argument_dict['template_object']
        if len(sections) > 0:
            text_dict = _create_text_dict_postprocessing_data_in(sections,
                                                                 doc_list)
        else:
            text_dict = None
        del argument_dict
        del sections
        self.simple_template_object.run_template(template_object, 
                                                 text_dict, doc_list)
            
    #
    def train_ab_fields(self, template_manager, metadata_manager, data_dir,
                        text_dict):
        self.ab_fields_object.train_template(template_manager, 
                                             metadata_manager, data_dir,
                                             text_dict)
        
    #
    def write_ab_fields(self, template_outlines_dir, filename):
        self.ab_fields_object.write_ab_fields(template_outlines_dir, filename)