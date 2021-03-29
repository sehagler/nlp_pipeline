# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 13:22:11 2020

@author: haglers
"""

#
from nlp_lib.py.processor_lib.preprocessor_lib.worker_lib.preprocessing_worker_class \
    import Preprocessing_worker
from projects_lib.BeatAML_Waves_1_And_2.py.cytogenetics_report_preprocessor_class \
    import Cytogenetics_report_preprocessor
from projects_lib.BeatAML_Waves_1_And_2.py.hematopathology_report_preprocessor_class \
    import Hematopathology_report_preprocessor
from projects_lib.BeatAML_Waves_1_And_2.py.beataml_waves_1_and_2_report_preprocessor_class \
    import BeatAML_Waves_1_And_2_report_preprocessor

#
class BeatAML_Waves_1_And_2_preprocessing_worker(Preprocessing_worker):
    
    #
    def __init__(self, project_data, preprocess_files_flg):
        Preprocessing_worker.__init__(self, project_data, preprocess_files_flg)
        self.beataml_report_preprocessor = BeatAML_Waves_1_And_2_report_preprocessor(project_data, 'formatted')
        self.cytogenetics_report_preprocessor = Cytogenetics_report_preprocessor(project_data, 'formatted')
        self.hematopathology_report_preprocessor = Hematopathology_report_preprocessor(project_data, 'formatted')
        
    #
    def _preprocess_documents(self, raw_data_reader, start_idx, document_ctr, 
                              fail_ctr, password):
        document_value_dict = raw_data_reader.get_document_values()
        for data_file in document_value_dict:
            for document_value_key in sorted(document_value_dict[data_file].keys()):
                for document_value in sorted(document_value_dict[data_file][document_value_key]):
                    data_tmp = raw_data_reader.get_data_by_document_value(data_file,
                                                                          document_value_key,
                                                                          document_value)
                    document_ctr, fail_ctr = \
                        self._preprocess_document(raw_data_reader, data_tmp, 
                                                  start_idx, document_ctr, 
                                                  fail_ctr, password)
        return document_ctr, fail_ctr
    
    #
    def _report_preprocessor(self, xml_metadata):
        if xml_metadata['NLP_PROCESS'] == 'BEATAML_REPORT':
            report_preprocessor = self.beataml_report_preprocessor
        elif xml_metadata['NLP_PROCESS'] == 'CYTOGENETICS_REPORT':
            report_preprocessor = self.cytogenetics_report_preprocessor
        elif xml_metadata['NLP_PROCESS'] == 'HEMATOPATHOLOGY_REPORT':
            report_preprocessor = self.hematopathology_report_preprocessor
        else:
            print('invalid NLP_PROCESS')
        return report_preprocessor