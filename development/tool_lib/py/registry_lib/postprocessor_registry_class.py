# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 08:12:07 2018

@author: haglers
"""

#
import os
import traceback

#
from tool_lib.py.registry_lib.base_lib.postprocessor_registry_base_class \
    import Postprocessor_registry_base

#
class Postprocessor_registry(Postprocessor_registry_base):
    
    #
    def _import_postprocessors(self, static_data_manager):
        pass
    
    #
    def create_postprocessor(self, file):
        filename, extension = os.path.splitext(file)
        import_cmd = 'from tool_lib.py.query_tools_lib.' + filename + \
                     '_tools import Postprocessor'
        try:
            exec(import_cmd, globals())
            print('Postprocessor_' + filename + ' import succeeded')
            postprocessor_imported_flg = True
        except Exception:
            print('Postprocessor_' + filename + ' import failed')
            traceback.print_exc()
            postprocessor_imported_flg = False
        registration_cmd = 'self._register_postprocessor(' + \
                           '\'postprocessor_' + filename + '\', ' + \
                           'Postprocessor_' + filename + '(self.static_data))'
        if postprocessor_imported_flg:
            try:
                self._register_postprocessor('postprocessor_' + filename,
                                             Postprocessor(self.static_data))
                print(filename + ' registration succeeded')
            except Exception:
                traceback.print_exc()
                print(filename + ' registration failed')
     
    #
    def push_data_dict(self, filename, data_dict):
        if filename in [ 'antigens.csv' ]:
            self._push_data_dict('postprocessor_antigens', data_dict, filename=filename)
        elif filename in [ 'bone_marrow_blast.csv' ]:
            self._push_data_dict('postprocessor_bone_marrow_blast', data_dict, filename=filename)
        elif filename in [ 'breast_cancer_biomarkers_blocks_er.csv' ]:
            self._push_data_dict('postprocessor_breast_cancer_biomarkers_er', data_dict, idx=1)
        elif filename in [ 'breast_cancer_biomarkers_blocks_gata3.csv' ]:
            self._push_data_dict('postprocessor_breast_cancer_biomarkers_gata3', data_dict, idx=1)
        elif filename in [ 'breast_cancer_biomarkers_blocks_her2.csv' ]:
            self._push_data_dict('postprocessor_breast_cancer_biomarkers_her2', data_dict, idx=1)
        elif filename in [ 'breast_cancer_biomarkers_blocks_ki67.csv' ]:
            self._push_data_dict('postprocessor_breast_cancer_biomarkers_ki67', data_dict, idx=1)
        elif filename in [ 'breast_cancer_biomarkers_blocks_pr.csv' ]:
            self._push_data_dict('postprocessor_breast_cancer_biomarkers_pr', data_dict, idx=1)
        elif filename in [ 'breast_cancer_biomarkers_er.csv' ]:
            self._push_data_dict('postprocessor_breast_cancer_biomarkers_er', data_dict, filename=filename)
        elif filename in [ 'breast_cancer_biomarkers_gata3.csv' ]:
            self._push_data_dict('postprocessor_breast_cancer_biomarkers_gata3', data_dict, filename=filename)
        elif filename in [ 'breast_cancer_biomarkers_her2.csv' ]:
            self._push_data_dict('postprocessor_breast_cancer_biomarkers_her2', data_dict, filename=filename)
        elif filename in [ 'breast_cancer_biomarkers_ki67.csv' ]:
            self._push_data_dict('postprocessor_breast_cancer_biomarkers_ki67', data_dict, filename=filename)
        elif filename in [ 'breast_cancer_biomarkers_pr.csv' ]:
            self._push_data_dict('postprocessor_breast_cancer_biomarkers_pr', data_dict, filename=filename)
        elif filename in [ 'breast_cancer_biomarkers_variability_er.csv' ]:
            self._push_data_dict('postprocessor_breast_cancer_biomarkers_er', data_dict, idx=2)
        elif filename in [ 'breast_cancer_biomarkers_variability_gata3.csv' ]:
            self._push_data_dict('postprocessor_breast_cancer_biomarkers_gata3', data_dict, idx=2)
        elif filename in [ 'breast_cancer_biomarkers_variability_her2.csv' ]:
            self._push_data_dict('postprocessor_breast_cancer_biomarkers_her2', data_dict, idx=2)
        elif filename in [ 'breast_cancer_biomarkers_variability_ki67.csv' ]:
            self._push_data_dict('postprocessor_breast_cancer_biomarkers_ki67', data_dict, idx=2)
        elif filename in [ 'breast_cancer_biomarkers_variability_pr.csv' ]:
            self._push_data_dict('postprocessor_breast_cancer_biomarkers_pr', data_dict, idx=2)
        elif filename in [ 'tnm_staging.csv' ]:
            self._push_data_dict('postprocessor_tnm_staging', data_dict, filename=filename)
        elif filename in [ 'cancer_stage.csv' ]:
            self._push_data_dict('postprocessor_cancer_stage', data_dict, filename=filename)
        elif filename in [ 'diagnosis.csv' ]:
            self._push_data_dict('postprocessor_diagnosis', data_dict, filename=filename)
        elif filename in [ 'diagnosis_date.csv' ]:
            self._push_data_dict('postprocessor_diagnosis_date', data_dict, filename=filename)
        elif filename in [ 'ecog_status.csv' ]:
            self._push_data_dict('postprocessor_ecog_status', data_dict, filename=filename)
        elif filename in [ 'extramedullary_disease.csv' ]:
            self._push_data_dict('postprocessor_extramedullary_disease', data_dict, filename=filename)
        elif filename in [ 'fab_classification.csv' ]:
            self._push_data_dict('postprocessor_fab_classification', data_dict, filename=filename)
        elif filename in [ 'fish_analysis_summary.csv' ]:
            self._push_data_dict('postprocessor_fish_analysis_summary', data_dict, filename=filename)
        elif filename in [ 'immunophenotype.csv' ]:
            self._push_data_dict('postprocessor_immunophenotype', data_dict, filename=filename)
        elif filename in [ 'karyotype.csv' ]:
            self._push_data_dict('postprocessor_karyotype', data_dict, filename=filename)
        elif filename in [ 'peripheral_blood_blast.csv' ]:
            self._push_data_dict('postprocessor_peripheral_blood_blast', data_dict, filename=filename)
        elif filename in [ 'relapse_date.csv' ]:
            self._push_data_dict('postprocessor_relapse_date', data_dict, filename=filename)
        elif filename in [ 'residual_disease.csv' ]:
            self._push_data_dict('postprocessor_residual_disease', data_dict, filename=filename)
        elif filename in [ 'smoking_history.csv' ]:
            self._push_data_dict('postprocessor_smoking_history', data_dict, filename=filename)
        elif filename in [ 'smoking_products.csv' ]:
            self._push_data_dict('postprocessor_smoking_products', data_dict, filename=filename)
        elif filename in [ 'smoking_status.csv' ]:
            self._push_data_dict('postprocessor_smoking_status', data_dict, filename=filename)
        elif filename in [ 'tnm_staging.csv' ]:
            self._push_data_dict('postprocessor_tnm_staging', data_dict, filename=filename)