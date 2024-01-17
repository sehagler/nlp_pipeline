# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 17:18:08 2022

@author: haglers
"""

#
from query_lib.processor_lib.karyotype_tools \
    import simple_template as karyotype_simple_template
 
#
class Karyotype_simple_template_object(object):
    
    #
    def simple_template(self):
        return karyotype_simple_template()