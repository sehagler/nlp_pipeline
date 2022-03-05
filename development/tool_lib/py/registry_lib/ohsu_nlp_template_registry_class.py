# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 18:24:06 2022

@author: haglers
"""

#
import os

#
class Ohsu_nlp_template_registry(object):
    
    #
    def __init__(self, static_data_manager):
        self._import_templates(static_data_manager)
        
    #
    def _import_templates(self, static_data_manager):
        static_data = static_data_manager.get_static_data()
        directory_manager = static_data['directory_manager']
        software_dir = directory_manager.pull_directory('software_dir')
        operation_mode = static_data['operation_mode']
        for file in os.listdir(software_dir + '/' + operation_mode + \
                               '/tool_lib/py/query_tools_lib'):
            filename, extension = os.path.splitext(file)
            import_cmd = 'from tool_lib.py.query_tools_lib.' + filename + \
                         ' import template as template_' + \
                         filename[:-6] 
            try:
                exec(import_cmd, globals())
                print('imported template_' + filename[:-6])
            except:
                pass
        
    #
    def get_template(self, filename):
        if filename in [ 'antigens.csv' ]:
            template, template_sections_list = template_antigens()
        elif filename in [ 'breast_cancer_tnm_stage.csv' ]:
            template, template_sections_list = template_tnm_stage()
        elif filename in [ 'fish_analysis_summary.csv' ]:
            template, template_sections_list = template_fish_analysis_summary()
        elif filename in [ 'karyotype.csv' ]:
            template, template_sections_list = template_karyotype()
        return template, template_sections_list