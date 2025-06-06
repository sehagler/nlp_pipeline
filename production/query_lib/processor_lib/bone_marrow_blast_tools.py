# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 15:52:26 2022

@author: haglers
"""

#
import traceback

#
from tools_lib.processing_tools_lib.variable_processing_tools \
    import trim_data_value
from query_lib.processor_lib.base_lib.blasts_tools_base \
    import Postprocessor as Postprocessor_base
from query_lib.processor_lib.base_lib.blasts_tools_base \
    import get_blast_value
    
#                 
def evaluate_bone_marrow_blast(data_json, manual_review):
    data_json_tmp = data_json
    for key0 in data_json_tmp.keys():
        for key1 in data_json_tmp[key0].keys():
            for key2 in data_json_tmp[key0][key1].keys():
                try:
                    blast_value_list = data_json_tmp[key0][key1][key2]['%.Blasts.in.BM']
                    blast_value_list = trim_data_value(blast_value_list)
                    value = get_blast_value(blast_value_list, manual_review)
                    if value is not None:
                        data_json[key0][key1][key2]['%.Blasts.in.BM'] = value
                    else:
                        del data_json[key0][key1][key2]['%.Blasts.in.BM']
                except Exception:
                    traceback.print_exc()
    return data_json
    
#
class Postprocessor(Postprocessor_base):
    pass
    
#
class Preprocessor(object):
    
    #
    def __init__(self, static_data_object, logger_object):
        self.static_data_object = static_data_object
        self.logger_object = logger_object
    
    #
    def run_object(self, text):
        return text