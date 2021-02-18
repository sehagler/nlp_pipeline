# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 14:20:35 2020

@author: haglers
"""

#
from nlp_lib.py.processor_lib.preprocessor_lib.worker_lib.preprocessing_worker_class \
    import Preprocessing_worker
from nlp_lib.py.template_lib.preprocessor_template_lib.pathology_report_class  import Pathology_report
from projects_lib.CCC19.py.ccc19_note_preprocessor_class import CCC19_note_preprocessor

#
class CCC19_preprocessing_worker(Preprocessing_worker):
    
    #
    def __init__(self, project_data, preprocess_files_flg):
        Preprocessing_worker.__init__(self, project_data, preprocess_files_flg)
        self.note_preprocessor = CCC19_note_preprocessor(project_data, 'unformatted')
        self.pathology_report_preprocessor = Pathology_report(project_data, 'unformatted')
        
    #
    def _preprocess_documents(self, raw_data_reader, start_idx,
                              document_ctr, fail_ctr):
        document_numbers = raw_data_reader.get_document_numbers()
        for document_number in document_numbers:
            data_tmp = raw_data_reader.get_data_by_document_number(document_number)
            if bool(data_tmp):
                document_ctr, fail_ctr = self._preprocess_document(raw_data_reader, 
                                                                   data_tmp, start_idx, 
                                                                   document_ctr, fail_ctr)
        return document_ctr, fail_ctr
    
    #
    def _report_preprocessor(self, xml_metadata):
        if xml_metadata['NLP_PROCESS'] == 'NOTE':
            report_preprocessor = self.note_preprocessor
        else:
            report_preprocessor = self.pathology_report_preprocessor
        return report_preprocessor