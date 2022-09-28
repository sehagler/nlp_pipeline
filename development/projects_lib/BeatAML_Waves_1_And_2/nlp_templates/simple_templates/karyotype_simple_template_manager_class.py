# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 17:18:08 2022

@author: haglers
"""

#
from tool_lib.py.query_tools_lib.karyotype_tools \
    import simple_template as karyotype_simple_template
 
#
class Karyotype_simple_template_manager(object):
    
    #
    def __init__(self, static_data_manager):
        self.static_data_manager = static_data_manager
     
    #
    def simple_template(self):
        return karyotype_simple_template()