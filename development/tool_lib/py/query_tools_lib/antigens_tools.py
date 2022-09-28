# -*- coding: utf-8 -*-
"""
Created on Fri Mar 08 12:42:14 2019

@author: haglers
"""

#
import re

#
from lambda_lib.lambda_manager_class import Lambda_manager
from tool_lib.py.processing_tools_lib.text_processing_tools import substitution
from tool_lib.py.processing_tools_lib.variable_processing_tools \
    import trim_data_value
from tool_lib.py.query_tools_lib.base_lib.postprocessor_base_class \
    import Postprocessor_base
from tool_lib.py.query_tools_lib.base_lib.preprocessor_base_class \
    import Preprocessor_base
    
#
def cleanup_antigens(text):
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
class Preprocessor(Preprocessor_base):
    
    #
    def run_preprocessor(self):
        antigens = antigens_list()
        self.text = self.lambda_manager.lambda_conversion('HLA ?DR', self.text, 'HLA-DR')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)dim(-| (/ )?)partial', self.text, 'dim/partial')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)dim (/ )?variable', self.text, 'dim/variable')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)(bright|dim|low|moderate|partial|subset|variable)CD', self.text, ' CD')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)partial (/ )?dim', self.text, 'dim/partial')
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?<=CD) (?=[0-9])', self.text)
        self.text = \
            self.lambda_manager.contextual_lambda_conversion(antigens + '\(', '\(', self.text, ' (')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion(antigens + ' : ' + antigens, ' : ', self.text, ':')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion(antigens + ' / ' + antigens, ' / ', self.text, '/')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion(antigens + '-negative', '-negative', self.text, ' negative')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion(antigens + '-positive', '-positive', self.text, ' positive')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion(antigens + '-', '-', self.text, ' negative ')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion(antigens + ' *\+', '\+', self.text, ' positive ')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion(antigens + ' *\( \+ \)', '\( \+ \)', self.text, ' positive')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=HLA) (negative|positive)(?=DR)', self.text, '-')
            
 #
class Postprocessor(Postprocessor_base):

    #
    def _extract_data_value(self, value_list_dict):
        extracted_data_dict = {}
        for key in value_list_dict.keys():
            text_list = value_list_dict[key]
            value = []
            for item in text_list[0]:
                value.append(item[0])
            value_dict_list = []
            value_dict = {}
            value_dict['ANTIBODIES_TESTED'] = value
            value_dict_list.append(value_dict)
            extracted_data_dict[key] = value_dict_list
        return extracted_data_dict
    
#
def antibodies_tested_performance(validation_data_manager, evaluation_manager,
                                  labId, nlp_values, nlp_datum_key,
                                  validation_datum_key):
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
        validation_value = cleanup_antigens(validation_value)
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
    performance = evaluation_manager.evaluation(nlp_value, validation_value,
                                                display_flg)
    return performance

#
def antigens_list():
    return '([a-z]?CD[0-9]+|HLA-DR|MPO|T[Dd]T|Kappa|Lambda)'

#
def correct_antibodies(text):
    lambda_manager = Lambda_manager()
    text = lambda_manager.lambda_conversion('HLA *- *DR', text, 'HLA-DR')
    return text

#                 
def evaluate_antibodies_tested(data_json):
    data_json_tmp = data_json
    for key0 in data_json_tmp.keys():
        for key1 in data_json_tmp[key0].keys():
            for key2 in data_json_tmp[key0][key1].keys():
                try:
                    diagnoses = data_json_tmp[key0][key1][key2]['Antibodies.Tested']
                    diagnoses = trim_data_value(diagnoses)
                    diagnoses = list(set(diagnoses))
                    if len(diagnoses) == 1:
                        value = diagnoses[0]
                    elif len(diagnoses) > 1:
                        value = 'MANUAL_REVIEW'
                    else:
                        value = None
                    if value is not None:
                        data_json[key0][key1][key2]['Antibodies.Tested'] = value
                    else:
                        del data_json[key0][key1][key2]['Antibodies.Tested']
                except Exception:
                    traceback.print_exc()
    return data_json

