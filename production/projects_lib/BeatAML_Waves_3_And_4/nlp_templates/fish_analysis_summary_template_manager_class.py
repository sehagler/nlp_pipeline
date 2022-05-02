# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 17:18:08 2022

@author: haglers
"""

#
from tool_lib.py.query_tools_lib.fish_analysis_summary_tools \
    import template as fish_analysis_summary_template

#
class Fish_analysis_summary_template_manager(object):
    
    #
    def __init__(self, static_data_manager):
        self.static_data_manager = static_data_manager
        
    #
    def template(self):
        return fish_analysis_summary_template()