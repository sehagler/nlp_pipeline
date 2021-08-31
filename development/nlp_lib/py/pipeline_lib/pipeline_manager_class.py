# -*- coding: utf-8 -*-
"""
Created on Wed Aug 1 9:05:23 2018

@author: haglers
"""

#
from datetime import datetime
import math
from matplotlib import pyplot as plt
import os
import pickle
import random
import re

#
from linguamatics_i2e_lib.py.linguamatics_i2e_manager_class \
    import Linguamatics_i2e_manager
from nlp_lib.py.file_lib.json_manager_class import Json_manager
from nlp_lib.py.metadata_lib.metadata_manager_class import Metadata_manager
from nlp_lib.py.process_lib.process_manager_class import Process_manager
from tool_lib.py.processing_tools_lib.file_processing_tools \
    import read_json_file
from tool_lib.py.query_tools_lib.date_tools import datetime2matlabdn

#
class Pipeline_manager(object):
    
    #
    def __init__(self, static_data_manager, server_manager, root_dir_flg,
                 password):
        self.static_data = static_data_manager.get_static_data()
        self._project_imports(static_data_manager)
        self._create_managers(static_data_manager, server_manager, password)
        
    #
    def _create_managers(self, static_data_manager, server_manager, password):
        self.linguamatics_i2e_manager = \
            Linguamatics_i2e_manager(static_data_manager, server_manager,
                                     password)
        self.metadata_manager = Metadata_manager(static_data_manager)
        
        static_data = static_data_manager.get_static_data()
        directory_manager = static_data['directory_manager']
        save_dir = \
            directory_manager.pull_directory('processing_data_dir')
            
        save_dir_tmp = re.sub('/production$', '/test', save_dir)
        project_name = static_data['project_name']
        filename = \
            os.path.join(save_dir_tmp, project_name + '.performance.json')
        performance_json_manager = \
            Json_manager(static_data_manager, filename)
        
        project_name = static_data['project_name']
        directory_manager = static_data['directory_manager']
        data_dir = directory_manager.pull_directory('processing_data_dir')
        filename = os.path.join(data_dir, project_name + '.json')
        project_json_manager = \
            Json_manager(static_data_manager, filename)
            
        self.process_manager = Process_manager(static_data_manager,
                                               self.linguamatics_i2e_manager,
                                               self.metadata_manager,
                                               server_manager, 
                                               performance_json_manager,
                                               project_json_manager, password)
            
        try:
            self.performance_data_manager = \
                Performance_data_manager(static_data_manager,
                                         performance_json_manager,
                                         project_json_manager)
            print('Performance_data_manager: ' + project_name + '_performance_data_manager')
        except Exception as e:
            print(e)
            self.performance_data_manager = None

    #
    def _get_metadata_values(self):
        metadata_json_file = self.metadata_manager.get_metadata_json_file()
        metadata = read_json_file(metadata_json_file)
        num_documents = len(metadata.keys())
        document_values = []
        patient_values = []
        date_values = []
        for key0 in metadata.keys():
            for key1 in metadata[key0]['METADATA'].keys():
                if key1 in self.static_data['datetime_identifiers'].keys():
                    date_str = metadata[key0]['METADATA'][key1]
                    date_num = \
                        datetime2matlabdn(datetime.strptime(date_str,
                                                            self.static_data['datetime_identifiers'][key1]))
                    date_values.append(date_num)
                if key1 in self.static_data['document_identifiers']:
                    document_values.append(metadata[key0]['METADATA'][key1])
                if key1 in self.static_data['patient_identifiers']:
                    patient_values.append(metadata[key0]['METADATA'][key1])
        document_values = list(set(document_values))
        patient_values = list(set(patient_values))
        date_values.sort()
        patient_values.sort()
        return document_values, patient_values, date_values
    
    #
    def _project_imports(self, static_data_manager):
        static_data = static_data_manager.get_static_data()
        project_name = static_data['project_name']
        import_cmd = 'from projects_lib.' + project_name + '.py.' + \
                     project_name.lower() + \
                     '_performance_data_manager_class import ' + project_name + \
                     '_performance_data_manager as Performance_data_manager'
        try:
            exec(import_cmd, globals())
        except Exception as e:
            print(e)
            
        
    #
    def _quality_control(self):
        document_values, patient_values, date_values = \
            self._get_metadata_values()
        num_documents = len(list(set(document_values)))
        num_days = round(date_values[-1] - date_values[0])
        num_patients = len(patient_values)
        plt.hist(date_values, bins=num_days)
        print('number of documents: %d' % num_documents)
        print('number of patients: %d' % num_patients)
        
    #
    def calculate_performance(self):
        if self.performance_data_manager is not None:
            self.performance_data_manager.get_performance_data()
            self.performance_data_manager.display_performance_data()
            self.performance_data_manager.write_performance_data()
        
    #
    def download_queries(self):
        self.process_manager.download_queries()
        
    #
    def fix_linguamatics_i2e_queries(self):
        self.linguamatics_i2e_manager.fix_queries()
        
    #
    def generate_training_data_sets(self, password):
        doc_fraction = self.static_data['document_fraction']
        num_groups = 4
        self.process_manager.preprocessor(password, 0, False,
                                          preprocess_files_flg=False)
        document_values, patient_values, date_values = \
            self._get_metadata_values()
        num_documents = len(document_values)
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
    def postqueries_postperformance(self):
        self.process_manager.postperformance()
            
    #
    def postqueries_preperformance(self):
        self.process_manager.postprocessor()
        self.process_manager.preperformance()
            
    #
    def prequeries(self, password, preprocessor_start_idx=0,
                   preprocessor_cleanup_flg=True):
        if preprocessor_start_idx >= 0:
            if preprocessor_start_idx > 0:
                preprocessor_cleanup_flg = False
            self.process_manager.preprocessor(password, 
                                              preprocessor_start_idx, 
                                              preprocessor_cleanup_flg)
            #self._quality_control()
        self.process_manager.preindexer()
        self.process_manager.indexer()
        self.process_manager.postindexer()