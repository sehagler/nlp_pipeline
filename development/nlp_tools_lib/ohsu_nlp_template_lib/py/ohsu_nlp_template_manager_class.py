# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 09:40:02 2022

@author: haglers
"""

#
import copy
import csv
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
    def __init__(self, static_data_manager, xls_manager_registry,
                 evaluation_manager):
        Worker_base.__init__(self)
        self.static_data_manager = static_data_manager
        self.xls_manager_registry = xls_manager_registry
        self.evaluation_manager = evaluation_manager
    
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
    def train_template(self, template_manager, metadata_manager, xls_manager,
                       data_dir, text_dict):
        training_worker = Training_worker(self.static_data_manager,
                                          template_manager, metadata_manager,
                                          self.xls_manager_registry,
                                          xls_manager, data_dir, text_dict)
        training_worker.train()
        template_dict = template_manager.training_template()
        primary_template_list = template_dict['primary_template_list']
        self.primary_template_list = primary_template_list
        
    #
    def write_template_outline(self, template_outlines_dir, filename):
        with open(os.path.join(template_outlines_dir, filename), 'w') as f:
            f.write(str(self.primary_template_list))

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