# -*- coding: utf-8 -*-
"""
Created on Mon Mar 04 12:29:38 2019

@author: haglers
"""

#
import re
from time import sleep

#
from nlp_lib.py.performance_data_lib.performance_data_manager_class \
    import Performance_data_manager
from projects_lib.BeatAML_Waves_1_And_2.py.specimens_class import Specimens
from projects_lib.BeatAML_Waves_1_And_2.py.gold_standard_jsons_class \
    import Gold_standard_jsons
from tool_lib.py.query_tools_lib.antigens_tools import extract_antigens
from tool_lib.py.query_tools_lib.date_tools import compare_dates

#
class BeatAML_Waves_1_And_2_performance_data_manager(Performance_data_manager):
    
    #
    def __init__(self, static_data_manager, performance_json_manager,
                 project_json_manager):
        Performance_data_manager.__init__(self, static_data_manager,
                                          performance_json_manager,
                                          project_json_manager)
        static_data = static_data_manager.get_static_data()
        self.static_data = static_data
        self.identifier_key = 'MRN'
        self.identifier_list = self.static_data['patient_list']
        self.queries = [ ('Antibodies.Tested', [ 'ANTIBODIES TESTED' ], 'ANTIBODIES_TESTED', 'ANTIBODIES_TESTED', 'multiple_values', True),
                         ('dx', [ 'SUMMARY', 'COMMENT', 'AMENDMENT COMMENT' ], 'DIAGNOSIS', 'DIAGNOSIS', 'multiple_values', True),
                         ('dx.Date', [ 'HISTORY', 'COMMENT', 'AMENDMENT COMMENT', 'SUMMARY' ], 'DIAGNOSIS_DATE', 'DATE', 'multiple_values', True),
                         ('Extramedullary.dx', [ 'SUMMARY', 'COMMENT', 'AMENDMENT COMMENT' ], 'EXTRAMEDULLARY_DISEASE', 'EXTRAMEDULLARY_DISEASE', 'multiple_values', True),
                         ('FAB/Blast.Morphology', [ 'COMMENT', 'AMENDMENT COMMENT', 'BONE MARROW' ], 'FAB_CLASSIFICATION', 'FAB_CLASSIFICATION', 'multiple_values', True),
                         ('FISH.Analysis.Summary', [ 'FISH ANALYSIS SUMMARY' ], 'FISH_ANALYSIS_SUMMARY', 'FISH_ANALYSIS_SUMMARY', 'multiple_values', True),
                         ('Karyotype', [ 'KARYOTYPE', 'IMPRESSIONS AND RECOMMENDATIONS' ], 'KARYOTYPE', 'KARYOTYPE', 'multiple_values', True),
                         ('%.Blasts.in.BM', [ 'SUMMARY', 'BONE MARROW DIFFERENTIAL', 'BONE MARROW ASPIRATE' ], 'BONE_MARROW_BLAST', 'BLAST_PERCENTAGE', 'multiple_values', True),
                         ('%.Blasts.in.PB', [ 'SUMMARY', 'PERIPHERAL BLOOD MORPHOLOGY' ], 'PERIPHERAL_BLOOD_BLAST', 'BLAST_PERCENTAGE', 'multiple_values', True),
                         ('Relapse.Date', [ 'HISTORY', 'COMMENT', 'AMENDMENT COMMENT', 'SUMMARY' ], 'RELAPSE_DATE', 'DATE', 'multiple_values', True),
                         ('Residual.dx', [ 'SUMMARY', 'COMMENT', 'AMENDMENT COMMENT' ], 'RESIDUAL_DISEASE', 'DIAGNOSIS', 'multiple_values', True),
                         ('specificDx', [ 'SUMMARY', 'COMMENT', 'AMENDMENT COMMENT' ], 'SPECIFIC_DIAGNOSIS', 'DIAGNOSIS', 'multiple_values', True),
                         ('Surface.Antigens.(Immunohistochemical.Stains)', [ 'SUMMARY', 'COMMENT', 'AMENDMENT COMMENT' ], 'IMMUNOPHENOTYPE', 'IMMUNOPHENOTYPE', 'multiple_values', True) ] 
        
        json_structure_manager = static_data['json_structure_manager']
        self.document_wrapper_key = \
            json_structure_manager.pull_key('document_wrapper_key')
        self.documents_wrapper_key = \
            json_structure_manager.pull_key('documents_wrapper_key')
        self.metadata_key = \
            json_structure_manager.pull_key('metadata_key')
        self.nlp_data_key = \
            json_structure_manager.pull_key('nlp_data_key')
        self.nlp_datetime_key = \
            json_structure_manager.pull_key('nlp_datetime_key')
        self.nlp_datum_key = \
            json_structure_manager.pull_key('nlp_datum_key')
        self.nlp_metadata_key = \
            json_structure_manager.pull_key('nlp_metadata_key')
        self.nlp_performance_key = \
            json_structure_manager.pull_key('nlp_performance_key')
        self.nlp_query_key = \
            json_structure_manager.pull_key('nlp_query_key')
        self.nlp_section_key = \
            json_structure_manager.pull_key('nlp_section_key')
        self.nlp_specimen_key = \
            json_structure_manager.pull_key('nlp_specimen_key')
        self.nlp_source_text_key = \
            json_structure_manager.pull_key('nlp_source_text_key')
        self.nlp_text_element_key = \
            json_structure_manager.pull_key('nlp_text_element_key')
        self.nlp_text_key = \
            json_structure_manager.pull_key('nlp_text_key')
        self.nlp_value_key = \
            json_structure_manager.pull_key('nlp_value_key')
            
        # to be moved to appropriate location
        self.manual_review = \
            json_structure_manager.pull_key('manual_review')
        #  
            
    #
    def _get_nlp_values(self, nlp_data, data_json, identifier_list):
        metadata_keys, metadata_dict_dict = self._read_metadata(nlp_data)
        validation_object = Specimens(self.static_data, metadata_dict_dict, data_json)
        validation_object.generate_json_file(self.directory_manager.pull_directory('log_dir'), 'validation.json')
        nlp_values = validation_object.get_data_json()
        return nlp_values
    
    #
    def _get_antibodies_tested_performance(self, labId, nlp_values,
                                           nlp_datum_key,
                                           validation_data, validation_datum_key):
        if labId in nlp_values.keys():
            keys0 = list(nlp_values[labId])
            if nlp_datum_key in nlp_values[labId][keys0[0]].keys():
                data_out = nlp_values[labId][keys0[0]][nlp_datum_key]
            else:
                data_out = None
        else:
            data_out = None
        if data_out is not None:
            if data_out == '':
                data_out = None
            data_out = re.sub('dim', 'dim ', data_out)
            data_out = re.sub('\+', ' +', data_out)
            data_out = re.sub('(?i)(-)?positive', ' +', data_out)
            data_out = extract_antigens(data_out)
            data_out = list(set(data_out))
        if data_out is not None:
            nlp_value = tuple(data_out)
        else:
            nlp_value = None
        if validation_datum_key in validation_data[labId].keys():
            validation_value = validation_data[labId][validation_datum_key]
            validation_value = re.sub('(?i)n/a', '', validation_value)
            validation_value = re.sub('(?i)not (available|run)', '', validation_value)
            if validation_value == '':
                validation_value = None
        else:
            validation_value = None
        if validation_value is not None:
            validation_value = re.sub('dim', 'dim ', validation_value)
            validation_value = re.sub('\+', ' +', validation_value)
            validation_value = re.sub('(?i)(-)?positive', ' +', validation_value)
            validation_value = extract_antigens(validation_value)
            validation_value = list(set(validation_value))
        if validation_value is not None:
            validation_value = tuple(validation_value)
        else:
            validation_value = None
        performance, flg = \
            self._compare_data_values(nlp_value, validation_value)
        return performance
    
    #
    def _get_blast_performance(self, labId, nlp_values, nlp_datum_key,
                               validation_data, validation_datum_key):
        if labId in nlp_values.keys():
            keys0 = list(nlp_values[labId])
            if nlp_datum_key in nlp_values[labId][keys0[0]].keys():
                data_out = nlp_values[labId][keys0[0]][nlp_datum_key]
            else:
                data_out = None
        else:
            data_out = None
        if data_out is not None:
            data_out = data_out.replace('~', '')
            data_out = data_out.replace('>', '')
            data_out = data_out.replace('<', '')
            data_out = data_out.replace('.0', '')
        if data_out is not None:
            nlp_value = []
            nlp_value.append(data_out)
        else:
            nlp_value = None
        nlp_value = self._nlp_to_tuple(nlp_value)
        if validation_datum_key in validation_data[labId].keys():
            validation_value = validation_data[labId][validation_datum_key]
            if validation_value == '':
                validation_value = None
        else:
            validation_value = None 
        if validation_value is not None:
            validation_value = validation_value.replace('~', '')
            validation_value = validation_value.replace('>', '')
            validation_value = validation_value.replace('<', '')
            validation_value = validation_value.replace('.0', '')
            validation_value = validation_value.replace('None', '0')
        validation_value = self._validation_to_tuple(validation_value)
        performance, flg = \
            self._compare_data_values(nlp_value, validation_value,
                                      value_range=5.0)
        return performance
    
    #
    def _get_diagnosis_performance(self, labId, nlp_values, nlp_datum_key,
                                   validation_data, validation_datum_key):
        if labId in nlp_values.keys():
            keys0 = list(nlp_values[labId])
            if nlp_datum_key in nlp_values[labId][keys0[0]].keys():
                data_out = nlp_values[labId][keys0[0]][nlp_datum_key]
            else:
                data_out = None
        if data_out is not None:
            data_out = \
                re.sub('SYNDROME(?!S)', 'SYNDROMES', data_out)
            data_out_tmp = data_out
            data_out = []
            data_out.append(data_out_tmp)
        if data_out is not None:
            nlp_value = tuple(data_out)
        else:
            nlp_value = None
        if validation_datum_key in validation_data[labId].keys():
            validation_value = validation_data[labId][validation_datum_key]
            validation_value = \
                re.sub('SYNDROME(?!S)', 'SYNDROMES', validation_value)
            if validation_value == '':
                validation_value = None
        else:
            validation_value = None
        if validation_value is not None:
            validation_value_tmp = validation_value
            validation_value = []
            validation_value.append(validation_value_tmp)
            validation_value = tuple(validation_value)
        performance, flg = \
            self._compare_data_values(nlp_value, validation_value)
        return performance
    
    #
    def _get_diagnosis_date_performance(self, labId, nlp_values, nlp_datum_key,
                                        validation_data, validation_datum_key):
        if labId in nlp_values.keys():
            keys0 = list(nlp_values[labId])
            if nlp_datum_key in nlp_values[labId][keys0[0]].keys():
                data_out = nlp_values[labId][keys0[0]][nlp_datum_key]
            else:
                data_out = None
        if data_out is not None:
            data_out = \
                re.sub('(?<=/)20(?=[0-9][0-9])', '', data_out)
            data_out = \
                re.sub('(?<=/)0(?=[0-9]/)', '', data_out)
            data_out_tmp = data_out
            data_out = []
            data_out.append(data_out_tmp)
        nlp_value = self._nlp_to_tuple(data_out)
        if validation_datum_key in validation_data[labId].keys():
            validation_value = validation_data[labId][validation_datum_key]
            validation_value = \
                re.sub('(?<=/)20(?=[0-9][0-9])', '', validation_value)
            validation_value = \
                re.sub('(?<=/)0(?=[0-9]/)', '', validation_value)
            if validation_value == '':
                validation_value = None
        else:
            validation_value = None
        validation_value = \
            self._validation_to_tuple(validation_value)
        performance, flg = \
            self._compare_data_values(nlp_value, validation_value)
        return performance
    
    #
    def _get_extramedullary_disease_performance(self, labId, nlp_values,
                                                nlp_datum_key, validation_data,
                                                validation_datum_key):
        if labId in nlp_values.keys():
            keys0 = list(nlp_values[labId])
            if nlp_datum_key in nlp_values[labId][keys0[0]].keys():
                data_out = nlp_values[labId][keys0[0]][nlp_datum_key]
            else:
                data_out = None
        if data_out is not None:
            data_out = re.sub('SYNDROME', 'SYNDROMES', data_out)
            data_out_tmp = data_out
            data_out = []
            data_out.append(data_out_tmp)
        nlp_value = self._nlp_to_tuple(data_out)
        if validation_datum_key in validation_data[labId].keys():
            validation_value = validation_data[labId][validation_datum_key]
            if validation_value == '':
                validation_value = None
        else:
            validation_value = None
        validation_value = self._validation_to_tuple(validation_value)
        performance, flg = \
            self._compare_data_values(nlp_value, validation_value)
        return performance
    
    #
    def _get_fab_classification_performance(self, labId, nlp_values,
                                            nlp_datum_key, validation_data,
                                            validation_datum_key):
        if labId in nlp_values.keys():
            keys0 = list(nlp_values[labId])
            if nlp_datum_key in nlp_values[labId][keys0[0]].keys():
                data_out = nlp_values[labId][keys0[0]][nlp_datum_key]
            else:
                data_out = None
        if data_out is not None:
            data_out = re.sub('SYNDROME', 'SYNDROMES', data_out)
            data_out_tmp = data_out
            data_out = []
            data_out.append(data_out_tmp)
        nlp_value = self._nlp_to_tuple(data_out)
        if validation_datum_key in validation_data[labId].keys():
            validation_value = validation_data[labId][validation_datum_key]
            if validation_value == '':
                validation_value = None
        else:
            validation_value = None
        validation_value = self._validation_to_tuple(validation_value)
        performance, flg = \
            self._compare_data_values(nlp_value, validation_value)
        return performance
    
    #
    def _get_fish_analysis_summary_performance(self, labId, nlp_values,
                                               nlp_datum_key, validation_data,
                                               validation_datum_key):
        if labId in nlp_values.keys():
            keys0 = list(nlp_values[labId])
            if nlp_datum_key in nlp_values[labId][keys0[0]].keys():
                data_out = nlp_values[labId][keys0[0]][nlp_datum_key]
            else:
                data_out = None
        else:
            data_out = None
        if data_out is not None:
            data_out_tmp = data_out
            data_out_tmp = \
                data_out_tmp.replace(' ', '')
            data_out = []
            data_out.append(data_out_tmp)
        if data_out is not None:
            nlp_value = tuple(data_out)
        else:
            nlp_value = None
        if validation_datum_key in validation_data[labId].keys():
            validation_value = validation_data[labId][validation_datum_key]
            if validation_value == '':
                validation_value = None
        else:
            validation_value = None
        if validation_value is not None:
            validation_value_tmp = validation_value
            validation_value_tmp = \
                validation_value_tmp.replace(' ', '')
            validation_value = []
            validation_value.append(validation_value_tmp)
        if validation_value is not None:
            validation_value = tuple(validation_value)
        performance, flg = \
            self._compare_data_values(nlp_value, validation_value)
        return performance
    
    #
    def _get_karyotype_performance(self, labId, nlp_values, nlp_datum_key,
                                   validation_data, validation_datum_key):
        if labId in nlp_values.keys():
            keys0 = list(nlp_values[labId])
            if nlp_datum_key in nlp_values[labId][keys0[0]].keys():
                data_out = nlp_values[labId][keys0[0]][nlp_datum_key]
            else:
                data_out = None
        else:
            data_out = None
        if data_out is not None:
            data_out = data_out.replace('//', '/')
            data_out_tmp = data_out
            data_out_tmp = \
                data_out_tmp.replace(' ', '')
            data_out = []
            data_out.append(data_out_tmp)
        if data_out is not None:
            nlp_value = tuple(data_out)
        else:
            nlp_value = None
        if validation_datum_key in validation_data[labId].keys():
            validation_value = validation_data[labId][validation_datum_key]
            validation_value = validation_value.replace('//', '/')
            if validation_value == '':
                validation_value = None
            if validation_value == 'N/A':
                validation_value = None
            if validation_value == 'Not available':
                validation_value = None
            if validation_value == 'None':
                validation_value = None
        else:
            validation_value = None
        if validation_value is not None:
            validation_value_tmp = validation_value
            validation_value_tmp = \
                validation_value_tmp.replace(' ', '')
            validation_value = []
            validation_value.append(validation_value_tmp)
        if validation_value is not None:
            validation_value = tuple(validation_value)
        performance, flg = \
            self._compare_data_values(nlp_value, validation_value)
        return performance
    
    #
    def _get_relapse_date_performance(self, labId, nlp_values, nlp_datum_key, 
                                      validation_data, validation_datum_key):
        if labId in nlp_values.keys():
            keys0 = list(nlp_values[labId])
            if nlp_datum_key in nlp_values[labId][keys0[0]].keys():
                data_out = nlp_values[labId][keys0[0]][nlp_datum_key]
            else:
                data_out = None
        else:
            data_out = None
        if data_out is not None:
            data_out = re.sub('(?<=/)20(?=[0-9][0-9])', '', data_out)
            data_out_tmp = data_out
            data_out = []
            data_out.append(data_out_tmp)
        nlp_value = self._nlp_to_tuple(data_out)
        if validation_datum_key in validation_data[labId].keys():
            validation_value = validation_data[labId][validation_datum_key]
            validation_value = \
                re.sub('(?<=/)20(?=[0-9][0-9])', '', validation_value)
            if validation_value == '':
                validation_value = None
        else:
            validation_value = None
        validation_value = self._validation_to_tuple(validation_value)
        performance, flg = \
            self._compare_data_values(nlp_value, validation_value)
        return performance
    
    #
    def _get_residual_disease_performance(self, labId, nlp_values, nlp_datum_key, 
                                          validation_data, validation_datum_key):
        if labId in nlp_values.keys():
            keys0 = list(nlp_values[labId])
            if nlp_datum_key in nlp_values[labId][keys0[0]].keys():
                data_out = nlp_values[labId][keys0[0]][nlp_datum_key]
            else:
                data_out = None
        else:
            data_out = None
        if data_out is not None:
            data_out = data_out.lower()
            data_out_tmp = data_out
            data_out = []
            data_out.append(data_out_tmp)
        nlp_value = self._nlp_to_tuple(data_out)
        if validation_datum_key in validation_data[labId].keys():
            validation_value = validation_data[labId][validation_datum_key]
            validation_value = re.sub('(?i)acute myeloid leukemia', 'AML', validation_value)
            validation_value = validation_value.lower()
            if validation_value == '':
                validation_value = None
        else:
            validation_value = None
        validation_value = self._validation_to_tuple(validation_value)
        performance, flg = \
            self._compare_data_values(nlp_value, validation_value)
        return performance
    
    #
    def _get_specific_diagnosis_performance(self, labId, nlp_values, nlp_datum_key, 
                                            validation_data, validation_datum_key):
        if labId in nlp_values.keys():
            keys0 = list(nlp_values[labId])
            if nlp_datum_key in nlp_values[labId][keys0[0]].keys():
                data_out = nlp_values[labId][keys0[0]][nlp_datum_key]
            else:
                data_out = None
        else:
            data_out = None
        if data_out is not None:
            data_out = re.sub('/', 'and', data_out)
            data_out = re.sub('monocytic and monoblastic', 'monoblastic and monocytic', data_out)
            data_out = re.sub(' ', '', data_out)
            data_out = data_out.lower()
        else:
            data_out = None
        if data_out is not None:
            data_out_tmp = data_out
            data_out = []
            data_out.append(data_out_tmp)
        if data_out is not None:
            nlp_value = tuple(data_out)
        else:
            nlp_value = None
        if validation_datum_key in validation_data[labId].keys():
            validation_value = validation_data[labId][validation_datum_key]
            validation_value = re.sub('(?i)acute myeloid leukemia', 'AML', validation_value)
            validation_value = re.sub('(?i)acute myelomonocytic leukemia', 'AMML', validation_value)
            validation_value = re.sub('monocytic and monoblastic', 'monoblastic and monocytic', validation_value)
            validation_value = re.sub(' ', '', validation_value)
            validation_value = validation_value.lower()
            if validation_value == '':
                validation_value = None
            elif validation_value[-1] == ',':
                validation_value = validation_value[:-1]
        else:
            validation_value = None
        if validation_value is not None:
            validation_value_tmp = validation_value
            validation_value = []
            validation_value.append(validation_value_tmp)
        if validation_value is not None:
            validation_specific_diagnosis_value = tuple(validation_value)
        else:
            validation_specific_diagnosis_value = None
            
        performance, flg = \
            self._compare_data_values(nlp_value, validation_value)
        return performance
    
    #
    def _get_surface_antigens_performance(self, labId, nlp_values, nlp_datum_key, 
                                          validation_data, validation_datum_key):
        if labId in nlp_values.keys():
            keys0 = list(nlp_values[labId])
            if nlp_datum_key in nlp_values[labId][keys0[0]].keys():
                data_out = nlp_values[labId][keys0[0]][nlp_datum_key]
                if data_out == '':
                    data_out = None
            else:
                data_out = None
        else:
            data_out = None
        if data_out is not None:
            if isinstance(data_out, list):
                data_out = self.manual_review
        if data_out is not None and \
           data_out is not self.manual_review:
            data_out = re.sub('dim', 'dim ', data_out)
            data_out = re.sub('\+', ' +', data_out)
            data_out = re.sub('(?i)(-)?positive', ' +', data_out)
            data_out = extract_antigens(data_out)
            data_out = list(set(data_out))
        if data_out is not None and \
           data_out is not self.manual_review:
            nlp_value = tuple(data_out)
        #elif data_out is None:
        else:
            nlp_value = None
        if labId in validation_data.keys():
            if validation_datum_key in validation_data[labId].keys():
                validation_value = validation_data[labId][validation_datum_key]
                validation_value = re.sub('(?i)n/a', '', validation_value)
                validation_value = re.sub('(?i)not (available|run)', '', validation_value)
                if validation_value == '':
                    validation_value = None
            else:
                validation_value = None
            if validation_value is not None:
                validation_value = re.sub('dim', 'dim ', validation_value)
                validation_value = re.sub('\+', ' +', validation_value)
                validation_value = re.sub('(?i)(-)?positive', ' +', validation_value)
                validation_value = extract_antigens(validation_value)
                validation_value = list(set(validation_value))
            if validation_value is not None:
                validation_value = \
                    tuple(validation_value)
            else:
                validation_value = None
        else:
            validation_value = None
        performance, flg = \
            self._compare_data_values(nlp_value, validation_value)
        return performance
    
    #
    def _process_performance(self, nlp_values_in, validation_data_in):
        #validation_csn_list = \
        #    self._get_validation_csn_list(validation_data)
        nlp_performance_dict = {}
        for i in range(len(self.queries)):
            validation_datum_key = self.queries[i][0]
            nlp_performance_dict[validation_datum_key] = []
        patientIds = nlp_values_in.keys()
        patientIds = list(set(patientIds))
        for patientId in patientIds:
            if patientId in nlp_values_in:
                nlp_values = nlp_values_in[patientId]
            else:
                nlp_values = {}
            if patientId in validation_data_in:
                validation_data = validation_data_in[patientId]
            else:
                validation_data = {}
            labIds = []
            labIds.extend(nlp_values.keys())
            for labId in labIds:
                print(labId)
                for i in range(len(self.queries)):
                    nlp_datum_key = self.queries[i][0]
                    validation_datum_key = self.queries[i][0]
                    if validation_datum_key == '%.Blasts.in.BM' or\
                       validation_datum_key == '%.Blasts.in.PB':
                        performance = self._get_blast_performance(labId, nlp_values,
                                                                  nlp_datum_key, 
                                                                  validation_data,
                                                                  validation_datum_key)
                    elif validation_datum_key == 'Antibodies.Tested':
                        performance = self._get_antibodies_tested_performance(labId,
                                                                              nlp_values,
                                                                              nlp_datum_key, 
                                                                              validation_data,
                                                                              validation_datum_key)
                    elif validation_datum_key == 'Extramedullary.dx':
                        performance = self._get_extramedullary_disease_performance(labId,
                                                                                   nlp_values,
                                                                                   nlp_datum_key, 
                                                                                   validation_data,
                                                                                   validation_datum_key)
                    elif validation_datum_key == 'FAB/Blast.Morphology':
                        performance = self._get_fab_classification_performance(labId,
                                                                               nlp_values,
                                                                               nlp_datum_key, 
                                                                               validation_data,
                                                                               validation_datum_key)
                    elif validation_datum_key == 'FISH.Analysis.Summary':
                        performance = self._get_fish_analysis_summary_performance(labId,
                                                                                  nlp_values,
                                                                                  nlp_datum_key, 
                                                                                  validation_data,
                                                                                  validation_datum_key)
                    elif validation_datum_key == 'Karyotype':
                        performance = self._get_karyotype_performance(labId, nlp_values,
                                                                      nlp_datum_key, 
                                                                      validation_data,
                                                                      validation_datum_key)
                        
                    elif validation_datum_key == 'Relapse.Date':
                        performance = self._get_relapse_date_performance(labId,
                                                                         nlp_values,
                                                                         nlp_datum_key, 
                                                                         validation_data,
                                                                         validation_datum_key)
                    elif validation_datum_key == 'Residual.dx':
                        performance = self._get_residual_disease_performance(labId,
                                                                             nlp_values,
                                                                             nlp_datum_key, 
                                                                             validation_data,
                                                                             validation_datum_key)
                    elif validation_datum_key == 'Surface.Antigens.(Immunohistochemical.Stains)':
                        performance = self._get_surface_antigens_performance(labId,
                                                                             nlp_values,
                                                                             nlp_datum_key, 
                                                                             validation_data,
                                                                             validation_datum_key)
                    elif validation_datum_key == 'dx':
                        performance = self._get_diagnosis_performance(labId,
                                                                      nlp_values,
                                                                      nlp_datum_key, 
                                                                      validation_data,
                                                                      validation_datum_key)
                    elif validation_datum_key == 'dx.Date':
                        performance = self._get_diagnosis_date_performance(labId,
                                                                           nlp_values,
                                                                           nlp_datum_key, 
                                                                           validation_data,
                                                                           validation_datum_key)
                    elif validation_datum_key == 'specificDx':
                        performance = self._get_specific_diagnosis_performance(labId,
                                                                               nlp_values,
                                                                               nlp_datum_key, 
                                                                               validation_data,
                                                                               validation_datum_key)
                    nlp_performance_dict[validation_datum_key].append(performance)
        patientIds = nlp_values_in.keys()
        patientIds = list(set(patientIds))
        N = 0
        for patientId in patientIds:
            if patientId in nlp_values_in:
                nlp_patient = nlp_values_in[patientId]
            else:
                nlp_patient = {}
            labIds = []
            labIds.extend(nlp_patient.keys())
            for labId in labIds:
                N += 1
        for key in nlp_performance_dict.keys():
            FN, FP, FP_plus_FN, TN, TP = \
                self._performance_values(nlp_performance_dict[key])
            self.performance_statistics_dict[key] = \
                self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
            
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
    
    #
    def _read_validation_data(self):
        mrn_list = self.static_data['patient_list']
        gold_standard_object = Gold_standard_jsons(self.directory_manager, mrn_list)
        gold_standard_object.generate_json_file(self.directory_manager.pull_directory('log_dir'), 'gold_standard.json')
        validation_data = gold_standard_object.get_data_json()
        return validation_data