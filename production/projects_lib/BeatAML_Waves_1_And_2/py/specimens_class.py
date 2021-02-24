# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 08:56:27 2019

@author: haglers
"""

#
import json
import os

#
from nlp_lib.py.tool_lib.query_tools_lib.blasts_tools import get_blast_value
from nlp_lib.py.tool_lib.processing_tools_lib.file_processing_tools import read_json_file
from nlp_lib.py.tool_lib.analysis_tools_lib.text_analysis_tools import prune_surface_antigens
from projects_lib.BeatAML_Waves_1_And_2.py.specimens_lib.specimens_jsons_class \
    import Specimens_jsons

#
class Specimens(Specimens_jsons):
    
    #
    def __init__(self, directory_manager, nlp_data):
        self.deidentifier_xlsx = directory_manager.pull_directory('raw_data_dir') + \
            '/manuscript OHSU MRNs.xlsx'
        Specimens_jsons.__init__(self, directory_manager, nlp_data)
    
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
                        diagnoses = data_json_tmp[key0][key1][key2]['specificDx']
                        diagnoses = self._trim_data_value(diagnoses)
                        diagnoses = list(set(diagnoses))
                        if len(diagnoses) == 1:
                            value = diagnoses[0]
                        elif len(diagnoses) > 1:
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
        data_out = self._get_data_value(data_in, data_out, [ 'ANTIBODIES TESTED' ], 'ANTIBODIES TESTED TEXT', 'Antibodies.Tested')
        data_out = self._get_data_value(data_in, data_out, [ 'SUMMARY', 'BONE MARROW DIFFERENTIAL', 'BONE MARROW ASPIRATE' ], 'BONE MARROW BLAST VALUE', '%.Blasts.in.BM')
        data_out = self._get_data_value(data_in, data_out, [ 'SUMMARY', 'COMMENT' ], 'DIAGNOSIS VALUE', 'dx')
        data_out = self._get_data_value(data_in, data_out, [ 'HISTORY', 'COMMENT', 'SUMMARY' ], 'DIAGNOSIS DATE VALUE', 'dx.Date')
        data_out = self._get_data_value(data_in, data_out, [ 'SUMMARY', 'COMMENT' ], 'EXTRAMEDULLARY DISEASE TEXT', 'Extramedullary.dx')
        data_out = self._get_data_value(data_in, data_out, [ 'COMMENT', 'BONE MARROW' ], 'FAB CLASSIFICATION VALUE', 'FAB/Blast.Morphology')
        data_out = self._get_data_value(data_in, data_out, [ 'FISH ANALYSIS SUMMARY' ], 'FISH ANALYSIS SUMMARY TEXT', 'FISH.Analysis.Summary')
        data_out = self._get_data_value(data_in, data_out, [ 'KARYOTYPE', 'IMPRESSIONS AND RECOMMENDATIONS' ], 'KARYOTYPE TEXT', 'Karyotype')
        data_out = self._get_data_value(data_in, data_out, [ 'HISTORY', 'COMMENT', 'SUMMARY' ], 'RELAPSE DATE VALUE', 'Relapse.Date')
        data_out = self._get_data_value(data_in, data_out, [ 'SUMMARY', 'PERIPHERAL BLOOD' ], 'PERIPHERAL BLOOD BLAST VALUE', '%.Blasts.in.PB')
        data_out = self._get_data_value(data_in, data_out, [ 'SUMMARY', 'COMMENT' ], 'RESIDUAL DISEASE TEXT', 'Residual.dx')
        data_out = self._get_data_value(data_in, data_out, [ 'SUMMARY', 'COMMENT' ], 'SPECIFIC DIAGNOSIS TEXT', 'specificDx')
        data_out = self._get_data_value(data_in, data_out, [ 'SUMMARY', 'COMMENT' ], 'SURFACE ANTIGENS TEXT', 'Surface.Antigens.(Immunohistochemical.Stains)')
        if not data_out:
            data_out = None
        return data_out

    #
    def _read_data(self, nlp_data):
        data_json = {}
        for key in nlp_data.keys():
            json_tmp = nlp_data[key]
            doc_name = str(key)
            mrn = json_tmp[self.metadata_key]['MRN']
            preprocessed_text = json_tmp[self.nlp_source_text_key]
            proc_nm = json_tmp[self.metadata_key]['PROC_NM']
            result_date = json_tmp[self.metadata_key]['RESULT_COMPLETED_DT']
            specimen_date = json_tmp[self.metadata_key]['SPECIMEN_COLL_DT']
            data_in = json_tmp[self.nlp_data_key]
            data_out = self._process_data(data_in)
            if data_out is not None:
                doc_label = ''
                if 'bone marrow' in preprocessed_text.lower():
                    doc_label += 'BLD'
                elif 'peripheral blood' in preprocessed_text.lower():
                    doc_label += 'BLD'
                if 'CSF' in preprocessed_text:
                    doc_label += 'CSF'
                if doc_label == '':
                    doc_label = 'NA'
                if mrn not in data_json:
                    data_json[mrn] = {}
                if specimen_date not in data_json[mrn]:
                    data_json[mrn][specimen_date] = {}
                if proc_nm not in data_json[mrn][specimen_date]:
                    data_json[mrn][specimen_date][proc_nm] = {}
                if doc_name not in data_json[mrn][specimen_date][proc_nm].keys():
                    data_json[mrn][specimen_date][proc_nm][doc_name + '_' + doc_label + '_' + result_date] = data_out
        return data_json