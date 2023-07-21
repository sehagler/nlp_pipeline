# -*- coding: utf-8 -*-
"""
Created on Wed Aug 1 9:05:23 2018

@author: haglers
"""

#
import os
import shutil

#
from base_lib.manager_base_class import Manager_base

#
class Software_manager(Manager_base):
    
    #
    def __init__(self, static_data_object, logger_object, server_manager):
        Manager_base.__init__(self, static_data_object, logger_object)
        self.static_data = static_data_object.get_static_data()
        self.server_manager = server_manager
        self.directory_manager = self.static_data['directory_manager']
        self.network_manager = self.static_data['network_manager']
        
    #
    def _copy_nlp_software(self, sandbox_path):
        self.cleanup_nlp_software()
        if os.path.exists(sandbox_path):
            shutil.rmtree(sandbox_path)
        shutil.copytree('X:/OHSU Shared/Restricted/OCTRI/Informatics/NLP/NLP_Software',
                        sandbox_path, ignore=shutil.ignore_patterns('.git'))
    
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
    def copy_x_nlp_software_to_nlp_sandbox(self, dest_drive):
        if dest_drive == 'X':
            sandbox_path = 'X:/OHSU Shared/Restricted/OCTRI/Informatics/NLP/NLP_Sandbox/' + \
                            self.static_data['user'] + '/NLP_Software'
        elif dest_drive == 'Z':
            sandbox_path = 'Z:/NLP/NLP_Sandbox/' + self.static_data['user'] + '/NLP_Software'
        self._copy_nlp_software(sandbox_path)