#                 
def evaluate_surface_antigens(entry_label, data_json):
    '''
    data_json_tmp = data_json
    for key0 in data_json_tmp.keys():
        for key1 in data_json_tmp[key0].keys():
            for key2 in data_json_tmp[key0][key1].keys():
                try:
                    antigens = data_json_tmp[key0][key1][key2][entry_label]
                    antigens = trim_data_value(antigens)
                    antigens = prune_surface_antigens(antigens)
                    if len(antigens) == 1:
                        value = antigens[0]
                    elif len(antigens) > 1:
                        value = 'MANUAL_REVIEW'
                    else:
                        value = None
                    if value is not None:
                        data_json[key0][key1][key2][entry_label] = value
                    else:
                        del data_json[key0][key1][key2][entry_label]
                except Exception:
                    traceback.print_exc()
    '''
    return data_json

#
def extract_antigens(text):
    antigen_list = []
    tokens = text.split(' ')
    for token in tokens:
        if is_antibody(token):
            antigen_list.append(token)
    return antigen_list

#
def is_antibody(text, lower_flg=False):
    match_str = '^('
    match_str += '[a-z]?CD[0-9]+[a-z]?( \(subset\))?'
    match_str += '|HLA-DR'
    match_str += '|[a-z]?Kappa[a-z]?( \(mono\))?'
    match_str += '|[a-z]?Lambda[a-z]?( \(mono\))?'
    match_str += '|[a-z]?MPO'
    match_str += '|[a-z]?T[Dd]T'
    match_str += ')$'
    if lower_flg:
        match_str = match_str.lower()
    if re.match(match_str, text):
        return True
    else:
        return False
 
#
def is_antibody_value(text):
    match_str = '(?i)^('
    match_str += 'bright'
    match_str += '|dim(inished)?'
    match_str += '|focal'
    match_str += '|low'
    match_str += '|partial/dim'
    match_str += '|partial'
    match_str += '|variable'
    match_str += ')$'
    if re.match(match_str, text):
        return True
    else:
        return False
    
#
def prune_surface_antigens(antigens):
    if len(antigens) > 1:
        text_list = list(set(antigens))
        if len(text_list) > 1:
            drop_list = []
            for i in range(len(text_list)-1):
                for j in range(len(text_list)-i-1):
                    text0 = text_list[i]
                    text1 = text_list[j+i+1]
                    text_score = compare_texts(text0, text1, True)
                    if text_score[2] == 0:
                        drop_list.append(text1)
                    elif text_score[0] == 0 and text_score[1] == 0:
                        tokens0 = text0.split(' ')
                        tokens1 = text1.split(' ')
                        if len(tokens0) < len(tokens1):
                            drop_list.append(text0)
                        elif len(tokens0) > len(tokens1):
                            drop_list.append(text1)
            text_list = list(set(text_list) - set(drop_list)) 
        if len(text_list) > 1:
            drop_list = []
            for i in range(len(text_list)-1):
                for j in range(len(text_list)-i-1):
                    text0 = text_list[i]
                    text1 = text_list[j+i+1]
                    text_score = compare_texts(text0, text1, True)
                    if text_score[0] > 0 and text_score[1] == 0:
                        drop_list.append(text1)
                    elif text_score[0] == 0 and text_score[1] > 0:
                        drop_list.append(text0)
            text_list = list(set(text_list) - set(drop_list))
        antigens = text_list
    return antigens
    
#
def simple_template():
    antigens = '[a-z]?(CD[0-9]+|HLA-DR|MPO|T[Dd]T|Kappa|Lambda)[a-z]?'
    template = '(' + antigens + ' ?){2,}'
    template_list = []
    template_list.append(template)
    sections_list = [ 'ANTIBODIES TESTED' ]
    template_dict = {}
    template_dict['primary_template_list'] = template_list
    template_dict['sections_list'] = sections_list
    template_dict['template_headers'] = [ 'Antigens' ]
    return template_dict