# -*- coding: utf-8 -*-
"""
Created on Mon Mar 04 12:29:38 2019

@author: haglers
"""

#
import os
import re

#
from nlp_pipeline_lib.performance_data_lib.performance_data_manager_class \
    import Performance_data_manager
from projects_lib.BeatAML_Waves_1_And_2.py.beataml_waves_1_and_2_specimens_manager_class \
    import BeatAML_Waves_1_And_2_specimens_manager as Specimens_manager
from tool_lib.py.query_tools_lib.antigens_tools \
    import antibodies_tested_performance
from tool_lib.py.query_tools_lib.diagnosis_tools \
    import diagnosis_performance
from tool_lib.py.query_tools_lib.diagnosis_date_tools \
    import diagnosis_date_performance
from tool_lib.py.query_tools_lib.extramedullary_disease_tools \
    import extramedullary_disease_performance
from tool_lib.py.query_tools_lib.fab_classification_tools \
    import fab_classification_performance
from tool_lib.py.query_tools_lib.fish_analysis_summary_tools \
    import fish_analysis_summary_performance
from tool_lib.py.query_tools_lib.immunophenotype_tools \
    import surface_antigens_performance
from tool_lib.py.query_tools_lib.karyotype_tools import karyotype_performance
from tool_lib.py.query_tools_lib.relapse_date_tools \
    import relapse_date_performance
from tool_lib.py.query_tools_lib.residual_disease_tools \
    import residual_disease_performance
from tool_lib.py.query_tools_lib.specific_diagnosis_tools \
    import specific_diagnosis_performance
from tool_lib.py.query_tools_lib.base_lib.blasts_tools_base \
    import blast_performance
from tool_lib.py.query_tools_lib.base_lib.date_tools_base import compare_dates

