# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 09:04:57 2019

@author: haglers
"""

#
from datetime import datetime
import os

#
from tools_lib.processing_tools_lib.directory_processing_tools \
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
            processing_root_dir = None
            software_root_dir = None
            source_data_root_dir = None
            print('unknown root_dir_flg')
        if software_root_dir is not None:
            acc_user_dir = 'home/users/' + user
            nlp_sandbox_root_dir = software_root_dir + '/NLP_Sandbox/' + user
            nlp_software_root_dir = nlp_sandbox_root_dir + '/NLP_Software'
            self.directory_dict = {}
            self.directory_dict['acc_user_dir'] = acc_user_dir
            self.directory_dict['sandbox_dir'] = nlp_sandbox_root_dir
            self.directory_dict['software_dir'] = nlp_software_root_dir
            
            project_dir = project_name
            project_subdir = static_data['project_subdir']
            
            if static_data['acc_server'] is not None:
                server = static_data['acc_server'][0]
            else:
                server = None
            
            nlp_data_processing_root_dir = \
                nlp_sandbox_root_dir + '/NLP_Data_Processing'
            if self.create_dir_flg:
                create_directory(nlp_data_processing_root_dir)
                
            if project_dir is not None and project_subdir is not None:
                nlp_source_data_root_dir = source_data_root_dir + '/NLP_Source_Data/' + \
                                           project_dir + '/' + project_subdir
                if self.create_dir_flg:
                    create_directory(nlp_source_data_root_dir)
            else:
                nlp_source_data_root_dir = None
                
            self._create_dict_entry('processing_base_dir',
                                    nlp_data_processing_root_dir, server)
            self._create_dict_entry('processing_project_dir',
                                    self.directory_dict['processing_base_dir'],
                                    project_dir)
            self._create_dict_entry('processing_data_dir',
                                    self.directory_dict['processing_project_dir'],
                                    project_subdir)
                
            self.directory_dict['raw_data_dir'] = nlp_source_data_root_dir
            
            self._create_dict_entry('log_dir',
                                    self.directory_dict['processing_data_dir'],
                                    'log')
            self._create_dict_entry('metadata_dir',
                                    self.directory_dict['processing_data_dir'],
                                    'metadata')
            self._create_dict_entry('preprocessing_data_out',
                                    self.directory_dict['processing_data_dir'],
                                    'preprocessing_data_out')
            self._create_dict_entry('postprocessing_data_in',
                                    self.directory_dict['processing_data_dir'],
                                    'postprocessing_data_in')
            self._create_dict_entry('postprocessing_data_out',
                                    self.directory_dict['processing_data_dir'],
                                    'postprocessing_data_out')
            self._create_dict_entry('source_data',
                                    self.directory_dict['processing_data_dir'],
                                    'source_data')
            self._create_dict_entry('template_outlines_dir',
                                    self.directory_dict['processing_data_dir'],
                                    'template_outlines')
            self._create_dict_entry('simple_templates_dir',
                                    self.directory_dict['template_outlines_dir'],
                                    'simple_templates')
            self._create_dict_entry('AB_fields_dir',
                                    self.directory_dict['template_outlines_dir'],
                                    'AB_fields')
            self._linguamatics_i2e_directories(nlp_software_root_dir, server,
                                               project_dir)
            if self.directory_dict['processing_data_dir'] is not None:
                now = datetime.now()
                datetime_str = now.strftime('_%Y%m%d_%H%M%S')
                self.directory_dict['production_data_dir'] = \
                    os.path.join(self.directory_dict['processing_data_dir'],
                                 static_data['project_name'] + datetime_str)
            self._melax_clamp_directories()
            self._ohsu_nlp_directories(nlp_software_root_dir, server,
                                            project_dir)
            
    #
    def _create_dict_entry(self, key, base_path, new_dir):
        if (base_path is not None) and (new_dir is not None):
            key_dir = os.path.join(base_path, new_dir)
            create_dir_flg = self.create_dir_flg
        else:
            key_dir = None
            create_dir_flg = False
        self.directory_dict[key] = key_dir
        if create_dir_flg:
            create_directory(self.directory_dict[key])
                    
    #
    def _linguamatics_i2e_directories(self, nlp_software_root_dir, server,
                                      project_dir):
        if server is not None:
            self.directory_dict['linguamatics_i2e_common_queries_dir'] = \
                nlp_software_root_dir + '/' + server + '/query_lib/linguamatics_lib/i2qy/Common'
            self.directory_dict['linguamatics_i2e_general_queries_dir'] = \
                nlp_software_root_dir + '/' + server + '/query_lib/linguamatics_lib/i2qy/General'
        else:
            self.directory_dict['linguamatics_i2e_common_queries_dir'] = None
            self.directory_dict['linguamatics_i2e_general_queries_dir'] = None
        if project_dir is not None:
            self.directory_dict['linguamatics_i2e_project_queries_dir'] = \
                nlp_software_root_dir + '/' + server + '/projects_lib/' + \
                project_dir + '/i2e_templates'
        else:
            self.directory_dict['linguamatics_i2e_project_queries_dir'] = None
        self._create_dict_entry('linguamatics_i2e_preprocessing_data_out',
                                self.directory_dict['preprocessing_data_out'],
                                'linguamatics_i2e_preprocessing_data_out')  

    #
    def _melax_clamp_directories(self):
        self._create_dict_entry('melax_clamp_preprocessing_data_out',
                                self.directory_dict['preprocessing_data_out'],
                                'melax_clamp_preprocessing_data_out') 
                
    #
    def _ohsu_nlp_directories(self, nlp_software_root_dir, server, project_dir):
        if project_dir is not None:
            self.directory_dict['ohsu_nlp_project_simple_templates_dir'] = \
                nlp_software_root_dir + '/' + server + '/projects_lib/' + \
                project_dir + '/nlp_templates/simple_templates'
            self.directory_dict['ohsu_nlp_project_AB_fields_dir'] = \
                nlp_software_root_dir + '/' + server + '/projects_lib/' + \
                project_dir + '/nlp_templates/AB_fields'
        else:
            self.directory_dict['ohsu_nlp_project_queries_dir'] = None
        self._create_dict_entry('ohsu_nlp_preprocessing_data_out',
                                self.directory_dict['preprocessing_data_out'],
                                'ohsu_nlp_preprocessing_data_out')
            
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