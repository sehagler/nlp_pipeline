# -*- coding: utf-8 -*-
"""
Created on Wed Aug 1 9:05:23 2018

@author: haglers
"""

#
from datetime import datetime
import getpass
import math
from matplotlib import pyplot as plt
import pickle
import random

#
from nlp_lib.py.manager_lib.process_manager_class import Process_manager
from nlp_lib.py.manager_lib.server_manager_class import Server_manager
from nlp_lib.py.tool_lib.processing_tools_lib.file_processing_tools \
    import read_json_file
from nlp_lib.py.tool_lib.query_tools_lib.date_tools import datetime2matlabdn

#
class Pipeline_manager(object):
    
    #
    def __init__(self, password, operation_mode, project, root_dir_flg):
        import_cmd = 'from projects_lib.' + project + '.py.' + project.lower() + \
                     '_project_manager_class import ' + project + \
                     '_project_manager as Project_manager'
        exec(import_cmd, globals())
        import_cmd = 'from projects_lib.' + project + '.py.' + project.lower() + \
                     '_test_manager_class import ' + project + \
                     '_test_manager as Test_manager'
        exec(import_cmd, globals())
        user = getpass.getuser()
        project_manager = Project_manager(operation_mode, user, root_dir_flg)
        self.project_data = project_manager.get_project_data()
        self.process_manager = Process_manager(self.project_data, password)
        self.test_manager = Test_manager(self.project_data, root_dir_flg)
        self.server_manager = Server_manager(self.project_data, password)
   
    #
    def _get_metadata_values(self):
        metadata_json_file = \
            self.project_data['metadata_manager'].get_metadata_json_file()
        metadata = read_json_file(metadata_json_file)
        num_documents = len(metadata.keys())
        document_values = []
        patient_values = []
        date_values = []
        for key0 in metadata.keys():
            for key1 in metadata[key0].keys():
                if key1 in self.project_data['datetime_identifiers'].keys():
                    date_str = metadata[key0][key1]
                    date_num = \
                        datetime2matlabdn(datetime.strptime(date_str,
                                                            self.project_data['datetime_identifiers'][key1]))
                    date_values.append(date_num)
                if key1 in self.project_data['document_identifiers']:
                    document_values.append(metadata[key0][key1])
                if key1 in self.project_data['patient_identifiers']:
                    patient_values.append(metadata[key0][key1])
        document_values = list(set(document_values))
        patient_values = list(set(patient_values))
        date_values.sort()
        patient_values.sort()
        return document_values, patient_values, date_values
        
    #
    def _quality_control(self):
        document_values, patient_values, date_values = self._get_metadata_values()
        num_documents = len(list(set(document_values)))
        num_days = round(date_values[-1] - date_values[0])
        num_patients = len(patient_values)
        plt.hist(date_values, bins=num_days)
        print('number of documents: %d' % num_documents)
        print('number of patients: %d' % num_patients)
        
    #
    def download_queries(self):
        self.process_manager.download_queries()
        
    #
    def generate_training_data_sets(self):
        doc_fraction = 0.1
        num_groups = 4
        self.process_manager.preprocessor(1, False, preprocess_files_flg=False)
        document_values, patient_values, date_values = self._get_metadata_values()
        num_documents = len(document_values)
        print(num_documents)
        print(len(patient_values))
        random.shuffle(document_values)
        number_training_docs = math.floor(doc_fraction * len(document_values))
        training_docs = document_values[:number_training_docs]
        with open('training_docs.pkl', 'wb') as f:
            pickle.dump([document_values, training_docs], f)
        random.shuffle(patient_values)
        patients_per_group = math.floor(len(patient_values)/num_groups)
        training_groups = []
        for i in range(num_groups-1):
            training_groups.append(patient_values[0:patients_per_group])
            patient_values = patient_values[patients_per_group:]
        training_groups.append(patient_values)
        with open('training_groups.pkl', 'wb') as f:
            pickle.dump(training_groups, f)
            
    #
    def post_queries(self):
        self.process_manager.postprocessor()
        self.process_manager.packager()
            
    #
    def pre_queries(self, preprocessor_start_idx=0, preprocessor_cleanup_flg=True):
        if preprocessor_start_idx >= 0:
            if preprocessor_start_idx > 0:
                preprocessor_cleanup_flg = False
            self.process_manager.preprocessor(preprocessor_start_idx, preprocessor_cleanup_flg)
            #self._quality_control()
        self.process_manager.preindexer()
        self.process_manager.indexer()
        self.process_manager.postindexer()
        
    #
    def test(self):
        #self.test_manager.compare_preprocessor_output()
        #self.test_manager.compare_postprocessor_output()
        self.test_manager.data_validation()