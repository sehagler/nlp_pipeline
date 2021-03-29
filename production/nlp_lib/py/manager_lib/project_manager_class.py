# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 12:35:50 2019

@author: haglers
"""

#
from nlp_lib.py.manager_lib.directory_manager_class import Directory_manager
from nlp_lib.py.manager_lib.metadata_manager_class import Metadata_manager
from nlp_lib.py.manager_lib.network_manager_class import Network_manager

#
class Project_manager(object):
    
    #
    def __init__(self, operation_mode, project_name, project_subdir, user,
                 root_dir_flg):
        network = Network_manager()
        self.project_data = {}
        self.project_data['acc_server'] = network.pull_server(operation_mode)
        self.project_data['datetime_keys'] = ['RESULT_COMPLETED_DT','SPECIMEN_COLL_DT']
        self.project_data['do_beakerap_flg'] = False
        self.project_data['header_key'] = 'REPORT_HEADER'
        self.project_data['max_files_per_zip'] = 10000
        self.project_data['mrn_list'] = None
        self.project_data['num_processes'] = 10
        self.project_data['operation_mode'] = operation_mode
        self.project_data['project_name'] = project_name
        self.project_data['project_subdir'] = project_subdir
        self.project_data['raw_data_files_case_number'] = None
        self.project_data['root_dir_flg'] = root_dir_flg
        self.project_data['user'] = user
        self.project_data['x_server'] = 'M01DFSNS02.OHSUM01.OHSU.EDU'
        self.project_data['xml_metadata_keys'] = []
        server = network.pull_server(operation_mode)
        self._create_managers(server, user, root_dir_flg)
        
    #
    def _create_managers(self, server, user, root_dir_flg):
        self.project_data['directory_manager'] = Directory_manager(self.project_data, root_dir_flg)
        self.project_data['metadata_manager'] = Metadata_manager(self.project_data['directory_manager'])
        
    #
    def _create_processors(self):
        postprocessor_cmd = 'from projects_lib.' + self.project_data['project_name'] + '.py.' + \
                             self.project_data['project_name'].lower() + '_postprocessor_class ' + \
                             'import ' + self.project_data['project_name'] + '_postprocessor'
        exec(postprocessor_cmd)
        postprocessor_cmd = 'self.project_data[\'report_postprocessor\'] = ' + \
                            self.project_data['project_name'] + \
                            '_postprocessor(\'' + self.project_data['project_name'] + \
                            '\', self.project_data[\'metadata_manager\'])'
        exec(postprocessor_cmd)
        
    #
    def get_project_data(self):
        return self.project_data