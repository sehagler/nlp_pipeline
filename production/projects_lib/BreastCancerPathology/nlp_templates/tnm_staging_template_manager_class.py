# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 17:18:08 2022

@author: haglers
"""

#
from tool_lib.py.query_tools_lib.tnm_staging_tools \
    import template as tnm_staging_template

#
class Tnm_staging_template_manager(object):
    
    #
    def __init__(self, static_data_manager):
        self.static_data_manager = static_data_manager
    
    #
    def template(self):
        return tnm_staging_template()