# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 16:03:49 2022

@author: haglers
"""

#
from nlp_pipeline_lib.manager_lib.evaluation_lib.evaluation_manager_class \
    import Evaluation_manager

#
class BeatAML_Waves_3_And_4_evaluation_manager(object):
    
    #
    def __init__(self, static_data_object, logger_object, evaluator_registry):
        self.evaluator_registry = evaluator_registry
        self.evaluation_manager = \
            Evaluation_manager(static_data_object, logger_object,
                               evaluator_registry)
    
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
                self.evaluator_registry.run_object_a('blasts_tools_base',
                                                        self.evaluation_manager, 
                                                        nlp_value,
                                                        validation_value,
                                                        display_flg, 5.0)
        elif validation_datum_key == 'Antibodies.Tested':
            performance = \
                self.evaluator_registry.run_object('antigens_tools',
                                                      self.evaluation_manager, 
                                                      nlp_value,
                                                      validation_value,
                                                      display_flg)
        elif validation_datum_key == 'Extramedullary.dx':
            performance = \
                self.evaluator_registry.run_object('extramedullary_disease_tools',
                                                      self.evaluation_manager, 
                                                      nlp_value,
                                                      validation_value,
                                                      display_flg)
        elif validation_datum_key == 'FAB/Blast.Morphology':
            performance = \
                self.evaluator_registry.run_object('fab_classification_tools',
                                                      self.evaluation_manager, 
                                                      nlp_value,
                                                      validation_value,
                                                      display_flg)
        elif validation_datum_key == 'FISH.Analysis.Summary':
            performance = \
                self.evaluator_registry.run_object('fish_analysis_summary_tools',
                                                      self.evaluation_manager, 
                                                      nlp_value,
                                                      validation_value,
                                                      display_flg)
        elif validation_datum_key == 'karyotype':
            performance = \
                self.evaluator_registry.run_object('karyotype_tools',
                                                      self.evaluation_manager, 
                                                      nlp_value,
                                                      validation_value,
                                                      display_flg)
        elif validation_datum_key == 'Relapse.Date':
            performance = \
                self.evaluator_registry.run_object('relapse_date_tools',
                                                      self.evaluation_manager, 
                                                      nlp_value,
                                                      validation_value,
                                                      display_flg)
        elif validation_datum_key == 'Residual.dx':
            performance = \
                self.evaluator_registry.run_object('residual_disease_tools',
                                                      self.evaluation_manager, 
                                                      nlp_value,
                                                      validation_value,
                                                      display_flg)
        elif validation_datum_key == 'surfaceAntigensImmunohistochemicalStains':
            performance = \
                self.evaluator_registry.run_object('immunophenotype_tools',
                                                      self.evaluation_manager, 
                                                      nlp_value,
                                                      validation_value,
                                                      display_flg)
        elif validation_datum_key == 'dxAtSpecimenAcquisition':
            performance = \
                self.evaluator_registry.run_object('diagnosis_tools',
                                                      self.evaluation_manager, 
                                                      nlp_value,
                                                      validation_value,
                                                      display_flg)
        elif validation_datum_key == 'dx.Date':
            performance = \
                self.evaluator_registry.run_object('diagnosis_date_tools',
                                                      self.evaluation_manager, 
                                                      nlp_value,
                                                      validation_value,
                                                      display_flg)
        elif validation_datum_key == 'specificDxAtAcquisition':
            performance = \
                self.evaluator_registry.run_object('specific_diagnosis_tools',
                                                      self.evaluation_manager, 
                                                      nlp_value,
                                                      validation_value,
                                                      display_flg)
        arg_dict['performance'] = performance
        return arg_dict