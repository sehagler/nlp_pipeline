# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 12:35:50 2019

@author: haglers
"""

#
import pickle

#
from nlp_pipeline_lib.object_lib.directory_lib.directory_object_class \
    import Directory_object
from static_data_lib.tools_lib.json_structure_tools \
    import Json_structure_tools
from static_data_lib.tools_lib.section_header_structure_tools \
    import Section_header_structure_tools
    
#
def _get_server_dict():
    server_dict = {}
    server_dict['development'] = \
        [ 'development', 'hopper1.ohsu.edu', 'https://hopper1.ohsu.edu:8334' ]
    server_dict['production'] = \
        [ 'production', 'hopper2.ohsu.edu', 'https://hopper2.ohsu.edu:8334' ]
    return server_dict

#
class Static_data_object(object):
    
    #
    def __init__(self, operation_mode, user, root_dir_flg,
                 project_name=None, project_subdir=None):
        server_dict = _get_server_dict()
        self.static_data = {}
        self.static_data['project_name'] = project_name
        self.static_data['project_subdir'] = project_subdir
        if operation_mode is not None:
            self.static_data['acc_server'] = server_dict[operation_mode]
        else:
            self.static_data['acc_server'] = None
        self.static_data['datetime_keys'] = \
            ['RESULT_COMPLETED_DT','SPECIMEN_COLL_DT']
        self.static_data['docs_per_processor'] = 10000
        self.static_data['max_files_per_zip'] = 10000
        self.static_data['mrn_list'] = None
        self.static_data['multiprocessing'] = True
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
        self.static_data['directory_object'] = \
            Directory_object(self.static_data, root_dir_flg)
        self.static_data['json_structure_tools'] = \
            Json_structure_tools()
        self.static_data['section_header_structure_tools'] = \
            Section_header_structure_tools()
            
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