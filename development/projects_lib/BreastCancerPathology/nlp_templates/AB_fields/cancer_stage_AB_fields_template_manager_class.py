# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 17:18:08 2022

@author: haglers
"""

#
from query_lib.processor_lib.cancer_stage_tools \
    import AB_fields_template_manager
    
#
class Cancer_stage_AB_fields_template_manager(AB_fields_template_manager):
    
    #
    def __init__(self, static_data_object, logger_object):
        AB_fields_template_manager.__init__(self, static_data_object,
                                            logger_object)
        self.linguamatics_i2e_AB_fields_path = \
            'General/queries/cancer_stage/cancer_stage_AB_fields'
        self.training_data_file = 'ohsunlptemplate_templates.xlsx'