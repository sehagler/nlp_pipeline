# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 09:40:02 2022

@author: haglers
"""

#
import copy
import csv
import errno
import os
import xml.etree.ElementTree as ET

#
from nlp_tools_lib.ohsu_nlp_template_lib.py.worker_lib.training_worker_class \
    import Training_worker
from nlp_tools_lib.ohsu_nlp_template_lib.py.worker_lib.worker_base_class \
    import Worker_base
from tool_lib.py.processing_tools_lib.file_processing_tools \
    import read_xlsx_file, write_file

#
class Ohsu_nlp_template_manager(Worker_base):
    
    #
    def __init__(self, static_data_manager):
        Worker_base.__init__(self)
        self.static_data_manager = static_data_manager
    
    #
    def clear_template_output(self):
        self.template_output = []
        
    #
    def create_source_data_file(self, ctr, rpt_text):
        static_data = self.static_data_manager.get_static_data()
        directory_manager = static_data['directory_manager']
        outdir = directory_manager.pull_directory('ohsu_nlp_preprocessing_data_out')
        filename = str(ctr) + '.txt'
        write_file(os.path.join(outdir, filename), rpt_text, False, False)
        ret_val = True
        return ret_val
    
    #
    def run_template(self, template_manager, text_dict):
        template_dict = template_manager.template()
        primary_template_list = template_dict['primary_template_list']
        if 'secondary_template_list' in template_dict.keys():
            secondary_template_list = template_dict['secondary_template_list']
        else:
            secondary_template_list = []
        template_sections_list = template_dict['sections_list']
        self._apply_template(primary_template_list, secondary_template_list,
                             template_sections_list, text_dict)
            
    #
    def train_template(self, template_manager, metadata_manager, data_dir,
                       text_dict):
        A_charge = template_manager.pull_A_charge()
        B_charge = template_manager.pull_B_charge()
        primary_template_list = \
            template_manager.pull_primary_template_list()
        training_worker = Training_worker(self.static_data_manager,
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
        with open(os.path.join(filename[:-4] + '_AB_field.txt'), 'w') as f:
            f.write(str(self.AB_field_list))
        with open(os.path.join(filename[:-4] + '_BA_field.txt'), 'w') as f:
            f.write(str(self.BA_field_list))

    #
    def write_template_output(self, template_manager, data_dir, filename):
        template_dict = template_manager.template()
        template_headers = template_dict['template_headers']
        header = [ 'DOCUMENT_ID', 'DATETIME', 'Section Title', 'Specimen Id' ]
        for i in range(len(template_headers)):
            header.append(template_headers[i])
        header.append('Snippet')
        header.append('Coords')
        with open(os.path.join(data_dir, filename), 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(self.template_output)