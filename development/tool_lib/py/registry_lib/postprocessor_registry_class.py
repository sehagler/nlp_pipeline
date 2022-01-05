# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 08:12:07 2018

@author: haglers
"""

#
from nlp_lib.py.base_lib.postprocessor_registry_base_class \
    import Postprocessor_registry_base
from tool_lib.py.query_tools_lib.blasts_tools \
    import Postprocessor as Postprocessor_blasts
from tool_lib.py.query_tools_lib.breast_cancer_biomarkers_tools \
    import Postprocessor as Postprocessor_breast_cancer_biomarkers
from tool_lib.py.query_tools_lib.cancer_stage_tools \
    import Postprocessor as Postprocessor_cancer_stage
from tool_lib.py.query_tools_lib.date_tools \
    import Postprocessor as Postprocessor_date
from tool_lib.py.query_tools_lib.ecog_tools \
    import Postprocessor as Postprocessor_ecog_score
from tool_lib.py.query_tools_lib.extramedullary_disease_tools \
    import Postprocessor as Postprocessor_extramedullary_disease
from tool_lib.py.query_tools_lib.fab_classification_tools \
    import Postprocessor as Postprocessor_fab_classification
from tool_lib.py.query_tools_lib.immunophenotype_tools \
    import Postprocessor as Postprocessor_immunophenotype
from tool_lib.py.query_tools_lib.residual_diagnosis_tools \
    import Postprocessor as Postprocessor_residual_diagnosis
from tool_lib.py.query_tools_lib.smoking_history_tools \
    import Postprocessor as Postprocessor_smoking_history
from tool_lib.py.query_tools_lib.smoking_products_tools \
    import Postprocessor as Postprocessor_smoking_products
from tool_lib.py.query_tools_lib.smoking_status_tools \
    import Postprocessor as Postprocessor_smoking_status

#
class Postprocessor_registry(Postprocessor_registry_base):
    
    #
    def create_postprocessor(self, filename):
        if filename in [ 'bone_marrow_blast.csv' ]:
            self._register_postprocessor('postprocessor_bone_marrow_blast',
                                         Postprocessor_blasts(self.static_data))
        elif filename in [ 'breast_cancer_biomarkers_er.csv' ]:
            self._register_postprocessor('postprocessor_breast_cancer_biomarkers_er',
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
        elif filename in [ 'cancer_stage.csv' ]:
            self._register_postprocessor('postprocessor_cancer_stage',
                                         Postprocessor_cancer_stage(self.static_data))
        elif filename in [ 'diagnosis_date.csv' ]:
            self._register_postprocessor('postprocessor_diagnosis_date',
                                         Postprocessor_date(self.static_data))
        elif filename in [ 'ecog_status.csv' ]:
            self._register_postprocessor('postprocessor_ecog_score',
                                         Postprocessor_ecog_score(self.static_data))
        elif filename in [ 'extramedullary_disease.csv' ]:
            self._register_postprocessor('postprocessor_extramedullary_disease',
                                         Postprocessor_extramedullary_disease(self.static_data))
        elif filename in [ 'fab_classification.csv' ]:
            self._register_postprocessor('postprocessor_fab_classification',
                                         Postprocessor_fab_classification(self.static_data))
        elif filename in [ 'immunophenotype.csv' ]:
            self._register_postprocessor('postprocessor_immunophenotype',
                                         Postprocessor_immunophenotype(self.static_data))
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
        if filename in [ 'bone_marrow_blast.csv' ]:
            self._push_data_dict('postprocessor_bone_marrow_blast', data_dict, filename=filename)
        elif filename in [ 'breast_cancer_biomarkers_blocks_er.csv' ]:
            self._push_data_dict('postprocessor_breast_cancer_biomarkers_er', data_dict, idx=1)
        elif filename in [ 'breast_cancer_biomarkers_blocks_her2.csv' ]:
            self._push_data_dict('postprocessor_breast_cancer_biomarkers_her2', data_dict, idx=1)
        elif filename in [ 'breast_cancer_biomarkers_blocks_ki67.csv' ]:
            self._push_data_dict('postprocessor_breast_cancer_biomarkers_ki67', data_dict, idx=1)
        elif filename in [ 'breast_cancer_biomarkers_blocks_pr.csv' ]:
            self._push_data_dict('postprocessor_breast_cancer_biomarkers_pr', data_dict, idx=1)
        elif filename in [ 'breast_cancer_biomarkers_er.csv' ]:
            self._push_data_dict('postprocessor_breast_cancer_biomarkers_er', data_dict, filename=filename)
        elif filename in [ 'breast_cancer_biomarkers_her2.csv' ]:
            self._push_data_dict('postprocessor_breast_cancer_biomarkers_her2', data_dict, filename=filename)
        elif filename in [ 'breast_cancer_biomarkers_ki67.csv' ]:
            self._push_data_dict('postprocessor_breast_cancer_biomarkers_ki67', data_dict, filename=filename)
        elif filename in [ 'breast_cancer_biomarkers_pr.csv' ]:
            self._push_data_dict('postprocessor_breast_cancer_biomarkers_pr', data_dict, filename=filename)
        elif filename in [ 'cancer_stage.csv' ]:
            self._push_data_dict('postprocessor_cancer_stage', data_dict, filename=filename)
        elif filename in [ 'diagnosis_date.csv' ]:
            self._push_data_dict('postprocessor_diagnosis_date', data_dict, filename=filename)
        elif filename in [ 'ecog_status.csv' ]:
            self._push_data_dict('postprocessor_ecog_score', data_dict, filename=filename)
        elif filename in [ 'extramedullary_disease.csv' ]:
            self._push_data_dict('postprocessor_extramedullary_disease', data_dict, filename=filename)
        elif filename in [ 'fab_classification.csv' ]:
            self._push_data_dict('postprocessor_fab_classification', data_dict, filename=filename)
        elif filename in [ 'immunophenotype.csv' ]:
            self._push_data_dict('postprocessor_immunophenotype', data_dict, filename=filename)
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