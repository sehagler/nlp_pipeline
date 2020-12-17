# -*- coding: utf-8 -*-
"""
Created on Fri Mar 01 15:48:21 2019

@author: haglers
"""

#
import re
import xlrd

#
from nlp_lib.py.tool_lib.query_tools_lib.antigens_tools import is_antibody, is_antibody_value
from nlp_lib.py.tool_lib.query_tools_lib.blasts_tools import get_blast_value
from nlp_lib.py.tool_lib.processing_tools_lib.text_processing_tools import substitution
from projects_lib.BeatAML_Waves_3_And_4.py.project_lib.packaging_base_class \
    import Packaging_base

#
class Gold_standard_jsons(Packaging_base):
    
    #
    def __init__(self, directory_manager, mrn_list):
        self.deidentifier_xlsx = directory_manager.pull_directory('raw_data_dir') + \
            '/wave3&4_unique_OHSU_clinical_summary_11_17_2020.xlsx'
        self.gpld_standard_xlsx = directory_manager.pull_directory('raw_data_dir') + \
            '/wave3&4_unique_OHSU_clinical_summary_11_17_2020.xlsx'
        self.mrn_list = mrn_list
        deidentifier_key_dict = self._get_deidentifier_keys()
        labIds_list = []
        patientIds_list = []
        for mrn in self.mrn_list:
            try:
                patientIds_list.append(deidentifier_key_dict[mrn]['patientId'])
                labIds_list.extend(deidentifier_key_dict[mrn]['labIds'].values())
            except:
                pass
        self.data_json = self._get_data_dict(patientIds_list, labIds_list)
        
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
    def _get_antibodies_dict(self, text):
        text = re.sub('(?i)(\+|\-positive)', '', text)
        text = substitution('([a-z]?CD[0-9]+|HLA-DR|MPO|T[Dd]T) and (?!([a-z]CD|CD[0-9]|HLA|MPO|T[Dd]T))',
                            {' and ' : ' ; '}, text)
        text_chunks = text.split(';')
        text_lists = []
        for text_chunk in text_chunks:
            text_lists.append(text_chunk.split())
        antibodies = list(set(text.split()))
        nonantibodies = []
        for element in antibodies:
            if not is_antibody(element):
                nonantibodies.append(element)
        nonantibodies = list(set(nonantibodies))
        for nonantibody in nonantibodies:
            antibodies.remove(nonantibody)
        antibodies.sort()
        antibody_dict = {}
        for antibody in antibodies:
            antibody_dict[antibody] = [ 'NO VALUE' ]
        for antibody_dict_key in antibody_dict.keys():
            for text_list in text_lists:
                if 'negative' in text_list or \
                   'without' in text_list:
                    polarity = 'negative'
                else:
                    polarity = 'positive'
                idxs = [ j for j, e in enumerate(text_list) if e == antibody_dict_key ]
                antibody_value_list = []
                for idx in idxs:
                    antibody_value = polarity
                    try:
                        if is_antibody_value(text_list[idx-1]):
                            antibody_value = text_list[idx-1].lower()
                    except:
                        pass
                    try:
                        if text_list[idx+1] == is_antibody_value(text_list[idx+1]):
                            antibody_value = text_list[idx+1].lower()
                    except:
                        pass
                    try:
                        if text_list[idx+1] == '(' and is_antibody_value(text_list[idx+2]):
                            antibody_value = text_list[idx+2].lower()
                    except:
                        pass
                    antibody_value_list.append(antibody_value)
                if len(antibody_value_list) > 0:
                    antibody_dict[antibody_dict_key] = antibody_value_list
        return(antibody_dict)
        
    #
    def _get_data_dict(self, patientIds_list, labIds_list):
        data_dict = {}
        book = xlrd.open_workbook(self.gpld_standard_xlsx)
        sheet = book.sheet_by_index(0)
        labIds = sheet.col_values(0)[1:]
        patientIds = sheet.col_values(3)[1:]
        antibodies_tested = sheet.col_values(163)[1:]
        bone_marrow_blasts = self._make_strings(sheet.col_values(62)[1:])
        diagnoses = self._make_strings(sheet.col_values(29)[1:])
        diagnosis_date = sheet.col_values(164)[1:]
        fab_morphology = sheet.col_values(165)[1:]
        fish_analysis_summary = relapse_date = sheet.col_values(167)[1:]
        karyotype = sheet.col_values(77)[1:]
        peripheral_blood_blasts = self._make_strings(sheet.col_values(63)[1:])
        relapse_date = sheet.col_values(166)[1:]
        residual_diagnosis = sheet.col_values(168)[1:]
        specific_diagnoses = self._make_strings(sheet.col_values(30)[1:])
        surface_antigens = sheet.col_values(82)[1:]
        for i in range(len(labIds)):
            if labIds[i] in labIds_list:
                patientId = str(int(patientIds[i]))
                if patientId in patientIds_list:
                    if patientId not in data_dict.keys():
                        data_dict[patientId] = {}
                    if labIds[i] not in data_dict[patientId].keys():
                        data_dict[patientId][labIds[i]] = {}
                    data_dict[patientId][labIds[i]]['Antibodies.Tested'] = \
                        self._cleanup_antigens(antibodies_tested[i])
                    data_dict[patientId][labIds[i]]['dx'] = \
                        self._normalize_diagnosis(diagnoses[i])
                    data_dict[patientId][labIds[i]]['dx.Date'] = \
                        diagnosis_date[i]
                    data_dict[patientId][labIds[i]]['FAB/Blast.Morphology'] = \
                        fab_morphology[i]
                    data_dict[patientId][labIds[i]]['FISH.Analysis.Summary'] = \
                        fish_analysis_summary[i]
                    data_dict[patientId][labIds[i]]['Karyotype'] = \
                        karyotype[i]
                    data_dict[patientId][labIds[i]]['%.Blasts.in.BM'] = \
                        get_blast_value([bone_marrow_blasts[i]])
                    data_dict[patientId][labIds[i]]['%.Blasts.in.PB'] = \
                        get_blast_value([peripheral_blood_blasts[i]])
                    data_dict[patientId][labIds[i]]['Relapse.Date'] = \
                        relapse_date[i]
                    data_dict[patientId][labIds[i]]['Residual.dx'] = \
                        residual_diagnosis[i]
                    data_dict[patientId][labIds[i]]['specificDx'] = \
                        self._normalize_diagnosis(specific_diagnoses[i])
                    data_dict[patientId][labIds[i]]['Surface.Antigens.(Immunohistochemical.Stains)'] = \
                        self._cleanup_antigens(surface_antigens[i])
        return data_dict
        
    #
    def _normalize_diagnosis(self, text):
        text = re.sub('LEUKAEMIA', 'LEUKEMIA', text)
        text = re.sub('leukaemia', 'leukemia', text)
        return(text)