# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 09:04:57 2019

@author: haglers
"""

#
import glob
import os

#
class Directory_manager(object):
    
    #
    def __init__(self, project_data, root_dir_flg, create_dir_flg=True):
        project_name = project_data['project_name']
        server = project_data['acc_server'][0]
        user = project_data['user']
        self.create_dir_flg = create_dir_flg
        acc_user_dir = 'home/users/' + user
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
        nlp_sandbox_root_dir = software_root_dir + '/NLP_Sandbox/' + user
        nlp_data_processing_root_dir = nlp_sandbox_root_dir + '/NLP_Data_Processing'
        nlp_software_root_dir = nlp_sandbox_root_dir + '/NLP_Software'
        nlp_source_data_root_dir = source_data_root_dir + '/NLP_Source_Data/' + project_name
        self.directory_dict = {}
        self.directory_dict['acc_user_dir'] = acc_user_dir
        self._create_directory(nlp_data_processing_root_dir)
        tmp_dir = os.path.join(nlp_data_processing_root_dir, server)
        self._create_directory(tmp_dir)
        self.directory_dict['processing_data_dir'] = os.path.join(tmp_dir, project_name)
        self._create_directory(self.directory_dict['processing_data_dir'])
        self.directory_dict['raw_data_dir'] = nlp_source_data_root_dir
        self.directory_dict['i2e_queries'] = \
            nlp_software_root_dir + '/' + server + '/projects_lib/' + project_name + '/i2qy'
        self.directory_dict['log_dir'] = \
            os.path.join(self.directory_dict['processing_data_dir'], 'log')
        self._create_directory(self.directory_dict['log_dir'])
        self.directory_dict['metadata_dir'] = \
            os.path.join(self.directory_dict['processing_data_dir'], 'metadata')
        self._create_directory(self.directory_dict['metadata_dir'])
        self.directory_dict['preprocessing_data_out'] = \
            os.path.join(self.directory_dict['processing_data_dir'], 'preprocessing_data_out')
        self._create_directory(self.directory_dict['preprocessing_data_out'])
        self.directory_dict['postprocessing_data_in'] = \
            os.path.join(self.directory_dict['processing_data_dir'], 'postprocessing_data_in')
        self._create_directory(self.directory_dict['postprocessing_data_in'])
        self.directory_dict['postprocessing_data_out'] = \
            os.path.join(self.directory_dict['processing_data_dir'], 'postprocessing_data_out')
        self._create_directory(self.directory_dict['postprocessing_data_out'])
        self.directory_dict['sandbox_dir'] = nlp_sandbox_root_dir
        self.directory_dict['software_dir'] = nlp_software_root_dir
        self.directory_dict['source_data'] = \
            os.path.join(self.directory_dict['processing_data_dir'], 'source_data')
        self._create_directory(self.directory_dict['source_data'])
            
    #
    def _create_directory(self, directory):
        if self.create_dir_flg:
            if not os.path.exists(directory):
                os.makedirs(directory)
                        
    #
    def cleanup_directory(self, label):
        directory = self.directory_dict[label]
        if os.path.exists(directory):
            items = glob.glob(directory + '/*')
            for item in items:
                if os.path.isfile(item):
                    os.remove(item)
                    
    #
    def pull_directory(self, key):
        return self.directory_dict[key]
                    
    #
    def push_directory(self, key, new_dir):
        self.directory_dict[key] = new_dir
        self._create_directory(self.directory_dict[key])