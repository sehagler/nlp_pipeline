# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 08:56:27 2019

@author: haglers
"""

#
import json
import os

#
from tool_lib.py.processing_tools_lib.file_processing_tools import read_json_file
from nlp_lib.py.tool_lib.analysis_tools_lib.text_analysis_tools import prune_surface_antigens
from projects_lib.BeatAML_Waves_1_And_2.py.specimens_lib.specimens_jsons_class \
    import Specimens_jsons
from tool_lib.py.query_tools_lib.blasts_tools import get_blast_value

#
class Specimens(Specimens_jsons):
    
    #
    def __init__(self, project_data, nlp_data):
        directory_manager = project_data['directory_manager']
        self.deidentifier_xlsx = directory_manager.pull_directory('raw_data_dir') + \
            '/manuscript OHSU MRNs.xlsx'
        Specimens_jsons.__init__(self, project_data, nlp_data)
    
    #                 
    def _evaluate_antibodies_tested(self):
        data_json_tmp = self.data_json
        for key0 in data_json_tmp.keys():
            for key1 in data_json_tmp[key0].keys():
                for key2 in data_json_tmp[key0][key1].keys():
                    try:
                        diagnoses = data_json_tmp[key0][key1][key2]['Antibodies.Tested']
                        diagnoses = self._trim_data_value(diagnoses)
                        diagnoses = list(set(diagnoses))
                        if len(diagnoses) == 1:
                            value = diagnoses[0]
                        elif len(diagnoses) > 1:
                            value = self.multiple_values
                        else:
                            value = None
                        if value is not None:
                            self.data_json[key0][key1][key2]['Antibodies.Tested'] = value
                        else:
                            del self.data_json[key0][key1][key2]['Antibodies.Tested']
                    except:
                        pass
   
    #                 
    def _evaluate_bone_marrow_blast(self):
        data_json_tmp = self.data_json
        for key0 in data_json_tmp.keys():
            for key1 in data_json_tmp[key0].keys():
                for key2 in data_json_tmp[key0][key1].keys():
                    try:
                        blast_value_list = data_json_tmp[key0][key1][key2]['%.Blasts.in.BM']
                        blast_value_list = self._trim_data_value(blast_value_list)
                        value = get_blast_value(blast_value_list)
                        if value is not None:
                            self.data_json[key0][key1][key2]['%.Blasts.in.BM'] = value
                        else:
                            del self.data_json[key0][key1][key2]['%.Blasts.in.BM']
                    except:
                        pass
                    
    #
    def _evaluate_features(self):
        self._evaluate_antibodies_tested()
        self._evaluate_bone_marrow_blast()
        self._evaluate_generic('dx')
        self._evaluate_generic('dx.Date')
        self._evaluate_generic('Extramedullary.dx')
        self._evaluate_generic('FAB/Blast.Morphology')
        self._evaluate_generic('FISH.Analysis.Summary')
        self._evaluate_generic('Karyotype')
        self._evaluate_peripheral_blood_blast()
        self._evaluate_generic('Relapse.Date')
        self._evaluate_generic('Residual.dx')
        self._evaluate_specific_diagnosis()
        self._evaluate_surface_antigens()
        
    #
    def _evaluate_peripheral_blood_blast(self):
        data_json_tmp = self.data_json
        for key0 in data_json_tmp.keys():
            for key1 in data_json_tmp[key0].keys():
                for key2 in data_json_tmp[key0][key1].keys():
                    try:
                        blast_value_list = data_json_tmp[key0][key1][key2]['%.Blasts.in.PB']
                        blast_value_list = self._trim_data_value(blast_value_list)
                        value = get_blast_value(blast_value_list)
                        if value is not None:
                            self.data_json[key0][key1][key2]['%.Blasts.in.PB'] = value
                        else:
                            del self.data_json[key0][key1][key2]['%.Blasts.in.PB']
                    except:
                        pass
                        
    #                 
    def _evaluate_specific_diagnosis(self):
        data_json_tmp = self.data_json
        for key0 in data_json_tmp.keys():
            for key1 in data_json_tmp[key0].keys():
                for key2 in data_json_tmp[key0][key1].keys():
                    try:
                        values = data_json_tmp[key0][key1][key2]['specificDx'][0]
                        #values = self._trim_data_value(values)
                        #values = list(set(values))
                        specific_diagnoses = []
                        specific_diagnoses.append(''.join(values[0][1]))
                        if len(specific_diagnoses) == 1:
                            value = specific_diagnoses[0]
                        elif len(specific_diagnoses) > 1:
                            value = self.multiple_values
                        else:
                            value = None
                        if value is not None:
                            self.data_json[key0][key1][key2]['specificDx'] = value
                        else:
                            del self.data_json[key0][key1][key2]['specificDx']
                    except:
                        pass
                        
    #                 
    def _evaluate_surface_antigens(self):
        data_json_tmp = self.data_json
        for key0 in data_json_tmp.keys():
            for key1 in data_json_tmp[key0].keys():
                for key2 in data_json_tmp[key0][key1].keys():
                    try:
                        antigens = data_json_tmp[key0][key1][key2]['Surface.Antigens.(Immunohistochemical.Stains)']
                        antigens = self._trim_data_value(antigens)
                        antigens = prune_surface_antigens(antigens)
                        if len(antigens) == 1:
                            value = antigens[0]
                        elif len(antigens) > 1:
                            value = self.multiple_values
                        else:
                            value = None
                        if value is not None:
                            self.data_json[key0][key1][key2]['Surface.Antigens.(Immunohistochemical.Stains)'] = value
                        else:
                            del self.data_json[key0][key1][key2]['Surface.Antigens.(Immunohistochemical.Stains)']
                    except:
                        pass
                    
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
    def _get_process_label(self, proc_nm, doc_label):
        if 'chromosome' in proc_nm.lower() or \
           'cytogenetics' in proc_nm.lower():
            process_label = 'cytogenetics_NA'
        else:
            process_label = 'hematopathology_' + doc_label
        return process_label
                    
    #
    def _process_data(self, data_in):
        data_out = {}
        data_out = self._get_data_value(data_in, data_out, [ 'ANTIBODIES TESTED' ], 'ANTIBODIES_TESTED_' + self.nlp_value_key, 'Antibodies.Tested')
        data_out = self._get_data_value(data_in, data_out, [ 'SUMMARY', 'BONE MARROW DIFFERENTIAL', 'BONE MARROW ASPIRATE' ], 'BONE_MARROW_BLAST_' + self.nlp_value_key, '%.Blasts.in.BM')
        data_out = self._get_data_value(data_in, data_out, [ 'SUMMARY', 'COMMENT' ], 'DIAGNOSIS_' + self.nlp_value_key, 'dx')
        data_out = self._get_data_value(data_in, data_out, [ 'HISTORY', 'COMMENT', 'SUMMARY' ], 'DIAGNOSIS_DATE_' + self.nlp_value_key, 'dx.Date')
        data_out = self._get_data_value(data_in, data_out, [ 'SUMMARY', 'COMMENT' ], 'EXTRAMEDULLARY_DISEASE_' + self.nlp_value_key, 'Extramedullary.dx')
        data_out = self._get_data_value(data_in, data_out, [ 'COMMENT', 'BONE MARROW' ], 'FAB_CLASSIFICATION_' + self.nlp_value_key, 'FAB/Blast.Morphology')
        data_out = self._get_data_value(data_in, data_out, [ 'FISH ANALYSIS SUMMARY' ], 'FISH_ANALYSIS_SUMMARY_' + self.nlp_value_key, 'FISH.Analysis.Summary')
        data_out = self._get_data_value(data_in, data_out, [ 'KARYOTYPE', 'IMPRESSIONS AND RECOMMENDATIONS' ], 'KARYOTYPE_' + self.nlp_value_key, 'Karyotype')
        data_out = self._get_data_value(data_in, data_out, [ 'SUMMARY', 'PERIPHERAL BLOOD' ], 'PERIPHERAL_BLOOD_BLAST_' + self.nlp_value_key, '%.Blasts.in.PB')
        data_out = self._get_data_value(data_in, data_out, [ 'HISTORY', 'COMMENT', 'SUMMARY' ], 'RELAPSE_DATE_' + self.nlp_value_key, 'Relapse.Date')
        data_out = self._get_data_value(data_in, data_out, [ 'SUMMARY', 'COMMENT' ], 'RESIDUAL_DISEASE_' + self.nlp_value_key, 'Residual.dx')
        data_out = self._get_data_value(data_in, data_out, [ 'SUMMARY', 'COMMENT' ], 'SPECIFIC_DIAGNOSIS_' + self.nlp_value_key, 'specificDx')
        data_out = self._get_data_value(data_in, data_out, [ 'SUMMARY', 'COMMENT' ], 'SURFACE_ANTIGENS_' + self.nlp_value_key, 'Surface.Antigens.(Immunohistochemical.Stains)')
        if not data_out:
            data_out = None
        return data_out