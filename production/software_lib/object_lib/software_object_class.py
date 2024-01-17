# -*- coding: utf-8 -*-
"""
Created on Wed Aug 1 9:05:23 2018

@author: haglers
"""

#
import os
import shutil

#
from nlp_pipeline_lib.object_lib.directory_lib.directory_object_class \
    import Directory_object
from nlp_pipeline_lib.object_lib.logger_lib.logger_object_class \
    import Logger_object
from nlp_pipeline_lib.registry_lib.remote_lib.remote_registry_class \
    import Remote_registry
from static_data_lib.object_lib.static_data_object_class \
    import Static_data_object

#
class Software_object(object):
    
    #
    def __init__(self, root_dir, user, password):
        self.root_dir = root_dir
        self._create_objects(None, root_dir, None, user, password)
        self._create_registries(root_dir, password)
        self.server_manager = self.remote_registry.get_object('update_manager')
        
    #
    def _cleanup_nlp_software(self, software_dir):
        for root, dirs, files in os.walk(software_dir):
            for name in dirs:
                if name == '__pycache__':
                    shutil.rmtree(os.path.join(root, name))
            for name in files:
                extension = name.split('.')[1]
                if extension == 'i2qy~':
                    os.remove(os.path.join(root, name))
        
    #
    def _copy_nlp_software(self, sandbox_path, software_dir):
        self._cleanup_nlp_software(software_dir)
        if os.path.exists(sandbox_path):
            shutil.rmtree(sandbox_path)
        shutil.copytree('X:/OHSU Shared/Restricted/OCTRI/Informatics/NLP/NLP_Software',
                        sandbox_path, ignore=shutil.ignore_patterns('.git'))
        
    #
    def _copy_x_nlp_software_to_nlp_sandbox(self, dest_drive, software_dir):
        static_data = self.static_data_object.get_static_data()
        if dest_drive == 'X':
            sandbox_path = 'X:/OHSU Shared/Restricted/OCTRI/Informatics/NLP/NLP_Sandbox/' + \
                            static_data['user'] + '/NLP_Software'
        elif dest_drive == 'Z':
            sandbox_path = 'Z:/NLP/NLP_Sandbox/' + static_data['user'] + '/NLP_Software'
        self._copy_nlp_software(sandbox_path, software_dir)
    
    #
    def _create_objects(self, server, root_dir, project_subdir, user,
                         password):
        self.static_data_object = \
            Static_data_object(server, user, root_dir,
                                project_subdir=project_subdir)
        static_data = self.static_data_object.get_static_data()
        self.directory_object = Directory_object(static_data, root_dir)
        self.software_dir = self.directory_object.pull_directory('software_dir')
        log_dir = self.directory_object.pull_directory('log_dir')
        self.logger_object = Logger_object(log_dir)
        self.update_static_data_object = \
            Static_data_object('development', user, root_dir)

    #
    def _create_registries(self, root_dir, password):
        self.remote_registry = \
            Remote_registry(self.static_data_object, 
                            self.update_static_data_object,
                            self.directory_object, self.logger_object,
                            root_dir, password)        
        
    #
    def move_software(self):
        if self.root_dir == 'X':
            dest_drive = 'Z'
        elif self.root_dir == 'Z':
            dest_drive = 'X'
        else:
            log_text = 'bad root directory'
            self.logger.print_log(log_text)
        self._copy_x_nlp_software_to_nlp_sandbox(dest_drive, self.software_dir)