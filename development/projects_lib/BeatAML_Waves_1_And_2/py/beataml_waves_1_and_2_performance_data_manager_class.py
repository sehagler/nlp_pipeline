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
        static_data['json_files_key_value'] = [ ('bone_marrow_blast_file', 'bone_marrow_blast.json'),
                                                ('diagnosis_file', 'diagnosis.json'),
                                                ('diagnosis_date_file', 'diagnosis_date.json'),
                                                ('extramedullary_disease_file', 'extramedullary_disease.json'),
                                                ('fab_classification_file', 'fab_classification.json'),
                                                ('immunophenotype_file', 'immunophenotype.json'),
                                                ('peripheral_blood_blast_file', 'peripheral_blood_blast.json'),
                                                ('relapse_date_file', 'relapse_date.json'),
                                                ('residual_disease_file', 'residual_disease.json'),
                                                ('sections_file', 'sections.json') ]
        
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
        
        self.static_data = static_data
    
    #
    def _get_nlp_data(self, data_in):
        data_out = {}
        data_out['Antibodies.Tested'] = \
            self._get_data_value(data_in, [ 'ANTIBODIES TESTED' ], 'ANTIBODIES_TESTED_' + self.nlp_value_key, 'ANTIBODIES_TESTED')
        if data_out['Antibodies.Tested'] is not None:
            data_out['Antibodies.Tested'] = data_out['Antibodies.Tested'][0]
        data_out['dx'] = \
            self._get_data_value(data_in, [ 'SUMMARY', 'COMMENT', 'AMENDMENT COMMENT' ], 'DIAGNOSIS_' + self.nlp_value_key, 'DIAGNOSIS')
        if data_out['dx'] is not None:
            data_out['dx'] = data_out['dx'][0]
        data_out['dx.Date'] = \
            self._get_data_value(data_in, [ 'HISTORY', 'COMMENT', 'AMENDMENT COMMENT', 'SUMMARY' ], 'DIAGNOSIS_DATE_' + self.nlp_value_key, 'DATE')
        if data_out['dx.Date'] is not None:
            data_out['dx.Date'] = data_out['dx.Date'][0]
        data_out['Extramedullary.dx'] = \
            self._get_data_value(data_in, [ 'SUMMARY', 'COMMENT', 'AMENDMENT COMMENT' ], 'EXTRAMEDULLARY_DISEASE_' + self.nlp_value_key, 'EXTRAMEDULLARY_DISEASE')
        if data_out['Extramedullary.dx'] is not None:
            data_out['Extramedullary.dx'] = data_out['Extramedullary.dx'][0]
        data_out['FAB/Blast.Morphology'] = \
            self._get_data_value(data_in, [ 'COMMENT', 'AMENDMENT COMMENT', 'BONE MARROW' ], 'FAB_CLASSIFICATION_' + self.nlp_value_key, 'FAB_CLASSIFICATION')
        if data_out['FAB/Blast.Morphology'] is not None:
            data_out['FAB/Blast.Morphology'] = data_out['FAB/Blast.Morphology'][0]
        data_out['FISH.Analysis.Summary'] = \
            self._get_data_value(data_in, [ 'FISH ANALYSIS SUMMARY' ], 'FISH_ANALYSIS_SUMMARY_' + self.nlp_value_key, 'FISH_ANALYSIS_SUMMARY')
        if data_out['FISH.Analysis.Summary'] is not None:
            data_out['FISH.Analysis.Summary'] = data_out['FISH.Analysis.Summary'][0]
        data_out['Karyotype'] = \
            self._get_data_value(data_in, [ 'KARYOTYPE', 'IMPRESSIONS AND RECOMMENDATIONS' ], 'KARYOTYPE_' + self.nlp_value_key, 'KARYOTYPE' )
        if data_out['Karyotype'] is not None:
            data_out['Karyotype'] = data_out['Karyotype'][0]
        data_out['%.Blasts.in.BM'] = \
            self._get_data_value(data_in, [ 'SUMMARY', 'BONE MARROW DIFFERENTIAL', 'BONE MARROW ASPIRATE' ], 'BONE_MARROW_BLAST_' + self.nlp_value_key, 'BLAST_PERCENTAGE')
        if data_out['%.Blasts.in.BM'] is not None:
            data_out['%.Blasts.in.BM'] = data_out['%.Blasts.in.BM'][0]
        data_out['%.Blasts.in.PB'] = \
            self._get_data_value(data_in, [ 'SUMMARY', 'PERIPHERAL BLOOD MORPHOLOGY' ], 'PERIPHERAL_BLOOD_BLAST_' + self.nlp_value_key, 'BLAST_PERCENTAGE')
        if data_out['%.Blasts.in.PB'] is not None:
            data_out['%.Blasts.in.PB'] = data_out['%.Blasts.in.PB'][0]
        data_out['Relapse.Date'] = \
            self._get_data_value(data_in, [ 'HISTORY', 'COMMENT', 'AMENDMENT COMMENT', 'SUMMARY' ], 'RELAPSE_DATE_' + self.nlp_value_key, 'DATE')
        if data_out['Relapse.Date'] is not None:
            data_out['Relapse.Date'] = data_out['Relapse.Date'][0]
        data_out['Residual.dx'] = \
            self._get_data_value(data_in, [ 'SUMMARY', 'COMMENT', 'AMENDMENT COMMENT' ], 'RESIDUAL_DISEASE_' + self.nlp_value_key, 'DIAGNOSIS')
        if data_out['Residual.dx'] is not None:
            data_out['Residual.dx'] = data_out['Residual.dx'][0]
        data_out['specificDx'] = \
            self._get_data_value(data_in, [ 'SUMMARY', 'COMMENT', 'AMENDMENT COMMENT' ], 'SPECIFIC_DIAGNOSIS_' + self.nlp_value_key, 'DIAGNOSIS')
        if data_out['specificDx'] is not None:
            data_out['specificDx'] = data_out['specificDx'][0]
        data_out['Surface.Antigens.(Immunohistochemical.Stains)'] = \
            self._get_data_value(data_in, [ 'SUMMARY', 'COMMENT', 'AMENDMENT COMMENT' ], 'IMMUNOPHENOTYPE_' + self.nlp_value_key, 'IMMUNOPHENOTYPE')
        if data_out['Surface.Antigens.(Immunohistochemical.Stains)'] is not None:
            data_out['Surface.Antigens.(Immunohistochemical.Stains)'] = \
                data_out['Surface.Antigens.(Immunohistochemical.Stains)'][0]
        del_keys = []
        for key in data_out:
            if data_out[key] is not None:
                data_out[key] = [ data_out[key] ]
            else:
                del_keys.append(key)
        for key in del_keys:
            del data_out[key]
        if not data_out:
            data_out = None
        return data_out
    
    #
    def _process_antibodies_tested_performance(self, nlp_values, validation_data):
        patientIds = nlp_values.keys()
        patientIds = list(set(patientIds))
        nlp_antibodies_tested_performance = []
        N = 0
        for patientId in patientIds:
            if patientId in validation_data:
                validation_patient = validation_data[patientId]
            else:
                validation_patient = {}
            if patientId in nlp_values:
                nlp_patient = nlp_values[patientId]
            else:
                nlp_patient = {}
            labIds = []
            labIds.extend(nlp_patient.keys())
            for labId in labIds:
                print(labId)
                if labId in nlp_patient.keys():
                    validation_record_tmp = nlp_patient[labId]
                    keys0 = list(validation_record_tmp)
                    validation_record = validation_record_tmp[keys0[0]]
                else:
                    validation_record = {}
                if labId in validation_patient.keys():
                    gold_standard_record = validation_patient[labId]
                else:
                    gold_standard_record = {}
                if 'Antibodies.Tested' in validation_record.keys():
                    validation_value = validation_record['Antibodies.Tested']
                    if validation_value == '':
                        validation_value = None
                else:
                    validation_value = None
                if 'Antibodies.Tested' in gold_standard_record.keys():
                    gold_standard_value = gold_standard_record['Antibodies.Tested']
                    gold_standard_value = re.sub('(?i)n/a', '', gold_standard_value)
                    gold_standard_value = re.sub('(?i)not (available|run)', '', gold_standard_value)
                    if gold_standard_value == '':
                        gold_standard_value = None
                else:
                    gold_standard_value = None
                if validation_value is not None:
                    validation_value = re.sub('dim', 'dim ', validation_value)
                    validation_value = re.sub('\+', ' +', validation_value)
                    validation_value = re.sub('(?i)(-)?positive', ' +', validation_value)
                    validation_value = extract_antigens(validation_value)
                    validation_value = list(set(validation_value))
                if gold_standard_value is not None:
                    gold_standard_value = re.sub('dim', 'dim ', gold_standard_value)
                    gold_standard_value = re.sub('\+', ' +', gold_standard_value)
                    gold_standard_value = re.sub('(?i)(-)?positive', ' +', gold_standard_value)
                    gold_standard_value = extract_antigens(gold_standard_value)
                    gold_standard_value = list(set(gold_standard_value))
                if validation_value is not None:
                    nlp_antibodies_tested_value = tuple(validation_value)
                else:
                    nlp_antibodies_tested_value = None
                if gold_standard_value is not None:
                    validation_antibodies_tested_value = \
                        tuple(gold_standard_value)
                else:
                    validation_antibodies_tested_value = None
                N += 1
                performance, flg = \
                    self._compare_data_values(nlp_antibodies_tested_value,
                                              validation_antibodies_tested_value)
                nlp_antibodies_tested_performance.append(performance)
        FN, FP, FP_plus_FN, TN, TP = \
            self._performance_values(nlp_antibodies_tested_performance)
        performance_statistics = \
            self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
        self.performance_statistics_dict['ANTIBODIES_TESTED'] = \
            performance_statistics
    
    #
    def _process_bone_marrow_blast_performance(self, nlp_values, validation_data):
        patientIds = nlp_values.keys()
        patientIds = list(set(patientIds))
        nlp_bone_marrow_blast_performance = []
        N = 0
        for patientId in patientIds:
            if patientId in validation_data:
                validation_patient = validation_data[patientId]
            else:
                validation_patient = {}
            if patientId in nlp_values:
                nlp_patient = nlp_values[patientId]
            else:
                nlp_patient = {}
            labIds = []
            labIds.extend(nlp_patient.keys())
            for labId in labIds:
                print(labId)
                if labId in nlp_patient.keys():
                    validation_record_tmp = nlp_patient[labId]
                    keys0 = list(validation_record_tmp)
                    validation_record = validation_record_tmp[keys0[0]]
                else:
                    validation_record = {}
                if labId in validation_patient.keys():
                    gold_standard_record = validation_patient[labId]
                else:
                    gold_standard_record = {}
                if '%.Blasts.in.BM' in validation_record.keys():
                    validation_value = validation_record['%.Blasts.in.BM']
                else:
                    validation_value = None
                if '%.Blasts.in.BM' in gold_standard_record.keys():
                    gold_standard_value = gold_standard_record['%.Blasts.in.BM']
                    if gold_standard_value == '':
                        gold_standard_value = None
                else:
                    gold_standard_value = None
                if validation_value is not None:
                    validation_value = validation_value.replace('~', '')
                    validation_value = validation_value.replace('>', '')
                    validation_value = validation_value.replace('<', '')
                    validation_value = validation_value.replace('.0', '')
                if gold_standard_value is not None:
                    gold_standard_value = gold_standard_value.replace('~', '')
                    gold_standard_value = gold_standard_value.replace('>', '')
                    gold_standard_value = gold_standard_value.replace('<', '')
                    gold_standard_value = gold_standard_value.replace('.0', '')
                    gold_standard_value = gold_standard_value.replace('None', '0')
                if validation_value is not None:
                    nlp_bone_marrow_blast_value = []
                    nlp_bone_marrow_blast_value.append(validation_value)
                else:
                    nlp_bone_marrow_blast_value = None
                validation_bone_marrow_blast_value = gold_standard_value
                nlp_bone_marrow_blast_value = \
                    self._nlp_to_tuple(nlp_bone_marrow_blast_value)
                validation_bone_marrow_blast_value = \
                    self._validation_to_tuple(validation_bone_marrow_blast_value)
                N += 1
                performance, flg = \
                    self._compare_data_values(nlp_bone_marrow_blast_value,
                                              validation_bone_marrow_blast_value,
                                              value_range=5.0)
                nlp_bone_marrow_blast_performance.append(performance)
        FN, FP, FP_plus_FN, TN, TP = \
            self._performance_values(nlp_bone_marrow_blast_performance)
        performance_statistics = \
            self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
        self.performance_statistics_dict['BONE_MARROW_BLAST'] = \
            performance_statistics
            
    #
    def _process_diagnosis_performance(self, nlp_values, validation_data):
        patientIds = nlp_values.keys()
        patientIds = list(set(patientIds))
        nlp_diagnosis_performance = []
        N = 0
        for patientId in patientIds:
            if patientId in validation_data:
                validation_patient = validation_data[patientId]
            else:
                validation_patient = {}
            if patientId in nlp_values:
                nlp_patient = nlp_values[patientId]
            else:
                nlp_patient = {}
            labIds = []
            labIds.extend(nlp_patient.keys())
            for labId in labIds:
                print(labId)
                if labId in nlp_patient.keys():
                    validation_record_tmp = nlp_patient[labId]
                    keys0 = list(validation_record_tmp)
                    validation_record = validation_record_tmp[keys0[0]]
                else:
                    validation_record = {}
                if labId in validation_patient.keys():
                    gold_standard_record = validation_patient[labId]
                else:
                    gold_standard_record = {}
                try:
                    validation_value = validation_record['dx']
                    validation_value = \
                        re.sub('SYNDROME(?!S)', 'SYNDROMES', validation_value)
                except:
                    validation_value = None
                try:
                    gold_standard_value = gold_standard_record['dx']
                    gold_standard_value = \
                        re.sub('SYNDROME(?!S)', 'SYNDROMES', gold_standard_value)
                    if gold_standard_value == '':
                        gold_standard_value = None
                except:
                    gold_standard_value = None
                if validation_value is not None:
                    nlp_diagnosis_value = []
                    nlp_diagnosis_value.append(validation_value)
                    nlp_diagnosis_value = tuple(nlp_diagnosis_value)
                else:
                    nlp_diagnosis_value = None
                if gold_standard_value is not None:
                    validation_diagnosis_value = []
                    validation_diagnosis_value.append(gold_standard_value)
                    validation_diagnosis_value = tuple(validation_diagnosis_value)
                else:
                    validation_diagnosis_value = None
                N += 1
                performance, flg = \
                    self._compare_data_values(nlp_diagnosis_value,
                                              validation_diagnosis_value)
                nlp_diagnosis_performance.append(performance)
        FN, FP, FP_plus_FN, TN, TP = \
            self._performance_values(nlp_diagnosis_performance)
        performance_statistics = \
            self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
        self.performance_statistics_dict['DIAGNOSIS'] = \
            performance_statistics
            
    #
    def _process_diagnosis_date_performance(self, nlp_values, validation_data):
        patientIds = nlp_values.keys()
        patientIds = list(set(patientIds))
        nlp_diagnosis_date_performance = []
        N = 0
        for patientId in patientIds:
            if patientId in validation_data:
                validation_patient = validation_data[patientId]
            else:
                validation_patient = {}
            if patientId in nlp_values:
                nlp_patient = nlp_values[patientId]
            else:
                nlp_patient = {}
            labIds = []
            labIds.extend(nlp_patient.keys())
            for labId in labIds:
                print(labId)
                if labId in nlp_patient.keys():
                    validation_record_tmp = nlp_patient[labId]
                    keys0 = list(validation_record_tmp)
                    validation_record = validation_record_tmp[keys0[0]]
                else:
                    validation_record = {}
                if labId in validation_patient.keys():
                    gold_standard_record = validation_patient[labId]
                else:
                    gold_standard_record = {}
                try:
                    validation_value = validation_record['dx.Date']
                    validation_value = \
                        re.sub('(?<=/)20(?=[0-9][0-9])', '', validation_value)
                    validation_value = \
                        re.sub('(?<=/)0(?=[0-9]/)', '', validation_value)
                except:
                    validation_value = None
                try:
                    gold_standard_value = gold_standard_record['dx.Date']
                    gold_standard_value = \
                        re.sub('(?<=/)20(?=[0-9][0-9])', '', gold_standard_value)
                    gold_standard_value = \
                        re.sub('(?<=/)0(?=[0-9]/)', '', gold_standard_value)
                    if gold_standard_value == '':
                        gold_standard_value = None
                except:
                    gold_standard_value = None
                if validation_value is not None:
                    validation_value_tmp = validation_value
                    validation_value = []
                    validation_value.append(validation_value_tmp)
                else:
                    validation_value = None
                nlp_diagnosis_date_value = validation_value
                validation_diagnosis_date_value = gold_standard_value
                nlp_diagnosis_date_value = \
                    self._nlp_to_tuple(nlp_diagnosis_date_value)
                validation_diagnosis_date_value = \
                    self._validation_to_tuple(validation_diagnosis_date_value)
                N += 1
                performance, flg = \
                    self._compare_data_values(nlp_diagnosis_date_value,
                                              validation_diagnosis_date_value)
                nlp_diagnosis_date_performance.append(performance)
        FN, FP, FP_plus_FN, TN, TP = \
            self._performance_values(nlp_diagnosis_date_performance)
        performance_statistics = \
            self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
        self.performance_statistics_dict['DIAGNOSIS_DATE'] = \
            performance_statistics
            
    #
    def _process_extramedullary_disease_performance(self, nlp_values, validation_data):
        patientIds = nlp_values.keys()
        patientIds = list(set(patientIds))
        nlp_extramedullary_disease_performance = []
        N = 0
        for patientId in patientIds:
            if patientId in validation_data:
                validation_patient = validation_data[patientId]
            else:
                validation_patient = {}
            if patientId in nlp_values:
                nlp_patient = nlp_values[patientId]
            else:
                nlp_patient = {}
            labIds = []
            labIds.extend(nlp_patient.keys())
            for labId in labIds:
                print(labId)
                if labId in nlp_patient.keys():
                    validation_record_tmp = nlp_patient[labId]
                    keys0 = list(validation_record_tmp)
                    validation_record = validation_record_tmp[keys0[0]]
                else:
                    validation_record = {}
                if labId in validation_patient.keys():
                    gold_standard_record = validation_patient[labId]
                else:
                    gold_standard_record = {}
                try:
                    validation_value = validation_record['Extramedullary.dx']
                    validation_value = re.sub('SYNDROME', 'SYNDROMES', validation_value)
                except:
                    validation_value = None
                try:
                    gold_standard_value = gold_standard_record['Extramedullary.dx']
                    if gold_standard_value == '':
                        gold_standard_value = None
                except:
                    gold_standard_value = None
                if validation_value is not None:
                    validation_value_tmp = validation_value
                    validation_value = []
                    validation_value.append(validation_value_tmp)
                else:
                    validation_value = None
                nlp_extramedullary_disease_value = \
                    self._nlp_to_tuple(validation_value)
                validation_extramedullary_disease_value = \
                    self._validation_to_tuple(gold_standard_value)
                N += 1
                performance, flg = \
                    self._compare_data_values(nlp_extramedullary_disease_value,
                                              validation_extramedullary_disease_value)
                nlp_extramedullary_disease_performance.append(performance)
        FN, FP, FP_plus_FN, TN, TP = \
            self._performance_values(nlp_extramedullary_disease_performance)
        performance_statistics = \
            self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
        self.performance_statistics_dict['EXTRAMEDULARY_DISEASE'] = \
            performance_statistics
            
    #
    def _process_fab_classification_performance(self, nlp_values, validation_data):
        patientIds = nlp_values.keys()
        patientIds = list(set(patientIds))
        nlp_fab_classification_performance = []
        N = 0
        for patientId in patientIds:
            if patientId in validation_data:
                validation_patient = validation_data[patientId]
            else:
                validation_patient = {}
            if patientId in nlp_values:
                nlp_patient = nlp_values[patientId]
            else:
                nlp_patient = {}
            labIds = []
            labIds.extend(nlp_patient.keys())
            for labId in labIds:
                print(labId)
                if labId in nlp_patient.keys():
                    validation_record_tmp = nlp_patient[labId]
                    keys0 = list(validation_record_tmp)
                    validation_record = validation_record_tmp[keys0[0]]
                else:
                    validation_record = {}
                if labId in validation_patient.keys():
                    gold_standard_record = validation_patient[labId]
                else:
                    gold_standard_record = {}
                try:
                    validation_value = validation_record['FAB/Blast.Morphology']
                    validation_value = re.sub('SYNDROME', 'SYNDROMES', validation_value)
                except:
                    validation_value = None
                try:
                    gold_standard_value = gold_standard_record['FAB/Blast.Morphology']
                    if gold_standard_value == '':
                        gold_standard_value = None
                except:
                    gold_standard_value = None
                if validation_value is not None:
                    validation_value_tmp = validation_value
                    validation_value = []
                    validation_value.append(validation_value_tmp)
                else:
                    validation_value = None
                nlp_fab_classification_value = \
                    self._nlp_to_tuple(validation_value)
                validation_fab_classification_value = \
                    self._validation_to_tuple(gold_standard_value)
                N += 1
                performance, flg = \
                    self._compare_data_values(nlp_fab_classification_value,
                                              validation_fab_classification_value)
                nlp_fab_classification_performance.append(performance)
        FN, FP, FP_plus_FN, TN, TP = \
            self._performance_values(nlp_fab_classification_performance)
        performance_statistics = \
            self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
        self.performance_statistics_dict['FAB_CLASSIFICATION'] = \
            performance_statistics
            
    #
    def _process_fish_analysis_summary_performance(self, nlp_values, validation_data):
        patientIds = nlp_values.keys()
        patientIds = list(set(patientIds))
        nlp_fish_analysis_summary_performance = []
        N = 0
        for patientId in patientIds:
            if patientId in validation_data:
                validation_patient = validation_data[patientId]
            else:
                validation_patient = {}
            if patientId in nlp_values:
                nlp_patient = nlp_values[patientId]
            else:
                nlp_patient = {}
            labIds = []
            labIds.extend(nlp_patient.keys())
            for labId in labIds:
                print(labId)
                if labId in nlp_patient.keys():
                    validation_record_tmp = nlp_patient[labId]
                    keys0 = list(validation_record_tmp)
                    validation_record = validation_record_tmp[keys0[0]]
                else:
                    validation_record = {}
                if labId in validation_patient.keys():
                    gold_standard_record = validation_patient[labId]
                else:
                    gold_standard_record = {}
                try:
                    validation_value = validation_record['FISH.Analysis.Summary']
                except:
                    validation_value = None
                try:
                    gold_standard_value = gold_standard_record['FISH.Analysis.Summary']
                    if gold_standard_value == '':
                        gold_standard_value = None
                except:
                    gold_standard_value = None
                if validation_value is not None:
                    validation_value_tmp = validation_value
                    validation_value_tmp = \
                        validation_value_tmp.replace(' ', '')
                    if validation_value_tmp != '':
                        validation_value = []
                        validation_value.append(validation_value_tmp)
                    else:
                        validation_value = None
                    if validation_value is not None:
                        nlp_fish_analysis_summary_value = tuple(validation_value)
                    else:
                        nlp_fish_analysis_summary_value = None
                else:
                    nlp_fish_analysis_summary_value = None
                if gold_standard_value is not None:
                    gold_standard_value_tmp = gold_standard_value
                    gold_standard_value_tmp = \
                        gold_standard_value_tmp.replace(' ', '')
                    gold_standard_value = []
                    gold_standard_value.append(gold_standard_value_tmp)
                    validation_fish_analysis_summary_value = \
                        tuple(gold_standard_value)
                else:
                    validation_fish_analysis_summary_value = None
                N += 1
                performance, flg = \
                    self._compare_data_values(nlp_fish_analysis_summary_value,
                                              validation_fish_analysis_summary_value)
                nlp_fish_analysis_summary_performance.append(performance)
        FN, FP, FP_plus_FN, TN, TP = \
            self._performance_values(nlp_fish_analysis_summary_performance)
        performance_statistics = \
            self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
        self.performance_statistics_dict['FISH_ANALYSIS_SUMMARY'] = \
            performance_statistics
            
    #
    def _process_karyotype_performance(self, nlp_values, validation_data):
        patientIds = nlp_values.keys()
        patientIds = list(set(patientIds))
        nlp_karyotype_performance = []
        N = 0
        for patientId in patientIds:
            if patientId in validation_data:
                validation_patient = validation_data[patientId]
            else:
                validation_patient = {}
            if patientId in nlp_values:
                nlp_patient = nlp_values[patientId]
            else:
                nlp_patient = {}
            labIds = []
            labIds.extend(nlp_patient.keys())
            for labId in labIds:
                print(labId)
                if labId in nlp_patient.keys():
                    validation_record_tmp = nlp_patient[labId]
                    keys0 = list(validation_record_tmp)
                    validation_record = validation_record_tmp[keys0[0]]
                else:
                    validation_record = {}
                if labId in validation_patient.keys():
                    gold_standard_record = validation_patient[labId]
                else:
                    gold_standard_record = {}
                try:
                    validation_value = validation_record['Karyotype']
                    validation_value = validation_value.replace('//', '/')
                except:
                    validation_value = None
                try:
                    gold_standard_value = gold_standard_record['Karyotype']
                    gold_standard_value = gold_standard_value.replace('//', '/')
                    if gold_standard_value == '':
                        gold_standard_value = None
                    if gold_standard_value == 'N/A':
                        gold_standard_value = None
                    if gold_standard_value == 'Not available':
                        gold_standard_value = None
                    if gold_standard_value == 'None':
                        gold_standard_value = None
                except:
                    gold_standard_value = None
                if validation_value is not None:
                    validation_value_tmp = validation_value
                    validation_value_tmp = \
                        validation_value_tmp.replace(' ', '')
                    validation_value = []
                    validation_value.append(validation_value_tmp)
                    nlp_karyotype_value = tuple(validation_value)
                else:
                    nlp_karyotype_value = None
                if gold_standard_value is not None:
                    gold_standard_value_tmp = gold_standard_value
                    gold_standard_value_tmp = \
                        gold_standard_value_tmp.replace(' ', '')
                    gold_standard_value = []
                    gold_standard_value.append(gold_standard_value_tmp)
                    validation_karyotype_value = \
                        tuple(gold_standard_value)
                else:
                    validation_karyotype_value = None
                N += 1
                performance, flg = \
                    self._compare_data_values(nlp_karyotype_value,
                                              validation_karyotype_value)
                nlp_karyotype_performance.append(performance)
        FN, FP, FP_plus_FN, TN, TP = \
            self._performance_values(nlp_karyotype_performance)
        performance_statistics = \
            self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
        self.performance_statistics_dict['KARYOTYPE'] = \
            performance_statistics
            
    #
    def _process_performance(self, nlp_values, validation_data):
        self._process_antibodies_tested_performance(nlp_values, validation_data)
        self._process_bone_marrow_blast_performance(nlp_values, validation_data)
        self._process_diagnosis_performance(nlp_values, validation_data)
        self._process_diagnosis_date_performance(nlp_values, validation_data)
        self._process_extramedullary_disease_performance(nlp_values, validation_data)
        self._process_fab_classification_performance(nlp_values, validation_data)
        self._process_fish_analysis_summary_performance(nlp_values, validation_data)
        self._process_karyotype_performance(nlp_values, validation_data)
        self._process_peripheral_blood_blast_performance(nlp_values, validation_data)
        self._process_relapse_date_performance(nlp_values, validation_data)
        self._process_residual_disease_performance(nlp_values, validation_data)
        self._process_specific_diagnosis_performance(nlp_values, validation_data)
        self._process_surface_antigens_performance(nlp_values, validation_data)
    
    #
    def _process_peripheral_blood_blast_performance(self, nlp_values, validation_data):
        patientIds = nlp_values.keys()
        patientIds = list(set(patientIds))
        nlp_peripheral_blood_blast_performance = []
        N = 0
        for patientId in patientIds:
            if patientId in validation_data:
                validation_patient = validation_data[patientId]
            else:
                validation_patient = {}
            if patientId in nlp_values:
                nlp_patient = nlp_values[patientId]
            else:
                nlp_patient = {}
            labIds = []
            labIds.extend(nlp_patient.keys())
            for labId in labIds:
                print(labId)
                if labId in nlp_patient.keys():
                    validation_record_tmp = nlp_patient[labId]
                    keys0 = list(validation_record_tmp)
                    validation_record = validation_record_tmp[keys0[0]]
                else:
                    validation_record = {}
                if labId in validation_patient.keys():
                    gold_standard_record = validation_patient[labId]
                else:
                    gold_standard_record = {}
                if '%.Blasts.in.PB' in validation_record.keys():
                    validation_value = validation_record['%.Blasts.in.PB']
                else:
                    validation_value = None
                if '%.Blasts.in.PB' in gold_standard_record.keys():
                    gold_standard_value = gold_standard_record['%.Blasts.in.PB']
                    if gold_standard_value == '':
                        gold_standard_value = None
                else:
                    gold_standard_value = None 
                if validation_value is not None:
                    validation_value = validation_value.replace('~', '')
                    validation_value = validation_value.replace('>', '')
                    validation_value = validation_value.replace('<', '')
                    validation_value = validation_value.replace('.0', '')
                if gold_standard_value is not None:
                    gold_standard_value = gold_standard_value.replace('~', '')
                    gold_standard_value = gold_standard_value.replace('>', '')
                    gold_standard_value = gold_standard_value.replace('<', '')
                    gold_standard_value = gold_standard_value.replace('.0', '')
                    gold_standard_value = gold_standard_value.replace('None', '0')
                if validation_value is not None:
                    nlp_peripheral_blood_blast_value = []
                    nlp_peripheral_blood_blast_value.append(validation_value)
                else:
                    nlp_peripheral_blood_blast_value = None
                validation_peripheral_blood_blast_value = gold_standard_value
                nlp_peripheral_blood_blast_value = \
                    self._nlp_to_tuple(nlp_peripheral_blood_blast_value)
                validation_peripheral_blood_blast_value = \
                    self._validation_to_tuple(validation_peripheral_blood_blast_value)
                N += 1
                performance, flg = \
                    self._compare_data_values(nlp_peripheral_blood_blast_value,
                                              validation_peripheral_blood_blast_value,
                                              value_range=5.0)
                nlp_peripheral_blood_blast_performance.append(performance)
        FN, FP, FP_plus_FN, TN, TP = \
            self._performance_values(nlp_peripheral_blood_blast_performance)
        performance_statistics = \
            self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
        self.performance_statistics_dict['PERIPHERAL_BLOOD_BLAST'] = \
            performance_statistics
    
    #
    def _process_relapse_date_performance(self, nlp_values, validation_data):
        patientIds = nlp_values.keys()
        patientIds = list(set(patientIds))
        nlp_relapse_date_performance = []
        N = 0
        for patientId in patientIds:
            if patientId in validation_data:
                validation_patient = validation_data[patientId]
            else:
                validation_patient = {}
            if patientId in nlp_values:
                nlp_patient = nlp_values[patientId]
            else:
                nlp_patient = {}
            labIds = []
            labIds.extend(nlp_patient.keys())
            for labId in labIds:
                print(labId)
                if labId in nlp_patient.keys():
                    validation_record_tmp = nlp_patient[labId]
                    keys0 = list(validation_record_tmp)
                    validation_record = validation_record_tmp[keys0[0]]
                else:
                    validation_record = {}
                if labId in validation_patient.keys():
                    gold_standard_record = validation_patient[labId]
                else:
                    gold_standard_record = {}
                try:
                    validation_value = validation_record['Relapse.Date']
                    validation_value = \
                        re.sub('(?<=/)20(?=[0-9][0-9])', '', validation_value)
                except:
                    validation_value = None
                try:
                    gold_standard_value = gold_standard_record['Relapse.Date']
                    gold_standard_value = \
                        re.sub('(?<=/)20(?=[0-9][0-9])', '', gold_standard_value)
                    if gold_standard_value == '':
                        gold_standard_value = None
                except:
                    gold_standard_value = None
                if validation_value is not None:
                    validation_value_tmp = validation_value
                    validation_value = []
                    validation_value.append(validation_value_tmp)
                else:
                    validation_value = None
                nlp_relapse_date_value = validation_value
                validation_relapse_date_value = gold_standard_value
                nlp_relapse_date_value = \
                    self._nlp_to_tuple(nlp_relapse_date_value)
                validation_relapse_date_value = \
                    self._validation_to_tuple(validation_relapse_date_value)
                N += 1
                performance, flg = \
                    self._compare_data_values(nlp_relapse_date_value,
                                              validation_relapse_date_value)
                nlp_relapse_date_performance.append(performance)
        FN, FP, FP_plus_FN, TN, TP = \
            self._performance_values(nlp_relapse_date_performance)
        performance_statistics = \
            self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
        self.performance_statistics_dict['RELAPSE_DATE'] = \
            performance_statistics
            
    #
    def _process_residual_disease_performance(self, nlp_values, validation_data):
        patientIds = nlp_values.keys()
        patientIds = list(set(patientIds))
        nlp_residual_disease_performance = []
        N = 0
        for patientId in patientIds:
            if patientId in validation_data:
                validation_patient = validation_data[patientId]
            else:
                validation_patient = {}
            if patientId in nlp_values:
                nlp_patient = nlp_values[patientId]
            else:
                nlp_patient = {}
            labIds = []
            labIds.extend(nlp_patient.keys())
            for labId in labIds:
                print(labId)
                if labId in nlp_patient.keys():
                    validation_record_tmp = nlp_patient[labId]
                    keys0 = list(validation_record_tmp)
                    validation_record = validation_record_tmp[keys0[0]]
                else:
                    validation_record = {}
                if labId in validation_patient.keys():
                    gold_standard_record = validation_patient[labId]
                else:
                    gold_standard_record = {}
                try:
                    validation_value = validation_record['Residual.dx']
                    validation_value = validation_value.lower()
                except:
                    validation_value = None
                try:
                    gold_standard_value = gold_standard_record['Residual.dx']
                    gold_standard_value = re.sub('(?i)acute myeloid leukemia', 'AML', gold_standard_value)
                    gold_standard_value = gold_standard_value.lower()
                    if gold_standard_value == '':
                        gold_standard_value = None
                except:
                    gold_standard_value = None
                if validation_value is not None:
                    validation_value_tmp = validation_value
                    validation_value = []
                    validation_value.append(validation_value_tmp)
                else:
                    validation_value = None
                nlp_residual_disease_value = validation_value
                validation_residual_disease_value = gold_standard_value
                nlp_residual_disease_value = \
                    self._nlp_to_tuple(nlp_residual_disease_value)
                validation_residual_disease_value = \
                    self._validation_to_tuple(validation_residual_disease_value)
                N += 1
                performance, flg = \
                    self._compare_data_values(nlp_residual_disease_value,
                                              validation_residual_disease_value)
                nlp_residual_disease_performance.append(performance)
        FN, FP, FP_plus_FN, TN, TP = \
            self._performance_values(nlp_residual_disease_performance)
        performance_statistics = \
            self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
        self.performance_statistics_dict['RESIDUAL_DISEASE'] = \
            performance_statistics
    
    #
    def _process_specific_diagnosis_performance(self, nlp_values, validation_data):
        patientIds = nlp_values.keys()
        patientIds = list(set(patientIds))
        item_score = {}
        nlp_specific_diagnosis_performance = []
        N = 0
        for patientId in patientIds:
            if patientId in validation_data:
                validation_patient = validation_data[patientId]
            else:
                validation_patient = {}
            if patientId in nlp_values:
                nlp_patient = nlp_values[patientId]
            else:
                nlp_patient = {}
            labIds = []
            labIds.extend(nlp_patient.keys())
            for labId in labIds:
                print(labId)
                if labId in nlp_patient.keys():
                    validation_record_tmp = nlp_patient[labId]
                    keys0 = list(validation_record_tmp)
                    validation_record = validation_record_tmp[keys0[0]]
                else:
                    validation_record = {}
                if labId in validation_patient.keys():
                    gold_standard_record = validation_patient[labId]
                else:
                    gold_standard_record = {}
                if 'specificDx' in validation_record.keys():
                    validation_value = validation_record['specificDx']
                    validation_value = re.sub('/', 'and', validation_value)
                    validation_value = re.sub('monocytic and monoblastic', 'monoblastic and monocytic', validation_value)
                    validation_value = re.sub(' ', '', validation_value)
                    validation_value = validation_value.lower()
                else:
                    validation_value = None
                if 'specificDx' in gold_standard_record.keys():
                    gold_standard_value = gold_standard_record['specificDx']
                    gold_standard_value = re.sub('(?i)acute myeloid leukemia', 'AML', gold_standard_value)
                    gold_standard_value = re.sub('(?i)acute myelomonocytic leukemia', 'AMML', gold_standard_value)
                    gold_standard_value = re.sub('monocytic and monoblastic', 'monoblastic and monocytic', gold_standard_value)
                    gold_standard_value = re.sub(' ', '', gold_standard_value)
                    gold_standard_value = gold_standard_value.lower()
                    if gold_standard_value == '':
                        gold_standard_value = None
                    elif gold_standard_value[-1] == ',':
                        gold_standard_value = gold_standard_value[:-1]
                else:
                    gold_standard_value = None
                if validation_value is not None:
                    validation_value_tmp = validation_value
                    validation_value = []
                    validation_value.append(validation_value_tmp)
                if gold_standard_value is not None:
                    gold_standard_value_tmp = gold_standard_value
                    gold_standard_value = []
                    gold_standard_value.append(gold_standard_value_tmp)
                if validation_value is not None:
                    nlp_specific_diagnosis_value = tuple(validation_value)
                else:
                    nlp_specific_diagnosis_value = None
                if gold_standard_value is not None:
                    validation_specific_diagnosis_value = tuple(gold_standard_value)
                else:
                    validation_specific_diagnosis_value = None
                N += 1
                performance, flg = \
                    self._compare_data_values(nlp_specific_diagnosis_value,
                                              validation_specific_diagnosis_value)
                nlp_specific_diagnosis_performance.append(performance)
        FN, FP, FP_plus_FN, TN, TP = \
            self._performance_values(nlp_specific_diagnosis_performance)
        performance_statistics = \
            self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
        self.performance_statistics_dict['SPECIFIC_DIAGNOSIS'] = \
            performance_statistics
    
    #
    def _process_surface_antigens_performance(self, nlp_values, validation_data):
        patientIds = nlp_values.keys()
        patientIds = list(set(patientIds))
        nlp_surface_antigens_performance = []
        N = 0
        for patientId in patientIds:
            if patientId in validation_data:
                validation_patient = validation_data[patientId]
            else:
                validation_patient = {}
            if patientId in nlp_values:
                nlp_patient = nlp_values[patientId]
            else:
                nlp_patient = {}
            labIds = []
            labIds.extend(nlp_patient.keys())
            for labId in labIds:
                print(labId)
                if labId in nlp_patient.keys():
                    validation_record_tmp = nlp_patient[labId]
                    keys0 = list(validation_record_tmp)
                    validation_record = validation_record_tmp[keys0[0]]
                else:
                    validation_record = {}
                if labId in validation_patient.keys():
                    gold_standard_record = validation_patient[labId]
                else:
                    gold_standard_record = {}
                if 'Surface.Antigens.(Immunohistochemical.Stains)' in validation_record.keys():
                    validation_value = validation_record['Surface.Antigens.(Immunohistochemical.Stains)']
                    if validation_value == '':
                        validation_value = None
                else:
                    validation_value = None
                if 'Surface.Antigens.(Immunohistochemical.Stains)' in gold_standard_record.keys():
                    gold_standard_value = gold_standard_record['Surface.Antigens.(Immunohistochemical.Stains)']
                    gold_standard_value = re.sub('(?i)n/a', '', gold_standard_value)
                    gold_standard_value = re.sub('(?i)not (available|run)', '', gold_standard_value)
                    if gold_standard_value == '':
                        gold_standard_value = None
                else:
                    gold_standard_value = None
                if validation_value is not None:
                    if isinstance(validation_value, list):
                        validation_value = self.manual_review
                if validation_value is not None and \
                   validation_value is not self.manual_review:
                    validation_value = re.sub('dim', 'dim ', validation_value)
                    validation_value = re.sub('\+', ' +', validation_value)
                    validation_value = re.sub('(?i)(-)?positive', ' +', validation_value)
                    validation_value = extract_antigens(validation_value)
                    validation_value = list(set(validation_value))
                if gold_standard_value is not None:
                    gold_standard_value = re.sub('dim', 'dim ', gold_standard_value)
                    gold_standard_value = re.sub('\+', ' +', gold_standard_value)
                    gold_standard_value = re.sub('(?i)(-)?positive', ' +', gold_standard_value)
                    gold_standard_value = extract_antigens(gold_standard_value)
                    gold_standard_value = list(set(gold_standard_value))
                if validation_value is not None and \
                   validation_value is not self.manual_review:
                    nlp_surface_antigens_value = tuple(validation_value)
                elif validation_value is None:
                    nlp_surface_antigens_value = None
                if gold_standard_value is not None:
                    validation_surface_antigens_value = \
                        tuple(gold_standard_value)
                else:
                    validation_surface_antigens_value = None
                N += 1
                performance, flg = \
                    self._compare_data_values(nlp_surface_antigens_value,
                                              validation_surface_antigens_value)
                nlp_surface_antigens_performance.append(performance)
        FN, FP, FP_plus_FN, TN, TP = \
            self._performance_values(nlp_surface_antigens_performance)
        performance_statistics = \
            self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
        self.performance_statistics_dict['SURFACE_ANTIGENS'] = \
            performance_statistics
    
    #
    def _read_nlp_value_data(self, nlp_data, validation_data):
        metadata_keys, metadata_dict_dict = self._read_metadata(nlp_data)
        data_json = {}
        for key in nlp_data.keys():
            json_tmp = nlp_data[key]
            doc_name = str(key)
            mrn = json_tmp[self.metadata_key]['MRN']
            preprocessed_text = json_tmp[self.nlp_source_text_key]
            if 'PROC_NM' in json_tmp[self.metadata_key].keys():
                proc_nm = json_tmp[self.metadata_key]['PROC_NM']
            else:
                proc_nm = json_tmp[self.metadata_key]['PROC_NAME']
            result_date = json_tmp[self.metadata_key]['RESULT_COMPLETED_DT']
            specimen_date = json_tmp[self.metadata_key]['SPECIMEN_COLL_DT']
            data_in = json_tmp[self.nlp_data_key]
            data_out = self._get_nlp_data(data_in)
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
        validation_object = Specimens(self.static_data, metadata_dict_dict, data_json)
        validation_object.generate_json_file(self.directory_manager.pull_directory('log_dir'), 'validation.json')
        nlp_values = validation_object.get_data_json()
        return nlp_values
    
    #
    def _read_validation_data(self):
        mrn_list = self.static_data['patient_list']
        gold_standard_object = Gold_standard_jsons(self.directory_manager, mrn_list)
        gold_standard_object.generate_json_file(self.directory_manager.pull_directory('log_dir'), 'gold_standard.json')
        validation_data = gold_standard_object.get_data_json()
        return validation_data