# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 09:04:57 2019

@author: haglers
"""

#
import os

#
from tool_lib.py.processing_tools_lib.directory_processing_tools \
    import clean_directory, create_directory

#
class Directory_manager(object):
    
    #
    def __init__(self, static_data, root_dir_flg, create_dir_flg=True):
        self.create_dir_flg = create_dir_flg
        user = static_data['user']
        project_name = static_data['project_name']
        dev_server_root_dir = '/home/groups/hopper2/RDW_NLP_WORKSPACE/NLP'
        prod_server_root_dir = '/home/groups/hopper2/RDW_NLP_WORKSPACE/NLP'
        x_root_dir = 'X:/OHSU Shared/Restricted/OCTRI/Informatics/NLP'
        z_root_dir = 'Z:/NLP'
        if root_dir_flg == 'X':
            processing_root_dir = x_root_dir
            software_root_dir = x_root_dir
            source_data_root_dir = z_root_dir
        elif root_dir_flg == 'Z':
            processing_root_dir = z_root_dir
            software_root_dir = z_root_dir
            source_data_root_dir = z_root_dir
        elif root_dir_flg == 'dev_server':
            processing_root_dir = dev_server_root_dir
            software_root_dir = dev_server_root_dir
            source_data_root_dir = dev_server_root_dir
        elif root_dir_flg == 'prod_server':
            processing_root_dir = dev_server_root_dir
            software_root_dir = dev_server_root_dir
            source_data_root_dir = dev_server_root_dir
        else:
            print('unknown root_dir_flg')
        acc_user_dir = 'home/users/' + user
        nlp_sandbox_root_dir = software_root_dir + '/NLP_Sandbox/' + user
        nlp_software_root_dir = nlp_sandbox_root_dir + '/NLP_Software'
        self.directory_dict = {}
        self.directory_dict['acc_user_dir'] = acc_user_dir
        self.directory_dict['sandbox_dir'] = nlp_sandbox_root_dir
        self.directory_dict['software_dir'] = nlp_software_root_dir
        if project_name is not None:
            project_dir = project_name
            project_subdir = static_data['project_subdir']
            server = static_data['acc_server'][0]
            nlp_data_processing_root_dir = nlp_sandbox_root_dir + '/NLP_Data_Processing'
            nlp_source_data_root_dir = source_data_root_dir + '/NLP_Source_Data/' + \
                                       project_dir + '/' + project_subdir
            if self.create_dir_flg:
                create_directory(nlp_data_processing_root_dir)
            self.directory_dict['processing_base_dir'] = \
                os.path.join(nlp_data_processing_root_dir, server)
            if self.create_dir_flg:
                create_directory(self.directory_dict['processing_base_dir'])
            self.directory_dict['processing_project_dir'] = \
                os.path.join(self.directory_dict['processing_base_dir'], project_dir)
            if self.create_dir_flg:
                create_directory(self.directory_dict['processing_project_dir'])
            self.directory_dict['processing_data_dir'] = \
                os.path.join(self.directory_dict['processing_project_dir'], project_subdir)
            if self.create_dir_flg:
                create_directory(self.directory_dict['processing_data_dir'])
            self.directory_dict['raw_data_dir'] = nlp_source_data_root_dir
            self.directory_dict['log_dir'] = \
                os.path.join(self.directory_dict['processing_data_dir'], 'log')
            if self.create_dir_flg:
                create_directory(self.directory_dict['log_dir'])
            self.directory_dict['metadata_dir'] = \
                os.path.join(self.directory_dict['processing_data_dir'], 'metadata')
            if self.create_dir_flg:
                create_directory(self.directory_dict['metadata_dir'])
            self.directory_dict['preprocessing_data_out'] = \
                os.path.join(self.directory_dict['processing_data_dir'],
                             'preprocessing_data_out')
            if self.create_dir_flg:
                create_directory(self.directory_dict['preprocessing_data_out'])
            self.directory_dict['postprocessing_data_in'] = \
                os.path.join(self.directory_dict['processing_data_dir'], 'postprocessing_data_in')
            if self.create_dir_flg:
                create_directory(self.directory_dict['postprocessing_data_in'])
            self.directory_dict['postprocessing_data_out'] = \
                os.path.join(self.directory_dict['processing_data_dir'], 'postprocessing_data_out')
            if self.create_dir_flg:
                create_directory(self.directory_dict['postprocessing_data_out'])
            self.directory_dict['source_data'] = \
                os.path.join(self.directory_dict['processing_data_dir'], 'source_data')
            if self.create_dir_flg:
                create_directory(self.directory_dict['source_data'])
            self.directory_dict['template_outlines_dir'] = \
                os.path.join(self.directory_dict['processing_data_dir'], 'template_outlines')
            if self.create_dir_flg:
                create_directory(self.directory_dict['template_outlines_dir'])
            self._linguamatics_i2e_directories(nlp_software_root_dir, server,
                                               project_dir)
            self._melax_clamp_directories()
            self._ohsu_nlp_directories(nlp_software_root_dir, server,
                                            project_dir)
                
    #
    def _linguamatics_i2e_directories(self, nlp_software_root_dir, server,
                                      project_dir):
        self.directory_dict['linguamatics_i2e_general_queries_dir'] = \
            nlp_software_root_dir + '/' + server + '/tool_lib/i2qy'
        self.directory_dict['linguamatics_i2e_project_queries_dir'] = \
            nlp_software_root_dir + '/' + server + '/projects_lib/' + \
            project_dir + '/i2e_templates'
        self.directory_dict['linguamatics_i2e_preprocessing_data_out'] = \
            os.path.join(self.directory_dict['preprocessing_data_out'],
                         'linguamatics_i2e_preprocessing_data_out')
        if self.create_dir_flg:
            create_directory(self.directory_dict['linguamatics_i2e_preprocessing_data_out'])
                
    #
    def _melax_clamp_directories(self):
        self.directory_dict['melax_clamp_preprocessing_data_out'] = \
            os.path.join(self.directory_dict['preprocessing_data_out'],
                         'melax_clamp_preprocessing_data_out')
        if self.create_dir_flg:
            create_directory(self.directory_dict['melax_clamp_preprocessing_data_out'])
                
    #
    def _ohsu_nlp_directories(self, nlp_software_root_dir, server, project_dir):
        self.directory_dict['ohsu_nlp_preprocessing_data_out'] = \
            os.path.join(self.directory_dict['preprocessing_data_out'],
                         'ohsu_nlp_preprocessing_data_out')
        if self.create_dir_flg:
            create_directory(self.directory_dict['ohsu_nlp_preprocessing_data_out'])
        self.directory_dict['ohsu_nlp_project_queries_dir'] = \
            nlp_software_root_dir + '/' + server + '/projects_lib/' + \
            project_dir + '/nlp_templates'
            
    #
    def cleanup_directory(self, label):
        directory = self.directory_dict[label]
        clean_directory(directory)
                    
    #
    def pull_directory(self, key):
        return self.directory_dict[key]
                    
    #
    def push_directory(self, key, new_dir):
        self.directory_dict[key] = new_dir
        create_directory(self.directory_dict[key])