# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 08:56:27 2019

@author: haglers
"""

#
import json
import os
import xlrd

#
from nlp_pipeline_lib.specimens_lib.specimens_manager_class \
    import Specimens_manager
from tool_lib.py.processing_tools_lib.file_processing_tools \
    import read_json_file
from tool_lib.py.query_tools_lib.antigens_tools \
    import evaluate_antibodies_tested
from tool_lib.py.query_tools_lib.antigens_tools \
    import evaluate_surface_antigens
from tool_lib.py.query_tools_lib.bone_marrow_blast_tools \
    import evaluate_bone_marrow_blast
from tool_lib.py.query_tools_lib.diagnosis_tools \
    import evaluate_diagnosis
from tool_lib.py.query_tools_lib.peripheral_blood_blast_tools \
    import evaluate_peripheral_blood_blast
from tool_lib.py.query_tools_lib.specific_diagnosis_tools \
    import evaluate_specific_diagnosis
from tool_lib.py.query_tools_lib.base_lib.date_tools_base \
    import get_date_difference

#
class BeatAML_Waves_1_And_2_specimens_manager(Specimens_manager):
    
    #
    def __init__(self, static_data, metadata_dict_dict, data_json):
        self.metadata_dict_dict = metadata_dict_dict
        directory_manager = static_data['directory_manager']
        self.deidentifier_xlsx = directory_manager.pull_directory('raw_data_dir') + \
            '/manuscript OHSU MRNs.xlsx'
        Specimens_manager.__init__(self, static_data, data_json)
        
    #
    def _cluster_specimens(self, specimen_tree_in):
        deidentifier_key_dict = self._get_deidentifier_keys()
        specimen_dict = {}
        for key0 in specimen_tree_in.keys():
            if key0 in deidentifier_key_dict.keys():
                if key0 not in specimen_dict.keys():
                    specimen_dict[key0] = {}
                labid_dict = deidentifier_key_dict[key0]['labIds']
                for key1 in labid_dict.keys():
                    if key1 not in specimen_dict[key0].keys():
                        specimen_dict[key0][key1] = {}
                    for key2 in specimen_tree_in[key0].keys():
                        documents = specimen_tree_in[key0][key2]
                        for document in documents:
                            proc_nm = self.metadata_dict_dict[document.split('_')[0]]['METADATA']['PROC_NM']
                            for document in documents:
                                if self.metadata_dict_dict[document.split('_')[0]]['METADATA']['PROC_NM'] == proc_nm:
                                    doc_label = document.split('_')[1]
                                    lower_bound_days, upper_bound_days = self._get_days_window(proc_nm)
                                    date_diff = get_date_difference(key2, key1)
                                    if ( lower_bound_days <= date_diff ) and ( date_diff <= upper_bound_days ):
                                        process_label = self._get_process_label(proc_nm, doc_label)
                                        if process_label not in specimen_dict[key0][key1].keys():
                                            specimen_dict[key0][key1][process_label] = []
                                        specimen_dict[key0][key1][process_label].append([date_diff, document])
        return specimen_dict
    
    #
    def _evaluate_features(self):
        self.data_json = evaluate_antibodies_tested(self.data_json)
        self.data_json = evaluate_bone_marrow_blast(self.data_json)
        self.data_json = evaluate_diagnosis(self.data_json)
        self.data_json = self._evaluate_generic('dx.Date', self.data_json)
        self.data_json = self._evaluate_generic('Extramedullary.dx', self.data_json)
        self.data_json = self._evaluate_generic('FAB/Blast.Morphology', self.data_json)
        self.data_json = self._evaluate_generic('FISH.Analysis.Summary', self.data_json)
        #self.data_json = self._evaluate_generic('Karyotype', self.data_json)
        self.data_json = evaluate_peripheral_blood_blast(self.data_json)
        self.data_json = self._evaluate_generic('Relapse.Date', self.data_json)
        self.data_json = self._evaluate_generic('Residual.dx', self.data_json)
        self.data_json = evaluate_specific_diagnosis(self.data_json)
        #self.data_json = evaluate_surface_antigens('Surface.Antigens.(Immunohistochemical.Stains)', self.data_json)
                    
    #
    def _get_days_window(self, label):
        if 'chromosome' in label.lower() or \
           'cytogenetics' in label.lower():
            upper_bound_days = 7
            lower_bound_days = -36525
        else:
            upper_bound_days = 2
            lower_bound_days = -2
        return lower_bound_days, upper_bound_days
    
    #
    def _get_deidentifier_keys(self):
        deidentifier_key_dict = {}
        book = xlrd.open_workbook(self.deidentifier_xlsx)
        sheet = book.sheet_by_index(0)
        patientids = sheet.col_values(0)[1:]
        mrns = sheet.col_values(1)[1:]
        labids = sheet.col_values(2)[1:]
        specimen_dates = self._make_strings(sheet.col_values(3)[1:])
        for mrn in list(set(mrns)):
            idxs = [ i for i, j in enumerate(mrns) if j == mrn ]
            patientid_tmp = list(set([ patientids[i] for i in idxs ]))
            for i in range(len(patientid_tmp)):
                patientid_tmp[i] = int(patientid_tmp[i])
            tmp_list = [ [labids[i], specimen_dates[i]] for i in idxs ]
            doc_dict = {}
            for item in tmp_list:
                doc_dict[item[1]] = item[0]
            if len(patientid_tmp) == 1:
                deidentifier_key_dict[mrn] = {}
                deidentifier_key_dict[mrn]['patientId'] = str(patientid_tmp[0])
                deidentifier_key_dict[mrn]['labIds'] = doc_dict
        return deidentifier_key_dict
    
    #
    def _get_process_label(self, proc_nm, doc_label):
        if 'chromosome' in proc_nm.lower() or \
           'cytogenetics' in proc_nm.lower():
            process_label = 'cytogenetics_NA'
        else:
            process_label = 'hematopathology_' + doc_label
        return process_label