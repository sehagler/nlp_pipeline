# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 08:12:07 2018

@author: haglers
"""

#
import os

#
from nlp_lib.py.postprocessing_lib.output_manager_class import Output_manager
from tool_lib.py.query_tools_lib.blasts_tools \
    import Postprocessor as Postprocessor_blasts
from tool_lib.py.query_tools_lib.block_tools \
    import Postprocessor as Postprocessor_block
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
class Postprocessing_manager(object):
    
    #
    def __init__(self, static_data_manager, metadata_manager):
        self.static_data = static_data_manager.get_static_data()
        directory_manager = self.static_data['directory_manager']
        self.output_manager = Output_manager(self.static_data, 
                                             metadata_manager)
        self.output_manager.set_data_dirs(directory_manager)
        self.data_dict_classes_list = []
    
    #
    def cleanup_json_files_dir(self):
        self.output_manager.cleanup_json_files_dir()

    #
    def create_json_files(self):
        self.output_manager.create_json_files()
        
    #
    def import_reports(self):
        self.output_manager.merge_data_dict_lists()
        self.output_manager.include_metadata()
        self.output_manager.include_text()
        self.merged_dict_list = self.output_manager.get_data()
        
    #
    def select_postprocessor(self, filename, data_dict):
        print('Processing ' + filename)
        if filename in [ 'bone_marrow_blast.csv',
                         'peripheral_blood_blast.csv' ]:
            self.output_manager.append(Postprocessor_blasts(self.static_data,
                                                            filename,
                                                            data_dict))
        elif filename in [ 'block.csv' ]:
            self.output_manager.append(Postprocessor_block(self.static_data,
                                                           filename,
                                                           data_dict))
        elif filename in [ 'breast_cancer_biomarkers_er.csv', 
                           'breast_cancer_biomarkers_her2.csv',
                           'breast_cancer_biomarkers_ki67.csv',
                           'breast_cancer_biomarkers_pr.csv' ]:
            self.output_manager.append(Postprocessor_breast_cancer_biomarkers(self.static_data,
                                                                              filename,
                                                                              data_dict))
        elif filename in [ 'cancer_stage.csv' ]:
            self.output_manager.append(Postprocessor_cancer_stage(self.static_data,
                                                                  filename,
                                                                  data_dict))
        elif filename in [ 'diagnosis_date.csv' ]:
            self.output_manager.append(Postprocessor_date(self.static_data,
                                                          filename,
                                                          data_dict))
        elif filename in [ 'ecog_status.csv' ]:
            self.output_manager.append(Postprocessor_ecog_score(self.static_data,
                                                                filename,
                                                                data_dict))
        elif filename in [ 'extramedullary_disease.csv' ]:
            self.output_manager.append(Postprocessor_extramedullary_disease(self.static_data,
                                                                            filename,
                                                                            data_dict))
        elif filename in [ 'fab_classification.csv' ]:
            self.output_manager.append(Postprocessor_fab_classification(self.static_data,
                                                                        filename,
                                                                        data_dict))
        elif filename in [ 'immunophenotype.csv' ]:
            self.output_manager.append(Postprocessor_immunophenotype(self.static_data,
                                                                     filename,
                                                                     data_dict))
        elif filename in [ 'relapse_date.csv' ]:
            self.output_manager.append(Postprocessor_date(self.static_data,
                                                          filename, data_dict))
        elif filename in [ 'residual_disease.csv' ]:
            self.output_manager.append(Postprocessor_residual_diagnosis(self.static_data,
                                                                        filename,
                                                                        data_dict))
        elif filename in [ 'smoking_history.csv' ]:
            self.output_manager.append(Postprocessor_smoking_history(self.static_data,
                                                                     filename,
                                                                     data_dict))
        elif filename in [ 'smoking_products.csv' ]:
            self.output_manager.append(Postprocessor_smoking_products(self.static_data,
                                                                      filename,
                                                                      data_dict))
        elif filename in [ 'smoking_status.csv' ]:
            self.output_manager.append(Postprocessor_smoking_status(self.static_data,
                                                                    filename,
                                                                    data_dict))