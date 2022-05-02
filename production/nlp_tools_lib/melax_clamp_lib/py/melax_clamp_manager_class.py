# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 09:56:24 2022

@author: haglers
"""

#
import os

#
from tool_lib.py.processing_tools_lib.file_processing_tools \
    import write_file

#
class Melax_clamp_manager(object):
    
    #
    def __init__(self, static_data_manager):
        self.static_data_manager = static_data_manager
    
    #
    def create_source_data_file(self, ctr, rpt_text):
        static_data = self.static_data_manager.get_static_data()
        directory_manager = static_data['directory_manager']
        outdir = directory_manager.pull_directory('melax_clamp_preprocessing_data_out')
        filename = str(ctr) + '.txt'
        write_file(os.path.join(outdir, filename), rpt_text, False, False)
        ret_val = True
        return ret_val