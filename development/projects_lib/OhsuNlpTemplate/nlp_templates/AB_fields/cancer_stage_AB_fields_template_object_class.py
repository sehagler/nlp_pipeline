# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 17:18:08 2022

@author: haglers
"""

#
from query_lib.processor_lib.cancer_stage_tools \
    import AB_fields_object
    
#
class Cancer_stage_AB_fields_template_object(AB_fields_object):
    
    #
    def __init__(self):
        AB_fields_object.__init__(self)