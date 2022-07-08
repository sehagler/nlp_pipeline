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
from projects_lib.BeatAML_Waves_3_And_4.py.specimens_class import Specimens
from tool_lib.py.processing_tools_lib.text_processing_tools import substitution
from tool_lib.py.query_tools_lib.antigens_tools import extract_antigens
from tool_lib.py.query_tools_lib.base_lib.date_tools_base import compare_dates

#
class BeatAML_Waves_3_And_4_performance_data_manager(Performance_data_manager):
    
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
    def _cleanup_antigens(self, text):
        text = re.sub(',$', '', text)
        text = re.sub('\.', '', text)
        text = re.sub(':', ' : ', text)
        text = re.sub(',', ' , ', text)
        text = re.sub('\(', ' ( ', text)
        text = re.sub('\)', ' ) ', text)
        text = re.sub('\.', ' . ', text)
        text = re.sub(';', ' ; ', text)
        text = re.sub('/', ' / ', text)
        text = re.sub('HLA ?DR', 'HLA-DR', text)
        text = re.sub('(?i)dim(-| (/ )?)partial', 'dim/partial', text)
        text = re.sub('(?i)dim (/ )?variable', 'dim/variable', text)
        text = re.sub('(?i)(bright|dim|low|moderate|partial|subset|variable)CD', ' CD', text)
        text = re.sub('(?i)partial (/ )?dim', 'dim/partial', text)
        text = re.sub('(?i)myeloperoxidase( \(MPO\))?', 'MPO', text)
        text = substitution('([a-z]?CD[0-9]+|MPO|T[Dd]T) : ([a-z]?CD[0-9]+|MPO|T[Dd]T)',
                            {' : ' : ':'}, text)
        text = substitution('([a-z]?CD[0-9]+|HLA-DR|MPO|T[Dd]T) / ([a-z]?CD[0-9]+|HLA-DR|MPO|T[Dd]T)',
                            {' / ' : '/'}, text)
        text = substitution('([a-z]?CD[0-9]+|HLA-DR|MPO|T[Dd]T)-negative',
                            {'-negative' : ' negative'}, text)
        text = substitution('([a-z]?CD[0-9]+|HLA-DR|MPO|T[Dd]T)-positive',
                            {'-positive' : ' positive'}, text)
        text = substitution('([a-z]?CD[0-9]+|HLA-DR|MPO|T[Dd]T)-',
                            {'-' : ' negative '}, text)
        text = substitution('([a-z]?CD[0-9]+|HLA-DR|MPO|T[Dd]T)\+',
                            {'\+' : ' positive'}, text)
        text = substitution('([a-z]?CD[0-9]+|HLA-DR|MPO|T[Dd]T) \+',
                            {'\+' : ' positive'}, text)
        text = re.sub('(?<=HLA) (negative|positive)(?=DR)', '-', text)
        text = re.sub(' +', ' ', text)
        text = re.sub(' \n', '\n', text)
        text = re.sub(' $', '', text)
        return text
    
    #
    def _generate_nlp_performance(self, nlp_performance_dict, labId, nlp_values,
                                  nlp_datum_key, validation_datum_key):
        if validation_datum_key == '%.Blasts.in.BM' or\
           validation_datum_key == '%.Blasts.in.PB':
            performance = self._get_blast_performance(labId, nlp_values,
                                                      nlp_datum_key, 
                                                      validation_datum_key)
        elif validation_datum_key == 'Antibodies.Tested':
            performance = self._get_antibodies_tested_performance(labId,
                                                                  nlp_values,
                                                                  nlp_datum_key, 
                                                                  validation_datum_key)
        elif validation_datum_key == 'Extramedullary.dx':
            performance = self._get_extramedullary_disease_performance(labId,
                                                                       nlp_values,
                                                                       nlp_datum_key, 
                                                                       validation_datum_key)
        elif validation_datum_key == 'FAB/Blast.Morphology':
            performance = self._get_fab_classification_performance(labId,
                                                                   nlp_values,
                                                                   nlp_datum_key, 
                                                                   validation_datum_key)
        elif validation_datum_key == 'FISH.Analysis.Summary':
            performance = self._get_fish_analysis_summary_performance(labId,
                                                                      nlp_values,
                                                                      nlp_datum_key, 
                                                                      validation_datum_key)
        elif validation_datum_key == 'karyotype':
            performance = self._get_karyotype_performance(labId, nlp_values,
                                                          nlp_datum_key, 
                                                          validation_datum_key)
            
        elif validation_datum_key == 'Relapse.Date':
            performance = self._get_relapse_date_performance(labId,
                                                             nlp_values,
                                                             nlp_datum_key, 
                                                             validation_datum_key)
        elif validation_datum_key == 'Residual.dx':
            performance = self._get_residual_disease_performance(labId,
                                                                 nlp_values,
                                                                 nlp_datum_key, 
                                                                 validation_datum_key)
        elif validation_datum_key == 'surfaceAntigensImmunohistochemicalStains':
            performance = self._get_surface_antigens_performance(labId,
                                                                 nlp_values,
                                                                 nlp_datum_key, 
                                                                 validation_datum_key)
        elif validation_datum_key == 'dxAtSpecimenAcquisition':
            performance = self._get_diagnosis_performance(labId,
                                                          nlp_values,
                                                          nlp_datum_key, 
                                                          validation_datum_key)
        elif validation_datum_key == 'dx.Date':
            performance = self._get_diagnosis_date_performance(labId,
                                                               nlp_values,
                                                               nlp_datum_key, 
                                                               validation_datum_key)
        elif validation_datum_key == 'specificDxAtAcquisition':
            performance = self._get_specific_diagnosis_performance(labId,
                                                                   nlp_values,
                                                                   nlp_datum_key, 
                                                                   validation_datum_key)
        nlp_performance_dict[validation_datum_key].append(performance)
        return nlp_performance_dict
    
    #
    def _get_nlp_values(self, nlp_data, data_json):
        static_data = self.static_data_manager.get_static_data()
        metadata_keys, metadata_dict_dict = self._read_metadata(nlp_data)
        validation_object = Specimens(static_data, metadata_dict_dict, data_json)
        validation_object.generate_json_file(self.directory_manager.pull_directory('log_dir'), 'validation.json')
        nlp_values = validation_object.get_data_json()
        return nlp_values
    
    #
    def _get_antibodies_tested_performance(self, labId, nlp_values,
                                           nlp_datum_key,
                                           validation_datum_key):
        validation_data = \
            self.validation_data_manager.get_validation_data()
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
        labid_idx = validation_data[0].index('labId')
        validation_datum_idx = validation_data[0].index(validation_datum_key)
        validation_value = None
        for item in validation_data:
            if item[labid_idx] == labId:
                validation_value = item[validation_datum_idx]
        if validation_value is not None:
            validation_value = self._cleanup_antigens(validation_value)
            validation_value = re.sub('(?i)n/a', '', validation_value)
            validation_value = re.sub('(?i)not (available|run)', '', validation_value)
            if validation_value == '':
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
        display_flg = True
        performance = \
            self.evaluation_manager.evaluation(nlp_value, validation_value,
                                               display_flg)
        return performance
    
    #
    def _get_blast_performance(self, labId, nlp_values, nlp_datum_key,
                               validation_datum_key):
        validation_data = \
            self.validation_data_manager.get_validation_data()
        if labId in nlp_values.keys():
            keys0 = list(nlp_values[labId])
            if nlp_datum_key in nlp_values[labId][keys0[0]].keys():
                data_out = nlp_values[labId][keys0[0]][nlp_datum_key]
            else:
                data_out = None
        else:
            data_out = None
        if data_out is not None:
            print(data_out)
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
        labid_idx = validation_data[0].index('labId')
        validation_datum_idx = validation_data[0].index(validation_datum_key)
        validation_value = None
        for item in validation_data:
            if item[labid_idx] == labId:
                validation_value = item[validation_datum_idx]
        if validation_value is not None:
            if validation_value == '':
                validation_value = None
        if validation_value is not None:
            validation_value = validation_value.replace('~', '')
            validation_value = validation_value.replace('>', '')
            validation_value = validation_value.replace('<', '')
            validation_value = validation_value.replace('.0', '')
            validation_value = validation_value.replace('None', '0')
        validation_value = self._validation_to_tuple(validation_value)
        display_flg = True
        performance = \
            self.evaluation_manager.evaluation(nlp_value, validation_value,
                                               display_flg, value_range=5.0)
        return performance
    
    #
    def _get_diagnosis_performance(self, labId, nlp_values, nlp_datum_key,
                                   validation_datum_key):
        validation_data = \
            self.validation_data_manager.get_validation_data()
        if labId in nlp_values.keys():
            keys0 = list(nlp_values[labId])
            if nlp_datum_key in nlp_values[labId][keys0[0]].keys():
                data_out = nlp_values[labId][keys0[0]][nlp_datum_key][0][0]
            else:
                data_out = None
        if data_out is not None:
            data_out = re.sub('SYNDROME(?!S)', 'SYNDROMES', data_out)
            data_out_tmp = data_out
            data_out = []
            data_out.append(data_out_tmp)
        if data_out is not None:
            nlp_value = tuple(data_out)
        else:
            nlp_value = None
        labid_idx = validation_data[0].index('labId')
        validation_datum_idx = validation_data[0].index(validation_datum_key)
        validation_value = None
        for item in validation_data:
            if item[labid_idx] == labId:
                validation_value = item[validation_datum_idx]
        if validation_value is not None:
            validation_value = re.sub('LEUKAEMIA', 'LEUKEMIA', validation_value)
            validation_value = re.sub('leukaemia', 'leukemia', validation_value)
            validation_value = \
                re.sub('SYNDROME(?!S)', 'SYNDROMES', validation_value)
            if validation_value == '':
                validation_value = None
        if validation_value is not None:
            validation_value_tmp = validation_value
            validation_value = []
            validation_value.append(validation_value_tmp)
            validation_value = tuple(validation_value)
        display_flg = True
        performance = \
            self.evaluation_manager.evaluation(nlp_value, validation_value,
                                               display_flg)
        return performance
    
    #
    def _get_diagnosis_date_performance(self, labId, nlp_values, nlp_datum_key,
                                        validation_datum_key):
        validation_data = \
            self.validation_data_manager.get_validation_data()
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
        labid_idx = validation_data[0].index('labId')
        validation_datum_idx = validation_data[0].index(validation_datum_key)
        validation_value = None
        for item in validation_data:
            if item[labid_idx] == labId:
                validation_value = item[validation_datum_idx]
        if validation_value is not None:
            validation_value = \
                re.sub('(?<=/)20(?=[0-9][0-9])', '', validation_value)
            validation_value = \
                re.sub('(?<=/)0(?=[0-9]/)', '', validation_value)
            if validation_value == '':
                validation_value = None
        validation_value = \
            self._validation_to_tuple(validation_value)
        display_flg = True
        performance = \
            self.evaluation_manager.evaluation(nlp_value, validation_value,
                                               display_flg)
        return performance
    
    #
    def _get_extramedullary_disease_performance(self, labId, nlp_values,
                                                nlp_datum_key,
                                                validation_datum_key):
        validation_data = \
            self.validation_data_manager.get_validation_data()
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
        labid_idx = validation_data[0].index('labId')
        validation_datum_idx = validation_data[0].index(validation_datum_key)
        validation_value = None
        for item in validation_data:
            if item[labid_idx] == labId:
                validation_value = item[validation_datum_idx]
        if validation_value is not None:
            if validation_value == '':
                validation_value = None
        validation_value = self._validation_to_tuple(validation_value)
        display_flg = True
        performance = \
            self.evaluation_manager.evaluation(nlp_value, validation_value,
                                               display_flg)
        return performance
    
    #
    def _get_fab_classification_performance(self, labId, nlp_values,
                                            nlp_datum_key,
                                            validation_datum_key):
        validation_data = \
            self.validation_data_manager.get_validation_data()
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
        labid_idx = validation_data[0].index('labId')
        validation_datum_idx = validation_data[0].index(validation_datum_key)
        validation_value = None
        for item in validation_data:
            if item[labid_idx] == labId:
                validation_value = item[validation_datum_idx]
        if validation_value is not None:
            if validation_value == '':
                validation_value = None
        validation_value = self._validation_to_tuple(validation_value)
        display_flg = True
        performance = \
            self.evaluation_manager.evaluation(nlp_value, validation_value,
                                               display_flg)
        return performance
    
    #
    def _get_fish_analysis_summary_performance(self, labId, nlp_values,
                                               nlp_datum_key,
                                               validation_datum_key):
        validation_data = \
            self.validation_data_manager.get_validation_data()
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
        labid_idx = validation_data[0].index('labId')
        validation_datum_idx = validation_data[0].index(validation_datum_key)
        validation_value = None
        for item in validation_data:
            if item[labid_idx] == labId:
                validation_value = item[validation_datum_idx]
        if validation_value is not None:
            if validation_value == '':
                validation_value = None
        if validation_value is not None:
            validation_value_tmp = validation_value
            validation_value_tmp = \
                validation_value_tmp.replace(' ', '')
            validation_value = []
            validation_value.append(validation_value_tmp)
        if validation_value is not None:
            validation_value = tuple(validation_value)
        display_flg = True
        performance = \
            self.evaluation_manager.evaluation(nlp_value, validation_value,
                                               display_flg)
        return performance
    
    #
    def _get_karyotype_performance(self, labId, nlp_values, nlp_datum_key,
                                   validation_datum_key):
        validation_data = \
            self.validation_data_manager.get_validation_data()
        if labId in nlp_values.keys():
            keys0 = list(nlp_values[labId])
            if nlp_datum_key in nlp_values[labId][keys0[0]].keys():
                data_out = nlp_values[labId][keys0[0]][nlp_datum_key][0][0]
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
        labid_idx = validation_data[0].index('labId')
        validation_datum_idx = validation_data[0].index(validation_datum_key)
        validation_value = None
        for item in validation_data:
            if item[labid_idx] == labId:
                validation_value = item[validation_datum_idx]
        if validation_value is not None:
            validation_value = validation_value.replace('//', '/')
            if validation_value == '':
                validation_value = None
            if validation_value == 'N/A':
                validation_value = None
            if validation_value == 'Not available':
                validation_value = None
            if validation_value == 'None':
                validation_value = None
        if validation_value is not None:
            validation_value_tmp = validation_value
            validation_value_tmp = \
                validation_value_tmp.replace(' ', '')
            validation_value = []
            validation_value.append(validation_value_tmp)
        if validation_value is not None:
            validation_value = tuple(validation_value)
        display_flg = True
        performance = \
            self.evaluation_manager.evaluation(nlp_value, validation_value,
                                               display_flg)
        return performance
    
    #
    def _get_relapse_date_performance(self, labId, nlp_values, nlp_datum_key, 
                                      validation_datum_key):
        validation_data = \
            self.validation_data_manager.get_validation_data()
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
        labid_idx = validation_data[0].index('labId')
        validation_datum_idx = validation_data[0].index(validation_datum_key)
        validation_value = None
        for item in validation_data:
            if item[labid_idx] == labId:
                validation_value = item[validation_datum_idx]
        if validation_value is not None:
            validation_value = \
                re.sub('(?<=/)20(?=[0-9][0-9])', '', validation_value)
            if validation_value == '':
                validation_value = None
        validation_value = self._validation_to_tuple(validation_value)
        display_flg = True
        performance = \
            self.evaluation_manager.evaluation(nlp_value, validation_value,
                                               display_flg)
        return performance
    
    #
    def _get_residual_disease_performance(self, labId, nlp_values, nlp_datum_key, 
                                          validation_datum_key):
        validation_data = \
            self.validation_data_manager.get_validation_data()
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
        labid_idx = validation_data[0].index('labId')
        validation_datum_idx = validation_data[0].index(validation_datum_key)
        validation_value = None
        for item in validation_data:
            if item[labid_idx] == labId:
                validation_value = item[validation_datum_idx]
        if validation_value is not None:
            validation_value = re.sub('(?i)acute myeloid leukemia', 'AML', validation_value)
            validation_value = validation_value.lower()
            if validation_value == '':
                validation_value = None
        validation_value = self._validation_to_tuple(validation_value)
        display_flg = True
        performance = \
            self.evaluation_manager.evaluation(nlp_value, validation_value,
                                               display_flg)
        return performance
    
    #
    def _get_specific_diagnosis_performance(self, labId, nlp_values, nlp_datum_key, 
                                            validation_datum_key):
        validation_data = \
            self.validation_data_manager.get_validation_data()
        if labId in nlp_values.keys():
            keys0 = list(nlp_values[labId])
            if nlp_datum_key in nlp_values[labId][keys0[0]].keys():
                data_out = nlp_values[labId][keys0[0]][nlp_datum_key][0][0]
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
        labid_idx = validation_data[0].index('labId')
        validation_datum_idx = validation_data[0].index(validation_datum_key)
        validation_value = None
        for item in validation_data:
            if item[labid_idx] == labId:
                validation_value = item[validation_datum_idx]
        if validation_value is not None:
            validation_value = re.sub('LEUKAEMIA', 'LEUKEMIA', validation_value)
            validation_value = re.sub('leukaemia', 'leukemia', validation_value)
            validation_value = re.sub('(?i)acute myeloid leukemia', 'AML', validation_value)
            validation_value = re.sub('(?i)acute myelomonocytic leukemia', 'AMML', validation_value)
            validation_value = re.sub('monocytic and monoblastic', 'monoblastic and monocytic', validation_value)
            validation_value = re.sub(' ', '', validation_value)
            validation_value = validation_value.lower()
            if validation_value == '':
                validation_value = None
            elif validation_value[-1] == ',':
                validation_value = validation_value[:-1]
        if validation_value is not None:
            validation_value_tmp = validation_value
            validation_value = []
            validation_value.append(validation_value_tmp)
        if validation_value is not None:
            validation_specific_diagnosis_value = tuple(validation_value)
        else:
            validation_specific_diagnosis_value = None
        display_flg = True
        performance = \
            self.evaluation_manager.evaluation(nlp_value, validation_value,
                                               display_flg)
        return performance
    
    #
    def _get_surface_antigens_performance(self, labId, nlp_values, nlp_datum_key, 
                                          validation_datum_key):
        validation_data = \
            self.validation_data_manager.get_validation_data()
        if labId in nlp_values.keys():
            keys0 = list(nlp_values[labId])
            if nlp_datum_key in nlp_values[labId][keys0[0]].keys():
                data_out = nlp_values[labId][keys0[0]][nlp_datum_key][0][0]
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
        else:
            nlp_value = None
        labid_idx = validation_data[0].index('labId')
        validation_datum_idx = validation_data[0].index(validation_datum_key)
        validation_value = None
        for item in validation_data:
            if item[labid_idx] == labId:
                validation_value = item[validation_datum_idx]
        if validation_value is not None:
            validation_value = self._cleanup_antigens(validation_value)
            validation_value = re.sub('(?i)n/a', '', validation_value)
            validation_value = re.sub('(?i)not (available|run)', '', validation_value)
            if validation_value == '':
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
        display_flg = True
        performance = \
            self.evaluation_manager.evaluation(nlp_value, validation_value,
                                               display_flg)
        return performance
            
    #
    def _process_performance(self, nlp_values_in):
        document_csn_list = \
            self.metadata_manager.pull_document_identifier_list('SOURCE_SYSTEM_DOCUMENT_ID')
        nlp_performance_wo_nlp_manual_review_dict = {}
        nlp_performance_nlp_manual_review_dict = {}
        wo_validation_manual_review_dict = {}
        wo_nlp_manual_review_dict = {}
        for i in range(len(self.queries)):
            validation_datum_key = self.queries[i][0]
            nlp_performance_wo_nlp_manual_review_dict[validation_datum_key] = []
            nlp_performance_nlp_manual_review_dict[validation_datum_key] = []
            wo_validation_manual_review_dict[validation_datum_key] = 0
            wo_nlp_manual_review_dict[validation_datum_key] = 0
        patientIds = nlp_values_in.keys()
        patientIds = list(set(patientIds))
        for patientId in patientIds:
            if patientId in nlp_values_in:
                nlp_values = nlp_values_in[patientId]
            else:
                nlp_values = {}
            labIds = []
            labIds.extend(nlp_values.keys())
            for labId in labIds:
                print(labId)
                for i in range(len(self.queries)):
                    nlp_datum_key = self.queries[i][0]
                    validation_datum_key = self.queries[i][0]
                    column_labels = self.validation_data_manager.column_labels()
                    if nlp_values[labId] is not None:
                        if nlp_datum_key in nlp_values[labId].keys():
                            nlp_value = nlp_values[labId][nlp_datum_key]
                        else:
                            nlp_value = None
                    else:
                        nlp_value = None
                    if not ( nlp_value is not None and self.manual_review in nlp_value ):
                        nlp_performance_wo_nlp_manual_review_dict = \
                            self._generate_nlp_performance(nlp_performance_wo_nlp_manual_review_dict,
                                                           labId, nlp_values, nlp_datum_key,
                                                           validation_datum_key)
                    else:
                        nlp_performance_nlp_manual_review_dict = \
                            self._generate_nlp_performance(nlp_performance_nlp_manual_review_dict,
                                                           csn, nlp_values, nlp_datum_key,
                                                           validation_datum_key)
                        wo_nlp_manual_review_dict[validation_datum_key] += 1
        patientIds = nlp_values_in.keys()
        patientIds = list(set(patientIds))
        N_total = 0
        for patientId in patientIds:
            if patientId in nlp_values_in:
                nlp_patient = nlp_values_in[patientId]
            else:
                nlp_patient = {}
            labIds = []
            labIds.extend(nlp_patient.keys())
            for labId in labIds:
                N_total += 1
        N_documents = len(document_csn_list)
        self._generate_performance_statistics(nlp_performance_wo_nlp_manual_review_dict,
                                              nlp_performance_nlp_manual_review_dict,
                                              N_documents, None,
                                              wo_nlp_manual_review_dict)
            
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
    
    '''
    #
    def _substitution(self, match_pattern, repl_dict, text_in):
        text_out = text_in
        match = 0
        match_str = match_pattern
        m_str = re.compile(match_str)
        stop_flg = False
        ctr = 0
        while not stop_flg:
            ctr += 1
            stop_flg = True
            for match in m_str.finditer(text_out):
                if match is not None:
                    stop_flg = False
                    search_str = match.group(0)
                    for key in repl_dict.keys():
                        replace_str = re.sub(key, repl_dict[key], search_str)
                        text_out = text_out.replace(search_str, replace_str)
            if ctr == 100:
                stop_flg = True
        return text_out
    '''