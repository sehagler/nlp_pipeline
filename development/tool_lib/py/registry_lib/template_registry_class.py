# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 11:20:31 2022

@author: haglers
"""

#
from tool_lib.py.query_tools_lib.karyotype_tools import template as karyotype_template
from tool_lib.py.query_tools_lib.tnm_stage_tools import template as tnm_template

#
class Template_registry(object):
    
    #
    def __init__(self, static_data_manager):
        self.static_data_manager = static_data_manager
        
    #
    def karyotype(self):
        return karyotype_template()
        
    #
    def tnm_template(self):
        return tnm_template()