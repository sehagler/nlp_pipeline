# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 12:13:23 2019

@author: haglers
"""

#
import re
import traceback

#
from tool_lib.py.processing_tools_lib.variable_processing_tools \
    import trim_data_value
from tool_lib.py.query_tools_lib.base_lib.postprocessor_base_class \
    import Postprocessor_base

#
class Postprocessor(Postprocessor_base):

    #
    def _extract_data_value(self, value_list_dict):
        extracted_data_dict = {}
        for key in value_list_dict.keys():
            text_list = value_list_dict[key]
            diagnosis_keys = self.diagnosis_reader.get_keys()
            dx_list = []
            for item in text_list[0]:
                dx_list.append(item[0])
            value_list = []
            for entry_txt in dx_list:
                entry_txt = \
                    self.lambda_manager.lambda_conversion('\(.*?\)', entry_txt, '')
                entry_txt = \
                    self.lambda_manager.lambda_conversion(' +', entry_txt, ' ')
                del_key = True
                for diagnosis_key in diagnosis_keys:
                    diagnosis_dict = self.diagnosis_reader.get_dict_by_key(diagnosis_key)
                    for diagnosis in diagnosis_dict['specific_diagnosis']:
                        if not re.search('(?i)no evidence of marrow involvement by ' + diagnosis, entry_txt):
                            if re.search('(?i)(?<!/)' + diagnosis + '(?!/)', entry_txt):
                                del_key = False
                                value_list.append((diagnosis_key, diagnosis))
            value_dict_list = []
            for value in value_list:
                value_dict = {}
                value_dict['DIAGNOSIS'] = value
                value_dict_list.append(value_dict)
            extracted_data_dict[key] = value_dict_list
        return extracted_data_dict
    
    #
    def run_postprocessor(self):
        Postprocessor_base.run_postprocessor(self,
                                             query_name='SPECIFIC_DIAGNOSIS',
                                             section_name='(COMMENT|NOTE|SUMMARY)')
        
#                 
def evaluate_specific_diagnosis(data_json):
    data_json_tmp = data_json
    for key0 in data_json_tmp.keys():
        for key1 in data_json_tmp[key0].keys():
            for key2 in data_json_tmp[key0][key1].keys():
                try:
                    values = data_json_tmp[key0][key1][key2]['specificDxAtAcquisition']
                    values = values[0]
                    #values = trim_data_value(values)
                    #values = list(set(values))
                    specific_diagnoses = []
                    specific_diagnoses.append(''.join(values[1]))
                    specific_diagnoses = list(set(specific_diagnoses))
                    if len(specific_diagnoses) == 1:
                        value = specific_diagnoses[0]
                    elif len(specific_diagnoses) > 1:
                        value = 'MANUAL_REVIEW'
                    else:
                        value = None
                    if value is not None:
                        data_json[key0][key1][key2]['specificDxAtAcquisition'] = value
                    else:
                        del data_json[key0][key1][key2]['specificDxAtAcquisition']
                except Exception:
                    traceback.print_exc()
    return data_json
        
#
def specific_diagnosis_performance(validation_data_manager, evaluation_manager,
                                   labId, nlp_values, nlp_datum_key, 
                                   validation_datum_key, display_flg):
    validation_data = validation_data_manager.get_validation_data()
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
    performance = evaluation_manager.evaluation(nlp_value, validation_value,
                                                display_flg)
    return performance