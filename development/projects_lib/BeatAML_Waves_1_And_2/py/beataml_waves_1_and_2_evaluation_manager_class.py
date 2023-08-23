# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 16:03:49 2022

@author: haglers
"""

#
from nlp_pipeline_lib.manager_lib.evaluation_lib.evaluation_manager_class \
    import Evaluation_manager

#
class BeatAML_Waves_1_And_2_evaluation_manager(Evaluation_manager):
    
    #
    def __init__(self, static_data_object, directory_object, logger_object,
                 evaluator_registry):
        self.evaluator_registry = evaluator_registry
        self.evaluation_manager = \
            Evaluation_manager(static_data_object, directory_object,
                               logger_object, evaluator_registry)
    
    #
    def evaluation(self, arg_dict):
        display_flg = arg_dict['display_flg']
        nlp_value = arg_dict['nlp_value']
        validation_datum_key = arg_dict['validation_datum_key']
        validation_value = arg_dict['validation_value']
        performance = None
        if validation_datum_key == '%.Blasts.in.BM' or\
           validation_datum_key == '%.Blasts.in.PB':
            performance = \
                self.evaluator_registry.run_evaluator_a('blasts_tools_base',
                                                        self.evaluation_manager, 
                                                        nlp_value,
                                                        validation_value,
                                                        display_flg, 5.0)
        elif validation_datum_key == 'Antibodies.Tested':
            performance = \
                self.evaluator_registry.run_evaluator('antigens_tools',
                                                      self.evaluation_manager, 
                                                      nlp_value,
                                                      validation_value,
                                                      display_flg)
        elif validation_datum_key == 'Extramedullary.dx':
            performance = \
                self.evaluator_registry.run_evaluator('extramedullary_disease_tools',
                                                      self.evaluation_manager, 
                                                      nlp_value,
                                                      validation_value,
                                                      display_flg)
        elif validation_datum_key == 'FAB/Blast.Morphology':
            performance = \
                self.evaluator_registry.run_evaluator('fab_classification_tools',
                                                      self.evaluation_manager, 
                                                      nlp_value,
                                                      validation_value,
                                                      display_flg)
        elif validation_datum_key == 'FISH.Analysis.Summary':
            performance = \
                self.evaluator_registry.run_evaluator('fish_analysis_summary_tools',
                                                      self.evaluation_manager, 
                                                      nlp_value,
                                                      validation_value,
                                                      display_flg)
        elif validation_datum_key == 'Karyotype':
            performance = \
                self.evaluator_registry.run_evaluator('karyotype_tools',
                                                      self.evaluation_manager, 
                                                      nlp_value,
                                                      validation_value,
                                                      display_flg)
        elif validation_datum_key == 'Relapse.Date':
            performance = \
                self.evaluator_registry.run_evaluator('relapse_date_tools',
                                                      self.evaluation_manager, 
                                                      nlp_value,
                                                      validation_value,
                                                      display_flg)
        elif validation_datum_key == 'Residual.dx':
            performance = \
                self.evaluator_registry.run_evaluator('residual_disease_tools',
                                                      self.evaluation_manager, 
                                                      nlp_value,
                                                      validation_value,
                                                      display_flg)
        elif validation_datum_key == 'Surface.Antigens.(Immunohistochemical.Stains)':
            performance = \
                self.evaluator_registry.run_evaluator('immunophenotype_tools',
                                                      self.evaluation_manager, 
                                                      nlp_value,
                                                      validation_value,
                                                      display_flg)
        elif validation_datum_key == 'dxAtSpecimenAcquisition':
            performance = \
                self.evaluator_registry.run_evaluator('diagnosis_tools',
                                                      self.evaluation_manager, 
                                                      nlp_value,
                                                      validation_value,
                                                      display_flg)
        elif validation_datum_key == 'dx.Date':
            performance = \
                self.evaluator_registry.run_evaluator('diagnosis_date_tools',
                                                      self.evaluation_manager, 
                                                      nlp_value,
                                                      validation_value,
                                                      display_flg)
        elif validation_datum_key == 'specificDxAtAcquisition':
            performance = \
                self.evaluator_registry.run_evaluator('specific_diagnosis_tools',
                                                      self.evaluation_manager, 
                                                      nlp_value,
                                                      validation_value,
                                                      display_flg)
        arg_dict['performance'] = performance
        return arg_dict