#
class BeatAML_Waves_1_And_2_performance_data_manager(Performance_data_manager):
    
    #
    def __init__(self, static_data_manager, evaluation_manager,
                 json_manager_registry, metadata_manager,
                 xls_manager_registry):
        Performance_data_manager.__init__(self, static_data_manager,
                                          evaluation_manager,
                                          json_manager_registry,
                                          metadata_manager,
                                          xls_manager_registry)
        static_data = self.static_data_manager.get_static_data()
        if static_data['project_subdir'] == 'test':
            self.identifier_key = 'MRN'
            self.identifier_list = static_data['patient_list']
            self.queries = static_data['queries_list']
        
    #
    def _generate_nlp_performance(self, nlp_performance_dict, labId, nlp_values,
                                  nlp_datum_key, validation_datum_key):
        performance = None
        if validation_datum_key == '%.Blasts.in.BM' or\
           validation_datum_key == '%.Blasts.in.PB':
            performance = blast_performance(self.validation_data_manager,
                                            self.evaluation_manager,
                                            labId, nlp_values, nlp_datum_key, 
                                            validation_datum_key)
        elif validation_datum_key == 'Antibodies.Tested':
            performance = antibodies_tested_performance(self.validation_data_manager,
                                                        self.evaluation_manager,
                                                        labId, nlp_values,
                                                        nlp_datum_key, 
                                                        validation_datum_key)
        elif validation_datum_key == 'Extramedullary.dx':
            performance = extramedullary_disease_performance(self.validation_data_manager,
                                                             self.evaluation_manager,
                                                             labId, nlp_values,
                                                             nlp_datum_key, 
                                                             validation_datum_key)
        elif validation_datum_key == 'FAB/Blast.Morphology':
            display_flg = True
            performance = fab_classification_performance(self.validation_data_manager,
                                                         self.evaluation_manager,
                                                         labId, nlp_values,
                                                         nlp_datum_key, 
                                                         validation_datum_key,
                                                         display_flg)
        elif validation_datum_key == 'FISH.Analysis.Summary':
            performance = fish_analysis_summary_performance(self.validation_data_manager,
                                                            self.evaluation_manager,labId,
                                                            nlp_values,
                                                            nlp_datum_key, 
                                                            validation_datum_key)
        elif validation_datum_key == 'Karyotype':
            performance = karyotype_performance(self.validation_data_manager,
                                                self.evaluation_manager,
                                                labId, nlp_values,
                                                nlp_datum_key, 
                                                validation_datum_key)
        elif validation_datum_key == 'Relapse.Date':
            performance = relapse_date_performance(self.validation_data_manager,
                                                   self.evaluation_manager,
                                                   labId, nlp_values,
                                                   nlp_datum_key, 
                                                   validation_datum_key)
        elif validation_datum_key == 'Residual.dx':
            performance = residual_disease_performance(self.validation_data_manager,
                                                       self.evaluation_manager,
                                                       labId, nlp_values,
                                                       nlp_datum_key, 
                                                       validation_datum_key)
        elif validation_datum_key == 'Surface.Antigens.(Immunohistochemical.Stains)':
            performance = surface_antigens_performance(self.validation_data_manager,
                                                       self.evaluation_manager,
                                                       labId, nlp_values,
                                                       nlp_datum_key, 
                                                       validation_datum_key)
        elif validation_datum_key == 'dxAtSpecimenAcquisition':
            performance = diagnosis_performance(self.validation_data_manager,
                                                self.evaluation_manager,
                                                labId, nlp_values,
                                                nlp_datum_key, 
                                                validation_datum_key)
        elif validation_datum_key == 'dx.Date':
            performance = diagnosis_date_performance(self.validation_data_manager,
                                                     self.evaluation_manager,
                                                     labId, nlp_values,
                                                     nlp_datum_key, 
                                                     validation_datum_key)
        elif validation_datum_key == 'specificDxAtAcquisition':
            display_flg = True
            performance = specific_diagnosis_performance(self.validation_data_manager,
                                                         self.evaluation_manager,
                                                         labId, nlp_values,
                                                         nlp_datum_key, 
                                                         validation_datum_key,
                                                         display_flg)
        if performance is not None:
            nlp_performance_dict[validation_datum_key].append(performance)
        return nlp_performance_dict
            
    #
    def _get_nlp_values(self, nlp_data, data_json):
        static_data = self.static_data_manager.get_static_data()
        metadata_keys, metadata_dict_dict = self._read_metadata(nlp_data)
        validation_object = Specimens_manager(static_data, metadata_dict_dict, data_json)
        validation_object.generate_json_file(self.directory_manager.pull_directory('log_dir'), 'validation.json')
        nlp_values = validation_object.get_data_json()
        return nlp_values
    
    #
    def _get_validation_idx(self, validation_data_manager, validation_datum_key):
        column_labels = validation_data_manager.column_labels()
        validation_idx_list = \
            [k for k in range(len(column_labels)) \
             if column_labels[k] == validation_datum_key]
        if len(validation_idx_list) > 0:
            validation_idx = validation_idx_list[0]
        else:
            validation_idx = None
        return validation_idx
    
    #
    def _process_performance(self, nlp_values_in):
        document_csn_list = \
            self.metadata_manager.pull_document_identifier_list('SOURCE_SYSTEM_DOCUMENT_ID')
        nlp_performance_wo_validation_manual_review_dict = {}
        nlp_performance_w_validation_manual_review_dict = {}
        wo_validation_manual_review_dict = {}
        wo_nlp_manual_review_dict = {}
        for i in range(len(self.queries)):
            validation_datum_key = self.queries[i][0]
            nlp_performance_wo_validation_manual_review_dict[validation_datum_key] = []
            nlp_performance_w_validation_manual_review_dict[validation_datum_key] = []
            wo_validation_manual_review_dict[validation_datum_key] = 0
            wo_nlp_manual_review_dict[validation_datum_key] = 0
        validation_datum_keys = []
        for query in self.queries:
            validation_datum_keys.append(query[0])
        nlp_values = \
            self._identify_manual_review(nlp_values_in, validation_datum_keys)
        N_manual_review = {}
        hit_documents_dict = {}
        hit_manual_review_dict = {}
        patientIds = nlp_values.keys()
        patientIds = list(set(patientIds))
        N_documents = 0
        for patientId in patientIds:
            if patientId in nlp_values_in:
                nlp_values = nlp_values_in[patientId]
            else:
                nlp_values = {}
            labIds = []
            labIds.extend(nlp_values.keys())
            for labId in labIds:
                print(labId)
                N_documents += 1
                for i in range(len(self.queries)):
                    nlp_datum_key = self.queries[i][0]
                    if nlp_datum_key not in N_manual_review.keys():
                        N_manual_review[nlp_datum_key] = 0
                    if nlp_datum_key not in hit_documents_dict.keys():
                        hit_documents_dict[nlp_datum_key] = []
                    if nlp_datum_key not in hit_manual_review_dict.keys():
                        hit_manual_review_dict[nlp_datum_key] = []
                    validation_datum_key = self.queries[i][0]
                    for j in range(1, self.validation_data_manager.length()):
                        row = self.validation_data_manager.row(j)
                        if row[0] == labId:
                            validation_value = self._process_validation_item(j, validation_datum_key)
                    if validation_value is not None and self.manual_review in validation_value:
                        N_manual_review[nlp_datum_key] += 1
                    if labId in nlp_values.keys() and nlp_values[labId] is not None:
                        if labId in nlp_values.keys():
                            if nlp_datum_key in nlp_values[labId].keys():
                                nlp_value = nlp_values[labId][nlp_datum_key]
                            else:
                                nlp_value = None
                        else:
                            nlp_value = None
                        if nlp_value is not None:
                            hit_documents_dict[nlp_datum_key].append(labId)
                            if validation_value is not None and self.manual_review in validation_value:
                                hit_manual_review_dict[nlp_datum_key].append(labId)
                        if not ( validation_value is not None and self.manual_review in validation_value ):
                            nlp_performance_wo_validation_manual_review_dict = \
                                self._generate_nlp_performance(nlp_performance_wo_validation_manual_review_dict,
                                                               labId, nlp_values, nlp_datum_key,
                                                               validation_datum_key)
                        else:
                            nlp_performance_w_validation_manual_review_dict = \
                                self._generate_nlp_performance(nlp_performance_w_validation_manual_review_dict,
                                                               labId, nlp_values, nlp_datum_key,
                                                               validation_datum_key)
                    else:
                        if validation_value == None:
                            nlp_performance_wo_validation_manual_review_dict[nlp_datum_key].append('true negative')
                        elif self.manual_review in validation_value:
                            nlp_performance_w_validation_manual_review_dict[nlp_datum_key].append('false negative')
                            print('false negative')
                            print(None)
                            print(validation_value)
                            print('')
                        else:
                            nlp_performance_wo_validation_manual_review_dict[nlp_datum_key].append('false negative')
                            print('false negative')
                            print(None)
                            print(validation_value)
                            print('')
        N_hit_documents_wo_validation_manual_review_dict = {}
        for key in hit_documents_dict.keys():
            N_hit_documents_wo_validation_manual_review_dict[key] = \
                len(list(set(hit_documents_dict[key])))
        N_hit_documents_w_validation_manual_review_dict = {}
        for key in hit_manual_review_dict.keys():
            N_hit_documents_w_validation_manual_review_dict[key] = \
                len(list(set(hit_manual_review_dict[key])))
        self._generate_performance_statistics(nlp_performance_wo_validation_manual_review_dict,
                                              nlp_performance_w_validation_manual_review_dict,
                                              N_documents, N_manual_review,
                                              N_hit_documents_wo_validation_manual_review_dict,
                                              N_hit_documents_w_validation_manual_review_dict)
        
    #
    def _process_validation_item(self, row_idx, validation_datum_key):
        row = self.validation_data_manager.row(row_idx)
        validation_idx = \
            self._get_validation_idx(self.validation_data_manager,
                                     validation_datum_key)
        if validation_idx is not None:
            x = row[validation_idx]
            if x == '':
                x = None
        else:
            x = None
        return x
            
    #
    def _read_nlp_value(self, nlp_data, data_json, key, identifier):
        doc_name = str(key)
        preprocessed_text = nlp_data[key][self.nlp_source_text_key]
        if 'PROC_NM' in nlp_data[key][self.metadata_key].keys():
            proc_nm = nlp_data[key][self.metadata_key]['PROC_NM']
        else:
            proc_nm = nlp_data[key][self.metadata_key]['PROC_NAME']
        result_date = nlp_data[key][self.metadata_key]['RESULT_COMPLETED_DT']
        specimen_date = nlp_data[key][self.metadata_key]['SPECIMEN_COLL_DT']
        data_in = nlp_data[key][self.nlp_data_key]
        data_out = self._get_nlp_data(data_in, self.queries)
        if data_out is not None:
            for key in data_out:
                data_out[key] = [ data_out[key] ]
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
            if identifier not in data_json:
                data_json[identifier] = {}
            if specimen_date not in data_json[identifier]:
                data_json[identifier][specimen_date] = {}
            if proc_nm not in data_json[identifier][specimen_date]:
                data_json[identifier][specimen_date][proc_nm] = {}
            if doc_name not in data_json[identifier][specimen_date][proc_nm].keys():
                data_json[identifier][specimen_date][proc_nm][doc_name + '_' + doc_label + '_' + result_date] = data_out
        return data_json