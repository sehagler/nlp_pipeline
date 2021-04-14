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
from nlp_lib.py.tool_lib.query_tools_lib.date_tools import compare_dates
from nlp_lib.py.tool_lib.analysis_tools_lib.text_analysis_tools \
    import compare_texts
from projects_lib.BeatAML_Waves_1_And_2.py.specimens_class import Specimens
from projects_lib.BeatAML_Waves_1_And_2.py.gold_standard_jsons_class \
    import Gold_standard_jsons

#
class BeatAML_Waves_1_And_2_performance_data_manager(Performance_data_manager):
    
    #
    def __init__(self, project_manager):
        project_data = project_manager.get_project_data()
        Performance_data_manager.__init__(self, project_manager)
        self.project_data = project_data
    
    #
    def _compare_values_antigens(self, validation_record, gold_standard_record, data_item, score, patientId, labId):
        try:
            validation_value = validation_record[data_item]
            if validation_value == '':
                validation_value = None
        except:
            validation_value = None
        try:
            gold_standard_value = gold_standard_record[data_item]
            gold_standard_value = re.sub('(?i)n/a', '', gold_standard_value)
            gold_standard_value = re.sub('(?i)not (available|run)', '', gold_standard_value)
            if gold_standard_value == '':
                gold_standard_value = None
        except:
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
        try:
            validation_value = validation_record[data_item]
        except:
            validation_value = None
        try:
            gold_standard_value = gold_standard_record[data_item]
            if gold_standard_value == '':
                gold_standard_value = None
        except:
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
        try:
            validation_value = validation_record[data_item]
        except:
            validation_value = None
        try:
            gold_standard_value = gold_standard_record[data_item]
            if gold_standard_value == '':
                gold_standard_value = None
        except:
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
    def _compare_values_texts(self, validation_record, gold_standard_record, data_item, score, patientId, labId):
        multiple_values = self.multiple_values
        multiple_values = re.sub(' ', '', multiple_values)
        try:
            validation_value = validation_record[data_item]
            validation_value = re.sub(' ', '', validation_value)
        except:
            validation_value = None
        try:
            gold_standard_value = gold_standard_record[data_item]
            gold_standard_value = re.sub(' ', '', gold_standard_value)
            if gold_standard_value == '':
                gold_standard_value = None
        except:
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
    def _compare_values_karyotypes(self, validation_record, gold_standard_record, data_item, score, patientId, labId):
        multiple_values = self.multiple_values
        multiple_values = re.sub(' ', '', multiple_values)
        try:
            validation_value = validation_record[data_item]
            validation_value = re.sub(' ', '', validation_value)
            validation_value = re.sub('//', '/', validation_value)
        except:
            validation_value = None
        try:
            gold_standard_value = gold_standard_record[data_item]
            gold_standard_value = re.sub('(?i)n/a', '', gold_standard_value)
            gold_standard_value = re.sub('(?i)not (available|run)', '', gold_standard_value)
            gold_standard_value = re.sub(' ', '', gold_standard_value)
            if gold_standard_value == '':
                gold_standard_value = None
            elif gold_standard_value[-1] == ',':
                gold_standard_value = gold_standard_value[:-1]
        except:
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
        try:
            validation_value = validation_record[data_item]
            validation_value = re.sub(' ', '', validation_value)
            validation_value = validation_value.lower()
        except:
            validation_value = None
        try:
            gold_standard_value = gold_standard_record[data_item]
            gold_standard_value = re.sub('(?i)acute myeloid leukemia', 'AML', gold_standard_value)
            gold_standard_value = re.sub(' ', '', gold_standard_value)
            gold_standard_value = gold_standard_value.lower()
            if gold_standard_value == '':
                gold_standard_value = None
            elif gold_standard_value[-1] == ',':
                gold_standard_value = gold_standard_value[:-1]
        except:
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
    def _compare_values_specific_diagnosis(self, validation_record, gold_standard_record, data_item, score, patientId, labId):
        multiple_values = self.multiple_values
        multiple_values = re.sub(' ', '', multiple_values)
        multiple_values = multiple_values.lower()
        try:
            validation_value = validation_record[data_item]
            validation_value = re.sub('/', 'and', validation_value)
            validation_value = re.sub('monocytic and monoblastic', 'monoblastic and monocytic', validation_value)
            validation_value = re.sub(' ', '', validation_value)
            validation_value = validation_value.lower()
        except:
            validation_value = None
        try:
            gold_standard_value = gold_standard_record[data_item]
            gold_standard_value = re.sub('(?i)acute myeloid leukemia', 'AML', gold_standard_value)
            gold_standard_value = re.sub('(?i)acute myelomonocytic leukemia', 'AMML', gold_standard_value)
            gold_standard_value = re.sub('monocytic and monoblastic', 'monoblastic and monocytic', gold_standard_value)
            gold_standard_value = re.sub(' ', '', gold_standard_value)
            gold_standard_value = gold_standard_value.lower()
            if gold_standard_value == '':
                gold_standard_value = None
            elif gold_standard_value[-1] == ',':
                gold_standard_value = gold_standard_value[:-1]
        except:
            gold_standard_value = None
        if data_item not in score.keys():
            score[data_item] = [ 0, 0, 0, 0, 0, 0 ]
        cond00 = validation_value is not None
        cond01 = validation_value is None
        cond10 = gold_standard_value is not None
        cond11 = gold_standard_value is None
        if cond00 and cond10:
            if validation_value != multiple_values:
                if validation_value in gold_standard_value:
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
    def _get_data(self, nlp_data):
        gold_standard_object = Gold_standard_jsons(self.directory_manager, self.mrn_list)
        gold_standard_object.generate_json_file(self.directory_manager.pull_directory('log_dir'), 'gold_standard.json')
        self.gold_standard_data = gold_standard_object.get_data_json()
        validation_object = Specimens(self.project_data, nlp_data)
        validation_object.generate_json_file(self.directory_manager.pull_directory('log_dir'), 'validation.json')
        self.validation_data = validation_object.get_data_json()
        
    #
    def calculate_performance(self):
        nlp_data = self.nlp_data
        self.mrn_list = self.project_data['patient_list']
        self._get_data(self.nlp_data)
        full_specimen_ctr = 0
        gs_record_ctr = 0
        patient_ids_list = []
        for patientId in self.gold_standard_data.keys():
            gold_standard_patient = self.gold_standard_data[patientId]
            gs_record_ctr += len(gold_standard_patient.keys())
        patientIds = []
        #patientIds.extend(self.gold_standard_data.keys())
        patientIds = self.validation_data.keys()
        patientIds = list(set(patientIds))
        labids_score = [ 0, 0, 0, 0 ]
        item_score = {}
        missing_specimens = {}
        for patientId in patientIds:
            try:
                validation_patient = self.validation_data[patientId]
            except:
                validation_patient = {}
            try:
                gold_standard_patient = self.gold_standard_data[patientId]
            except:
                gold_standard_patient = {}
            labIds = []
            #labIds.extend(gold_standard_patient.keys())
            labIds.extend(validation_patient.keys())
            for labId in labIds:
                try:
                    validation_record_tmp = validation_patient[labId]
                    keys0 = list(validation_record_tmp)
                    validation_record = validation_record_tmp[keys0[0]]
                except:
                    validation_record = {}
                try:
                    gold_standard_record = gold_standard_patient[labId]
                except:
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
                            self._compare_values(validation_value, gold_standard_value)
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
        performance_statistics_list = []
        for key in item_score.keys():
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
            performance_statistics['QUERY'] = key
            performance_statistics_list.append(performance_statistics)
        self.logger.create_file('log.txt')
        print('\n')
        print(gs_record_ctr)
        print(missing_specimens)
        print(full_specimen_ctr)
        print(len(list(set(patient_ids_list))))
        return performance_statistics_list
        
    #
    def display_performance(self, performance_statistics_list):
        self._display_performance_statistics(performance_statistics_list)