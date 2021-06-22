# -*- coding: utf-8 -*-
"""
Created on Mon Mar 04 12:29:38 2019

@author: haglers
"""

#
import re

#
from nlp_lib.py.performance_data_lib.performance_data_manager_class \
    import Performance_data_manager
from nlp_lib.py.tool_lib.analysis_tools_lib.text_analysis_tools \
    import compare_texts
from projects_lib.BeatAML_Waves_1_And_2.py.specimens_class import Specimens
from projects_lib.BeatAML_Waves_1_And_2.py.gold_standard_jsons_class \
    import Gold_standard_jsons
from tool_lib.py.query_tools_lib.date_tools import compare_dates

#
class BeatAML_Waves_1_And_2_performance_data_manager(Performance_data_manager):
    
    #
    def __init__(self, static_data_manager):
        project_data = static_data_manager.get_project_data()
        
        json_structure_manager = project_data['json_structure_manager']
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
        self.multiple_specimens = \
            json_structure_manager.pull_key('multiple_specimens')
        self.multiple_values = \
            json_structure_manager.pull_key('multiple_values')
        #
        
        Performance_data_manager.__init__(self, static_data_manager)
        self.project_data = project_data
    
    #
    def _compare_values_antigens(self, validation_record, gold_standard_record, data_item, score, patientId, labId):
        if data_item in validation_record.keys():
            validation_value = validation_record[data_item]
            if validation_value == '':
                validation_value = None
        else:
            validation_value = None
        if data_item in gold_standard_record.keys():
            gold_standard_value = gold_standard_record[data_item]
            gold_standard_value = re.sub('(?i)n/a', '', gold_standard_value)
            gold_standard_value = re.sub('(?i)not (available|run)', '', gold_standard_value)
            if gold_standard_value == '':
                gold_standard_value = None
        else:
            gold_standard_value = None
        if data_item not in score.keys():
            score[data_item] = [ 0, 0, 0, 0, 0, 0 ]
        cond00 = validation_value is not None
        cond01 = validation_value is None
        cond10 = gold_standard_value is not None
        cond11 = gold_standard_value is None
        if cond00 and cond10:
            if validation_value != self.multiple_values:
                text_score = compare_texts(gold_standard_value, validation_value, True)
                if text_score[0] == 0:
                    score[data_item][0] += 1
                else:
                    score[data_item][3] += 1
                    self.logger.log_entry(patientId, labId, data_item, gold_standard_value, validation_value)
            else:
                score[data_item][2] += 1
                self.logger.log_entry(patientId, labId, data_item, gold_standard_value, validation_value)
        elif cond00 and cond11:
            score[data_item][4] += 1
            self.logger.log_entry(patientId, labId, data_item, gold_standard_value, validation_value)
        elif cond01 and cond10:
            score[data_item][5] += 1
            self.logger.log_entry(patientId, labId, data_item, gold_standard_value, validation_value)
        elif cond01 and cond11:
            score[data_item][1] += 1
        return score
    
    #
    def _compare_values_blasts(self, validation_record, gold_standard_record, data_item, score, patientId, labId):
        if data_item in validation_record.keys():
            validation_value = validation_record[data_item]
        else:
            validation_value = None
        if data_item in gold_standard_record.keys():
            gold_standard_value = gold_standard_record[data_item]
            if gold_standard_value == '':
                gold_standard_value = None
        else:
            gold_standard_value = None
        if data_item not in score.keys():
            score[data_item] = [ 0, 0, 0, 0, 0, 0 ]
        cond00 = validation_value is not None
        cond01 = validation_value is None
        cond10 = gold_standard_value is not None
        cond11 = gold_standard_value is None
        if cond00 and cond10:
            if validation_value != self.multiple_values:
                if validation_value == gold_standard_value:
                    score[data_item][0] += 1
                elif validation_value[0] == '>':
                    if gold_standard_value[0] == '>':
                        score[data_item[0]] += 1
                    elif gold_standard_value[0] == '<':
                        try:
                            test_flg = float(gold_standard_value[2:]) - float(validation_value[2:]) >= 0.0
                        except:
                            test_flg = False
                        if test_flg:
                            score[data_item][0] += 1
                        else:
                            score[data_item][3] += 1
                            self.logger.log_entry(patientId, labId, data_item, gold_standard_value, validation_value)
                    else:
                        try:
                            test_flg = float(gold_standard_value) - float(validation_value[2:]) >= 0.0
                        except:
                            test_flg = False
                        if test_flg:
                            score[data_item][0] += 1
                        else:
                            score[data_item][3] += 1
                            self.logger.log_entry(patientId, labId, data_item, gold_standard_value, validation_value)
                elif validation_value[0] == '<':
                    if gold_standard_value[0] == '<':
                        score[data_item[0]] += 1
                    elif gold_standard_value[0] == '>':
                        try:
                            test_flg = float(gold_standard_value[2:]) - float(validation_value[2:]) >= 0.0
                        except:
                            test_flg = False
                        if test_flg:
                            score[data_item][0] += 1
                        else:
                            score[data_item][3] += 1
                            self.logger.log_entry(patientId, labId, data_item, gold_standard_value, validation_value)
                    else:
                        try:
                            test_flg = float(validation_value[2:]) - float(gold_standard_value) >= 0.0
                        except:
                            test_flg = False
                        if test_flg:
                            score[data_item][0] += 1
                        else:
                            score[data_item][3] += 1
                            self.logger.log_entry(patientId, labId, data_item, gold_standard_value, validation_value)
                else:
                    try:
                        test_flg = abs(float(validation_value) - float(gold_standard_value)) <= 5.0
                    except:
                        test_flg = False
                    if test_flg:
                        score[data_item][0] += 1
                    else:
                        score[data_item][3] += 1
                        self.logger.log_entry(patientId, labId, data_item, gold_standard_value, validation_value)
            else:
                score[data_item][2] += 1
                self.logger.log_entry(patientId, labId, data_item, gold_standard_value, validation_value)
        elif cond00 and cond11:
            score[data_item][4] += 1
            self.logger.log_entry(patientId, labId, data_item, gold_standard_value, validation_value)
        elif cond01 and cond10:
            score[data_item][5] += 1
            self.logger.log_entry(patientId, labId, data_item, gold_standard_value, validation_value)
        elif cond01 and cond11:
            score[data_item][1] += 1
        return score
    
    #
    def _compare_values_dates(self, validation_record, gold_standard_record, data_item, score, patientId, labId):
        if data_item in validation_record.keys():
            validation_value = validation_record[data_item]
        else:
            validation_value = None
        if data_item in gold_standard_record.keys():
            gold_standard_value = gold_standard_record[data_item]
            if gold_standard_value == '':
                gold_standard_value = None
        else:
            gold_standard_value = None
        if data_item not in score.keys():
            score[data_item] = [ 0, 0, 0, 0, 0, 0 ]
        cond00 = validation_value is not None
        cond01 = validation_value is None
        cond10 = gold_standard_value is not None
        cond11 = gold_standard_value is None
        if cond00 and cond10:
            if validation_value != self.multiple_values:
                text_score = compare_dates(gold_standard_value, validation_value)
                if text_score:
                    score[data_item][0] += 1
                else:
                    score[data_item][3] += 1
                    self.logger.log_entry(patientId, labId, data_item, gold_standard_value, validation_value)
            else:
                score[data_item][2] += 1
                self.logger.log_entry(patientId, labId, data_item, gold_standard_value, validation_value)
        elif cond00 and cond11:
            score[data_item][4] += 1
            self.logger.log_entry(patientId, labId, data_item, gold_standard_value, validation_value)
        elif cond01 and cond10:
            score[data_item][5] += 1
            self.logger.log_entry(patientId, labId, data_item, gold_standard_value, validation_value)
        elif cond01 and cond11:
            score[data_item][1] += 1
            self.logger.log_entry(patientId, labId, data_item, gold_standard_value, validation_value)
        return score
    
    #
    def _compare_values_karyotypes(self, validation_record, gold_standard_record, data_item, score, patientId, labId):
        multiple_values = self.multiple_values
        multiple_values = re.sub(' ', '', multiple_values)
        if data_item in validation_record.keys():
            validation_value = validation_record[data_item]
            validation_value = re.sub(' ', '', validation_value)
            validation_value = re.sub('//', '/', validation_value)
        else:
            validation_value = None
        if data_item in gold_standard_record.keys():
            gold_standard_value = gold_standard_record[data_item]
            gold_standard_value = re.sub('(?i)n/a', '', gold_standard_value)
            gold_standard_value = re.sub('(?i)not (available|run)', '', gold_standard_value)
            gold_standard_value = re.sub(' ', '', gold_standard_value)
            if gold_standard_value == '':
                gold_standard_value = None
            elif gold_standard_value[-1] == ',':
                gold_standard_value = gold_standard_value[:-1]
        else:
            gold_standard_value = None
        if data_item not in score.keys():
            score[data_item] = [ 0, 0, 0, 0, 0, 0 ]
        cond00 = validation_value is not None
        cond01 = validation_value is None
        cond10 = gold_standard_value is not None
        cond11 = gold_standard_value is None
        if cond00 and cond10:
            if validation_value != multiple_values:
                if validation_value == gold_standard_value:
                    score[data_item][0] += 1
                else:
                    score[data_item][3] += 1
                    self.logger.log_entry(patientId, labId, data_item, gold_standard_value, validation_value)
            else:
                score[data_item][2] += 1
                self.logger.log_entry(patientId, labId, data_item, gold_standard_value, validation_value)
        elif cond00 and cond11:
            score[data_item][4] += 1
            self.logger.log_entry(patientId, labId, data_item, gold_standard_value, validation_value)
        elif cond01 and cond10:
            score[data_item][5] += 1
            self.logger.log_entry(patientId, labId, data_item, gold_standard_value, validation_value)
        elif cond01 and cond11:
            score[data_item][1] += 1
        return score
    
    #
    def _compare_values_residual_diagnosis(self, validation_record, gold_standard_record, data_item, score, patientId, labId):
        multiple_values = self.multiple_values
        multiple_values = re.sub(' ', '', multiple_values)
        multiple_values = multiple_values.lower()
        if data_item in validation_record.keys():
            validation_value = validation_record[data_item]
            validation_value = re.sub(' ', '', validation_value)
            validation_value = validation_value.lower()
        else:
            validation_value = None
        if data_item in gold_standard_record.keys():
            gold_standard_value = gold_standard_record[data_item]
            gold_standard_value = re.sub('(?i)acute myeloid leukemia', 'AML', gold_standard_value)
            gold_standard_value = re.sub(' ', '', gold_standard_value)
            gold_standard_value = gold_standard_value.lower()
            if gold_standard_value == '':
                gold_standard_value = None
            elif gold_standard_value[-1] == ',':
                gold_standard_value = gold_standard_value[:-1]
        else:
            gold_standard_value = None
        if data_item not in score.keys():
            score[data_item] = [ 0, 0, 0, 0, 0, 0 ]
        cond00 = validation_value is not None
        cond01 = validation_value is None
        cond10 = gold_standard_value is not None
        cond11 = gold_standard_value is None
        if cond00 and cond10:
            if validation_value != multiple_values:
                if validation_value == gold_standard_value:
                    score[data_item][0] += 1
                else:
                    score[data_item][3] += 1
                    self.logger.log_entry(patientId, labId, data_item, gold_standard_value, validation_value)
            else:
                score[data_item][2] += 1
                self.logger.log_entry(patientId, labId, data_item, gold_standard_value, validation_value)
        elif cond00 and cond11:
            score[data_item][4] += 1
            self.logger.log_entry(patientId, labId, data_item, gold_standard_value, validation_value)
        elif cond01 and cond10:
            score[data_item][5] += 1
            self.logger.log_entry(patientId, labId, data_item, gold_standard_value, validation_value)
        elif cond01 and cond11:
            score[data_item][1] += 1
        return score
    
    #
    def _compare_values_specific_diagnosis(self, validation_record, 
                                           gold_standard_record, item, 
                                           item_score, patientId, labId):
        multiple_values = self.multiple_values
        multiple_values = re.sub(' ', '', multiple_values)
        multiple_values = multiple_values.lower()
        if item in validation_record.keys():
            #print(validation_record)
            validation_value = validation_record[item]
            #print(validation_value)
            validation_value = re.sub('/', 'and', validation_value)
            validation_value = re.sub('monocytic and monoblastic', 'monoblastic and monocytic', validation_value)
            validation_value = re.sub(' ', '', validation_value)
            validation_value = validation_value.lower()
            #print(validation_value)
            #print('')
        else:
            validation_value = None
        if item in gold_standard_record.keys():
            gold_standard_value = gold_standard_record[item]
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
        performance, flg = \
            self._compare_strings(validation_value, gold_standard_value)
        item_score = self._performance_values(item, item_score, performance)
        return item_score
    
    #
    def _compare_values_texts(self, validation_record, gold_standard_record, 
                              item, item_score, patientId, labId):
        multiple_values = self.multiple_values
        multiple_values = re.sub(' ', '', multiple_values)
        if item in validation_record.keys():
            validation_value = validation_record[item]
            validation_value = re.sub(' ', '', validation_value)
        else:
            validation_value = None
        if item in gold_standard_record.keys():
            gold_standard_value = gold_standard_record[item]
            gold_standard_value = re.sub(' ', '', gold_standard_value)
            if gold_standard_value == '':
                gold_standard_value = None
        else:
            gold_standard_value = None
        performance, flg = \
            self._compare_values(validation_value, gold_standard_value)
        item_score = self._performance_values(item, item_score, performance)
        return item_score
    
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
            self._get_data_value(data_in, [ 'SUMMARY', 'COMMENT', 'AMENDMENT COMMENT' ], 'SURFACE_ANTIGENS_' + self.nlp_value_key, 'IMMUNOPHENOTYPE')
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
    def _performance_values(self, item, item_score, performance):
        if item not in item_score.keys():
            item_score[item] = [ 0, 0, 0, 0, 0, 0 ]
        if performance == 'false negative':
            item_score[item][5] += 1
        elif performance == 'false positive':
            item_score[item][4] += 1
        elif performance == 'false positive + false negative':
            item_score[item][3] += 1
        elif performance == 'true negative':
            item_score[item][1] += 1
        elif performance == 'true positive':
            item_score[item][0] += 1
        elif performance == 'multiple values':
            item_score[item][2] += 1
        return item_score
    
    #
    def _read_nlp_value_data(self, nlp_data):
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
        validation_object = Specimens(self.project_data, metadata_dict_dict, data_json)
        validation_object.generate_json_file(self.directory_manager.pull_directory('log_dir'), 'validation.json')
        nlp_values = validation_object.get_data_json()
        return nlp_values
    
    #
    def _read_validation_data(self, project_data, nlp_data):
        mrn_list = project_data['patient_list']
        gold_standard_object = Gold_standard_jsons(self.directory_manager, mrn_list)
        gold_standard_object.generate_json_file(self.directory_manager.pull_directory('log_dir'), 'gold_standard.json')
        validation_data = gold_standard_object.get_data_json()
        return validation_data
    
    #
    def calculate_performance(self):
        nlp_data = self.nlp_data
        validation_data = \
            self._read_validation_data(self.project_data, nlp_data)
        full_specimen_ctr = 0
        gs_record_ctr = 0
        patient_ids_list = []
        for patientId in validation_data.keys():
            validation_patient = validation_data[patientId]
            gs_record_ctr += len(validation_patient.keys())
        patientIds = []
        #patientIds.extend(validation_data.keys())
        nlp_values = self._read_nlp_value_data(nlp_data)
        self.nlp_values = nlp_values
        patientIds = self.nlp_values.keys()
        patientIds = list(set(patientIds))
        labids_score = [ 0, 0, 0, 0 ]
        item_score = {}
        missing_specimens = {}
        for patientId in patientIds:
            if patientId in validation_data:
                validation_patient = validation_data[patientId]
            else:
                validation_patient = {}
            if patientId in self.nlp_values:
                nlp_patient = self.nlp_values[patientId]
            else:
                nlp_patient = {}
            labIds = []
            #labIds.extend(validation_patient.keys())
            labIds.extend(nlp_patient.keys())
            for labId in labIds:
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
                if not bool(validation_record) and bool(gold_standard_record):
                    missing_specimens[patientId] = labId
                else:
                    patient_ids_list.append(patientId)
                    docs_list = list(validation_record_tmp)
                    if '_' in docs_list[0]:
                        full_specimen_ctr += 1
                cond00 = len(validation_record) > 0
                cond01 = len(validation_record) == 0
                cond10 = len(gold_standard_record) > 0
                cond11 = len(gold_standard_record) == 0
                if cond00 and cond10:
                    labids_score[0] += 1
                elif cond00 and cond11:
                    labids_score[1] += 1
                elif cond01 and cond10:
                    labids_score[2] += 1
                elif cond01 and cond11:
                    labids_score[3] += 1
                for item in [ 'Antibodies.Tested', 'dx.Date', 'dx', 'Extramedullary.dx',
                              'FAB/Blast.Morphology', 'FISH.Analysis.Summary', 
                              'Karyotype', '%.Blasts.in.BM', '%.Blasts.in.PB',
                              'Relapse.Date', 'Residual.dx', 'specificDx',
                              'Surface.Antigens.(Immunohistochemical.Stains)' ]:
                    if item in [ '%.Blasts.in.BM', '%.Blasts.in.PB' ]:
                        item_score = \
                            self._compare_values_blasts(validation_record, gold_standard_record, item, item_score, patientId, labId)
                    elif item in [ 'Antibodies.Tested', 'Surface.Antigens.(Immunohistochemical.Stains)' ]:
                        item_score = \
                            self._compare_values_antigens(validation_record, gold_standard_record, item, item_score, patientId, labId)
                    elif item in [ 'dx.Date', 'Relapse.Date' ]:
                        item_score = \
                            self._compare_values_dates(validation_record, gold_standard_record, item, item_score, patientId, labId)
                    elif item in [ 'FISH.Analysis.Summary' ]:
                        item_score = \
                            self._compare_values_texts(validation_record, gold_standard_record, item, item_score, patientId, labId)
                    elif item in [ 'Karyotype' ]:
                        item_score = \
                            self._compare_values_karyotypes(validation_record, gold_standard_record, item, item_score, patientId, labId)
                    elif item in [ 'Residual.dx' ]:
                        item_score = \
                            self._compare_values_residual_diagnosis(validation_record, gold_standard_record, item, item_score, patientId, labId)
                    elif item in [ 'specificDx' ]:
                        item_score = \
                            self._compare_values_specific_diagnosis(validation_record, gold_standard_record, item, item_score, patientId, labId)
                    else:
                        try:
                            validation_value = validation_record[item]
                            validation_value = re.sub('SYNDROME', 'SYNDROMES', validation_value)
                        except:
                            validation_value = None
                        try:
                            gold_standard_value = gold_standard_record[item]
                            if gold_standard_value == '':
                                gold_standard_value = None
                        except:
                            gold_standard_value = None
                        performance, flg = \
                            self._compare_data_values(validation_value,
                                                      gold_standard_value)
                        item_score = \
                            self._performance_values(item, item_score, performance)
        performance_statistics_dict = {}
        for key in item_score.keys():
            performance_key = {}
            performance_key['Antibodies.Tested'] = 'ANTIBODIES_TESTED'
            performance_key['dx'] = 'DIAGNOSIS'
            performance_key['dx.Date'] = 'DIAGNOSIS_DATE'
            performance_key['Extramedullary.dx'] = 'EXTRAMEDULARY_DISEASE'
            performance_key['FAB/Blast.Morphology'] = 'FAB_CLASSIFICATION'
            performance_key['FISH.Analysis.Summary'] = 'FISH_ANALYSIS_SUMMARY'
            performance_key['Karyotype'] = 'KARYOTYPE'
            performance_key['%.Blasts.in.BM'] = 'BONE_MARROW_BLAST'
            performance_key['%.Blasts.in.PB'] = 'PERIPHERAL_BLOOD_BLAST'
            performance_key['Relapse.Date'] = 'RELAPSE_DATE'
            performance_key['Residual.dx'] = 'RESIDUAL_DISEASE'
            performance_key['specificDx'] = 'SPECIFIC_DIAGNOSIS'
            performance_key['Surface.Antigens.(Immunohistochemical.Stains)'] = \
                'SURFACE_ANTIGENS'
            M = item_score[key][2]
            FN = item_score[key][5]
            FP = item_score[key][4]
            FP_plus_FN = item_score[key][3]
            TN = item_score[key][1]
            TP = item_score[key][0]
            N = sum(item_score[key])
            print('--' + key + '--')
            print(item_score[key])
            print(f'\tnumber docs: ' + str(N))
            print(f'\tmultiple vals: ' + str(M))
            print(f'\tfalse neg: ' + str(FN))
            print(f'\tfalse pos: ' + str(FP))
            print(f'\tfalse pos + false neg: ' + str(FP_plus_FN))
            performance_statistics = \
                self._performance_statistics(FN, FP, FP_plus_FN, TN, TP, N)
            performance_statistics_dict[performance_key[key]] = \
                performance_statistics
        self.logger.create_file('log.txt')
        print('\n')
        print(gs_record_ctr)
        print(missing_specimens)
        print(full_specimen_ctr)
        print(len(list(set(patient_ids_list))))
        return performance_statistics_dict
        
    #
    def display_performance(self, performance_statistics_dict):
        self._display_performance_statistics(performance_statistics_dict)