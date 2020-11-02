# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 14:20:35 2020

@author: haglers
"""

#
from nlp_lib.py.manager_lib.process_manager_class import Process_manager
from projects_lib.BreastCancerPathology.py.breastcancerpathology_preprocessor_class \
    import BreastCancerPathology_preprocessor

#
class BreastCancerPathology_process_manager(Process_manager):
    
    #
    def __init__(self, project_data, server):
        Process_manager.__init__(self, project_data, server)
        self.report_preprocessor = BreastCancerPathology_preprocessor()
        
    #
    def _preprocess_documents(self, raw_data_reader, start_idx, mrn_list, xml_metadata_keys, 
                              document_ctr, fail_ctr, do_beakerap_flg):
        document_value_dict = raw_data_reader.get_document_values()
        for data_file in document_value_dict:
            for document_value_key in sorted(document_value_dict[data_file].keys()):
                for document_value in sorted(document_value_dict[data_file][document_value_key]):
                    data_tmp = raw_data_reader.get_data_by_document_value(data_file, document_value_key, document_value)
                    document_ctr, fail_ctr = self._preprocess_document(raw_data_reader, do_beakerap_flg, 
                                                                       data_tmp, start_idx, mrn_list, 
                                                                       xml_metadata_keys, document_ctr,
                                                                       fail_ctr)
        return document_ctr, fail_ctr
    
    #
    def _report_preprocessor(self, xml_metadata):
        return self.report_preprocessor