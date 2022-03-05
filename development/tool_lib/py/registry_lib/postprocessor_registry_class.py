# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 08:12:07 2018

@author: haglers
"""

#
import os

#
from nlp_lib.py.base_lib.postprocessor_registry_base_class \
    import Postprocessor_registry_base

#
class Postprocessor_registry(Postprocessor_registry_base):
    
    #
    def _import_postprocessors(self, static_data_manager):
        static_data = static_data_manager.get_static_data()
        directory_manager = static_data['directory_manager']
        software_dir = directory_manager.pull_directory('software_dir')
        operation_mode = static_data['operation_mode']
        for file in os.listdir(software_dir + '/' + operation_mode + \
                               '/tool_lib/py/query_tools_lib'):
            filename, extension = os.path.splitext(file)
            import_cmd = 'from tool_lib.py.query_tools_lib.' + filename + \
                         ' import Postprocessor as Postprocessor_' + \
                         filename[:-6] 
            try:
                exec(import_cmd, globals())
                print('imported Postprocessor_' + filename[:-6])
            except:
                pass
    
    #
    def create_postprocessor(self, filename):
        if filename in [ 'antigens.csv' ]:
            self._register_postprocessor('postprocessor_antigens',
                                         Postprocessor_antigens(self.static_data))
        elif filename in [ 'bone_marrow_blast.csv' ]:
            self._register_postprocessor('postprocessor_bone_marrow_blast',
                                         Postprocessor_blasts(self.static_data))
        elif filename in [ 'breast_cancer_biomarkers_er.csv' ]:
            self._register_postprocessor('postprocessor_breast_cancer_biomarkers_er',
                                         Postprocessor_breast_cancer_biomarkers(self.static_data))
        elif filename in [ 'breast_cancer_biomarkers_gata3.csv' ]:
            self._register_postprocessor('postprocessor_breast_cancer_biomarkers_gata3',
                                         Postprocessor_breast_cancer_biomarkers(self.static_data))
        elif filename in [ 'breast_cancer_biomarkers_her2.csv' ]:
            self._register_postprocessor('postprocessor_breast_cancer_biomarkers_her2',
                                         Postprocessor_breast_cancer_biomarkers(self.static_data))
        elif filename in [ 'breast_cancer_biomarkers_ki67.csv' ]:
            self._register_postprocessor('postprocessor_breast_cancer_biomarkers_ki67',
                                         Postprocessor_breast_cancer_biomarkers(self.static_data))
        elif filename in [ 'breast_cancer_biomarkers_pr.csv' ]:
            self._register_postprocessor('postprocessor_breast_cancer_biomarkers_pr',
                                         Postprocessor_breast_cancer_biomarkers(self.static_data))
        elif filename in [ 'breast_cancer_tnm_stage.csv' ]:
            self._register_postprocessor('postprocessor_tnm_stage',
                                         Postprocessor_tnm_stage(self.static_data))
        elif filename in [ 'cancer_stage.csv' ]:
            self._register_postprocessor('postprocessor_cancer_stage',
                                         Postprocessor_cancer_stage(self.static_data))
        elif filename in [ 'diagnosis_date.csv' ]:
            self._register_postprocessor('postprocessor_diagnosis_date',
                                         Postprocessor_date(self.static_data))
        elif filename in [ 'ecog_status.csv' ]:
            self._register_postprocessor('postprocessor_ecog',
                                         Postprocessor_ecog(self.static_data))
        elif filename in [ 'extramedullary_disease.csv' ]:
            self._register_postprocessor('postprocessor_extramedullary_disease',
                                         Postprocessor_extramedullary_disease(self.static_data))
        elif filename in [ 'fab_classification.csv' ]:
            self._register_postprocessor('postprocessor_fab_classification',
                                         Postprocessor_fab_classification(self.static_data))
        elif filename in [ 'fish_analysis_summary.csv' ]:
            self._register_postprocessor('postprocessor_fish_analysis_summary',
                                         Postprocessor_fish_analysis_summary(self.static_data))
        elif filename in [ 'immunophenotype.csv' ]:
            self._register_postprocessor('postprocessor_immunophenotype',
                                         Postprocessor_immunophenotype(self.static_data))
        elif filename in [ 'karyotype.csv' ]:
            self._register_postprocessor('postprocessor_karyotype',
                                         Postprocessor_karyotype(self.static_data))
        elif filename in [ 'peripheral_blood_blast.csv' ]:
            self._register_postprocessor('postprocessor_peripheral_blood_blast',
                                         Postprocessor_blasts(self.static_data))
        elif filename in [ 'relapse_date.csv' ]:
            self._register_postprocessor('postprocessor_relapse_date',
                                         Postprocessor_date(self.static_data))
        elif filename in [ 'residual_disease.csv' ]:
            self._register_postprocessor('postprocessor_residual_diagnosis',
                                         Postprocessor_residual_diagnosis(self.static_data))
        elif filename in [ 'smoking_history.csv' ]:
            self._register_postprocessor('postprocessor_smoking_history',
                                         Postprocessor_smoking_history(self.static_data))
        elif filename in [ 'smoking_products.csv' ]:
            self._register_postprocessor('postprocessor_smoking_products',
                                         Postprocessor_smoking_products(self.static_data))
        elif filename in [ 'smoking_status.csv' ]:
            self._register_postprocessor('postprocessor_smoking_status',
                                         Postprocessor_smoking_status(self.static_data))
     
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
        elif filename in [ 'breast_cancer_tnm_stage.csv' ]:
            self._push_data_dict('postprocessor_tnm_stage', data_dict, filename=filename)
        elif filename in [ 'cancer_stage.csv' ]:
            self._push_data_dict('postprocessor_cancer_stage', data_dict, filename=filename)
        elif filename in [ 'diagnosis_date.csv' ]:
            self._push_data_dict('postprocessor_diagnosis_date', data_dict, filename=filename)
        elif filename in [ 'ecog_status.csv' ]:
            self._push_data_dict('postprocessor_ecog', data_dict, filename=filename)
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
            self._push_data_dict('postprocessor_residual_diagnosis', data_dict, filename=filename)
        elif filename in [ 'smoking_history.csv' ]:
            self._push_data_dict('postprocessor_smoking_history', data_dict, filename=filename)
        elif filename in [ 'smoking_products.csv' ]:
            self._push_data_dict('postprocessor_smoking_products', data_dict, filename=filename)
        elif filename in [ 'smoking_status.csv' ]:
            self._push_data_dict('postprocessor_smoking_status', data_dict, filename=filename)