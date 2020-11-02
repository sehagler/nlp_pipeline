# -*- coding: utf-8 -*-
"""
Created on Wed Aug 1 9:05:23 2018

@author: haglers
"""

#
import getpass
import os
import shutil

#
from nlp_lib.py.manager_lib.directory_manager_class import Directory_manager
from nlp_lib.py.manager_lib.network_manager_class import Network_manager
from nlp_lib.py.manager_lib.server_manager_class import Server_manager

#
class Workspace_manager(object):
    
    #
    def __init__(self, password, root_dir_flg):
        self.network_manager = Network_manager()
        self.project_data = {}
        self.project_data['acc_server'] = self.network_manager.pull_server('development')
        self.project_data['project_name'] = 'none'
        self.project_data['root_dir_flg'] = root_dir_flg
        self.project_data['user'] = getpass.getuser()
        self.directory_manager = \
            Directory_manager(self.project_data, root_dir_flg, create_dir_flg=False)
        self.server_manager = Server_manager(self.project_data, password)
        
    #
    def cleanup_nlp_software(self):
        for root, dirs, files in os.walk(self.directory_manager.pull_directory('software_dir')):
            for name in dirs:
                if name == '__pycache__':
                    shutil.rmtree(os.path.join(root, name))
            for name in files:
                extension = name.split('.')[1]
                if extension == 'i2qy~':
                    os.remove(os.path.join(root, name))
        
    #
    def copy_x_nlp_sandbox_to_acc_nlp_sandbox(self):
        acc_nlp_sandbox_path = '/home/users/' + self.project_data['user'] + '/NLP_Sandbox'
        x_nlp_sandbox_path = 'X:/OHSU Shared/Restricted/OCTRI/Informatics/NLP/NLP_Sandbox/'
        self.server_manager.open_ssh_client()
        self.server_manager.remove_directory(acc_nlp_sandbox_path)
        for item in os.listdir(x_nlp_sandbox_path + '/' + self.project_data['user']):
            if item != 'NLP_Data_Processing':
                self.server_manager.push_directory(x_nlp_sandbox_path + '/' + self.project_data['user'] + '/' + item,
                                                   acc_nlp_sandbox_path + '/' + self.project_data['user'] + '/' + item)
        self.server_manager.close_ssh_client()
        
    #
    def copy_x_nlp_software_to_x_nlp_sandbox(self):
        sandbox_path = 'X:/OHSU Shared/Restricted/OCTRI/Informatics/NLP/NLP_Sandbox/' + \
                        self.project_data['user'] + '/NLP_Software'
        if os.path.exists(sandbox_path):
            shutil.rmtree(sandbox_path)
        shutil.copytree('X:/OHSU Shared/Restricted/OCTRI/Informatics/NLP/NLP_Software',
                        sandbox_path)
        
    #
    def copy_x_nlp_software_to_z_nlp_sandbox(self):
        sandbox_path = 'Z:/NLP/NLP_Sandbox/' + self.project_data['user'] + '/NLP_Software'
        if os.path.exists(sandbox_path):
            shutil.rmtree(sandbox_path)
        shutil.copytree('X:/OHSU Shared/Restricted/OCTRI/Informatics/NLP/NLP_Software',
                        sandbox_path)