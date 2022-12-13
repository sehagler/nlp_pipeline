# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 12:40:03 2022

@author: haglers
"""

#
import errno
import os

#
from nlp_tools_lib.ohsu_nlp_template_lib.worker_lib.training_worker_class \
    import Training_worker
from tools_lib.processing_tools_lib.file_processing_tools \
    import read_xlsx_file, write_file

#
class AB_fields_manager(object):
    
    #
    def __init__(self, static_data_object):
        self.static_data_object = static_data_object
    
    #
    def train_template(self, template_manager, metadata_manager, data_dir,
                       text_dict):
        A_charge = template_manager.pull_A_charge()
        B_charge = template_manager.pull_B_charge()
        primary_template_list = \
            template_manager.pull_primary_template_list()
        training_worker = Training_worker(self.static_data_object,
                                          template_manager, metadata_manager,
                                          data_dir, text_dict)
        training_worker.train(primary_template_list, A_charge, B_charge)
        template_dict = template_manager.training_template()
        self.AB_field_list = template_dict['AB_field_list']
        self.BA_field_list = template_dict['BA_field_list']
        
    #
    def write_ab_fields(self, template_outlines_dir, filename):
        filename = os.path.join(template_outlines_dir, filename)
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        directory = os.path.dirname(filename)
        with open(os.path.join(filename + '_AB_field.txt'), 'w') as f:
            f.write(str(self.AB_field_list))
        with open(os.path.join(filename + '_BA_field.txt'), 'w') as f:
            f.write(str(self.BA_field_list))