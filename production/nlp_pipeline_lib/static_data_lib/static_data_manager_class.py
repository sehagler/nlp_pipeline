# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 12:35:50 2019

@author: haglers
"""

#
import pickle

#
from nlp_pipeline_lib.static_data_lib.manager_lib.directory_manager_class \
    import Directory_manager
from nlp_pipeline_lib.static_data_lib.manager_lib.linguamatics_i2e_file_manager_class \
    import Linguamatics_i2e_file_manager
from nlp_pipeline_lib.static_data_lib.manager_lib.network_manager_class \
    import Network_manager
from tool_lib.py.structure_tools_lib.json_structure_tools \
    import Json_structure_tools

#
class Static_data_manager(object):
    
    #
    def __init__(self, operation_mode, user, root_dir_flg,
                 project_name=None, project_subdir=None):
        network = Network_manager()
        self.static_data = {}
        self.static_data['project_name'] = project_name
        self.static_data['project_subdir'] = project_subdir
        self.static_data['acc_server'] = network.pull_server(operation_mode)
        self.static_data['datetime_keys'] = \
            ['RESULT_COMPLETED_DT','SPECIMEN_COLL_DT']
        self.static_data['do_beaker_ap_flg'] = False
        self.static_data['max_files_per_zip'] = 10000
        self.static_data['mrn_list'] = None
        self.static_data['multiprocessing'] = True
        self.static_data['network_manager'] = network
        self.static_data['num_processes'] = 15
        self.static_data['operation_mode'] = operation_mode
        self.static_data['patient_identifiers'] = [ 'MRN', 'MRN_CD', 'OHSU_MRN' ]
        if self.static_data['project_name'] is not None and \
           self.static_data['project_subdir'] is not None:
            self.static_data['performance_data_files'] = \
                [ self.static_data['project_name']  + '/test/' + \
                  self.static_data['project_name'] + '.performance.json' ]
            self.static_data['project_data_files'] = \
                [ self.static_data['project_name']  + '/' + \
                  self.static_data['project_subdir'] + '/' + \
                  self.static_data['project_name'] + '.json' ]
        self.static_data['raw_data_files_case_number'] = None
        self.static_data['remove_date'] = True
        self.static_data['root_dir_flg'] = root_dir_flg
        self.static_data['text_identifiers'] = [ 'REPORT', 'TEXT' ]
        self.static_data['tmp_data_encoding'] = 'utf-8'
        self.static_data['user'] = user
        self.static_data['x_server'] = 'M01DFSNS02.OHSUM01.OHSU.EDU'
        self.static_data['xml_metadata_keys'] = []
        server = network.pull_server(operation_mode)
        self.static_data['directory_manager'] = \
            Directory_manager(self.static_data, root_dir_flg)
        self.static_data['json_structure_manager'] = \
            Json_structure_tools()
        self.static_data['linguamatics_i2e_file_manager'] = \
            Linguamatics_i2e_file_manager(project_name, user)
            
    #
    def _include_lists(self, docs_files, groups_files, groups_idx_list):
        self.static_data['document_list'] = []
        for docs_file in docs_files:
            with open(docs_file, 'rb') as f:
                document_list = pickle.load(f)
            self.static_data['document_list'].extend(document_list[0])
        self.static_data['document_list'] = \
            list(set(self.static_data['document_list']))
        self.static_data['patient_list'] = []
        for groups_file in groups_files:
            with open(groups_file, 'rb') as f:
                patient_list = pickle.load(f)
            for idx in groups_idx_list:
                self.static_data['patient_list'].extend(patient_list[idx])
        self.static_data['patient_list'] = \
            list(set(self.static_data['patient_list']))
        
    #
    def get_static_data(self):
        return self.static_data