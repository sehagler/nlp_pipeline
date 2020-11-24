# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 14:20:35 2020

@author: haglers
"""

#
from nlp_lib.py.manager_lib.process_manager_class import Process_manager
from nlp_lib.py.template_lib.preprocessor_template_lib.note_template_class import Note_template
from nlp_lib.py.template_lib.preprocessor_template_lib.pathology_report_class import Pathology_report

#
class AdverseEvents_process_manager(Process_manager):
    
    #
    def __init__(self, project_data, password):
        Process_manager.__init__(self, project_data, password)
        self.note_preprocessor = Note_template(project_data, 'unformatted')
        self.pathology_report_preprocessor = Pathology_report(project_data, 'unformatted')
        
    #
    def _preprocess_documents(self, raw_data_reader, start_idx, mrn_list, xml_metadata_keys, 
                              document_ctr, fail_ctr, do_beakerap_flg):
        document_numbers = raw_data_reader.get_document_numbers()
        for document_number in document_numbers:
            data_tmp = raw_data_reader.get_data_by_document_number(document_number)
            if bool(data_tmp):
                document_ctr, fail_ctr = self._preprocess_document(raw_data_reader, do_beakerap_flg, 
                                                                   data_tmp, start_idx, mrn_list, 
                                                                   xml_metadata_keys, document_ctr, fail_ctr)
        return document_ctr, fail_ctr
    
    #
    def _report_preprocessor(self, xml_metadata):
        if xml_metadata['NLP_PROCESS'] == 'NOTE':
            report_preprocessor = self.note_preprocessor
        else:
            report_preprocessor = self.pathology_report_preprocessor
        return report_preprocessor