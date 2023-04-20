# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 08:12:07 2018

@author: haglers
"""

#
import os
import traceback

#
from base_lib.postprocessor_registry_base_class \
    import Postprocessor_registry_base

#
class Postprocessor_registry(Postprocessor_registry_base):
    
    #
    def _import_postprocessors(self, static_data_object):
        pass
    
    #
    def create_postprocessor(self, file):
        filename, extension = os.path.splitext(file)
        import_cmd = 'from query_lib.processor_lib.' + filename + \
                     '_tools import Postprocessor'
        try:
            exec(import_cmd, globals())
            print('Postprocessor_' + filename + ' import succeeded')
            postprocessor_imported_flg = True
        except Exception:
            print('Postprocessor_' + filename + ' import failed')
            traceback.print_exc()
            postprocessor_imported_flg = False
        if postprocessor_imported_flg:
            try:
                self._register_postprocessor('postprocessor_' + filename,
                                             Postprocessor(self.static_data_object))
                print(filename + ' registration succeeded')
            except Exception:
                traceback.print_exc()
                print(filename + ' registration failed')
     
    #
    def push_data_dict(self, filename, data_dict, sections_data_dict):
        print(filename)
        if filename in [ 'breast_cancer_biomarkers_blocks_er.csv' ]:
            self._push_data_dict('postprocessor_breast_cancer_biomarkers_er', 
                                 data_dict, sections_data_dict, idx=1)
        elif filename in [ 'breast_cancer_biomarkers_blocks_gata3.csv' ]:
            self._push_data_dict('postprocessor_breast_cancer_biomarkers_gata3',
                                 data_dict, sections_data_dict, idx=1)
        elif filename in [ 'breast_cancer_biomarkers_blocks_her2.csv' ]:
            self._push_data_dict('postprocessor_breast_cancer_biomarkers_her2',
                                 data_dict, sections_data_dict, idx=1)
        elif filename in [ 'breast_cancer_biomarkers_blocks_ki67.csv' ]:
            self._push_data_dict('postprocessor_breast_cancer_biomarkers_ki67',
                                 data_dict, sections_data_dict, idx=1)
        elif filename in [ 'breast_cancer_biomarkers_blocks_pr.csv' ]:
            self._push_data_dict('postprocessor_breast_cancer_biomarkers_pr',
                                 data_dict, sections_data_dict, idx=1)
        elif filename in [ 'breast_cancer_biomarkers_variability_er.csv' ]:
            self._push_data_dict('postprocessor_breast_cancer_biomarkers_er',
                                 data_dict, sections_data_dict, idx=2)
        elif filename in [ 'breast_cancer_biomarkers_variability_gata3.csv' ]:
            self._push_data_dict('postprocessor_breast_cancer_biomarkers_gata3',
                                 data_dict, sections_data_dict, idx=2)
        elif filename in [ 'breast_cancer_biomarkers_variability_her2.csv' ]:
            self._push_data_dict('postprocessor_breast_cancer_biomarkers_her2',
                                 data_dict, sections_data_dict, idx=2)
        elif filename in [ 'breast_cancer_biomarkers_variability_ki67.csv' ]:
            self._push_data_dict('postprocessor_breast_cancer_biomarkers_ki67',
                                 data_dict, sections_data_dict, idx=2)
        elif filename in [ 'breast_cancer_biomarkers_variability_pr.csv' ]:
            self._push_data_dict('postprocessor_breast_cancer_biomarkers_pr',
                                 data_dict, sections_data_dict, idx=2)
        else:
            filename_base, extension = os.path.splitext(filename)
            if extension == '.csv' and filename_base != 'sections':
                self._push_data_dict('postprocessor_' + filename_base, data_dict, 
                                     sections_data_dict, filename=filename)