# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 16:03:49 2022

@author: haglers
"""

#
from nlp_pipeline_lib.manager_lib.evaluation_lib.evaluation_manager_class \
    import Evaluation_manager
from query_lib.processor_lib.antigens_tools \
    import antibodies_tested_performance
from query_lib.processor_lib.diagnosis_tools \
    import diagnosis_performance
from query_lib.processor_lib.diagnosis_date_tools \
    import diagnosis_date_performance
from query_lib.processor_lib.extramedullary_disease_tools \
    import extramedullary_disease_performance
from query_lib.processor_lib.fab_classification_tools \
    import fab_classification_performance
from query_lib.processor_lib.fish_analysis_summary_tools \
    import fish_analysis_summary_performance
from query_lib.processor_lib.immunophenotype_tools \
    import surface_antigens_performance
from query_lib.processor_lib.karyotype_tools import karyotype_performance
from query_lib.processor_lib.relapse_date_tools \
    import relapse_date_performance
from query_lib.processor_lib.residual_disease_tools \
    import residual_disease_performance
from query_lib.processor_lib.specific_diagnosis_tools \
    import specific_diagnosis_performance
from query_lib.processor_lib.base_lib.blasts_tools_base \
    import blast_performance

#
class BeatAML_Waves_3_And_4_evaluation_manager(Evaluation_manager):
    
    #
    def __init__(self, static_data_object):
        self.evaluation_manager = Evaluation_manager(static_data_object)
    
    #
    def evaluation(self, arg_dict):
        display_flg = arg_dict['display_flg']
        nlp_value = arg_dict['nlp_value']
        validation_datum_key = arg_dict['validation_datum_key']
        validation_value = arg_dict['validation_value']
        performance = None
        if validation_datum_key == '%.Blasts.in.BM' or\
           validation_datum_key == '%.Blasts.in.PB':
            performance = blast_performance(self.evaluation_manager, nlp_value,
                                            validation_value, display_flg)
        elif validation_datum_key == 'Antibodies.Tested':
            performance = antibodies_tested_performance(self.evaluation_manager,
                                                        nlp_value,
                                                        validation_value,
                                                        display_flg)
        elif validation_datum_key == 'Extramedullary.dx':
            performance = extramedullary_disease_performance(self.evaluation_manager,
                                                             nlp_value,
                                                             validation_value,
                                                             display_flg)
        elif validation_datum_key == 'FAB/Blast.Morphology':
            performance = fab_classification_performance(self.evaluation_manager,
                                                         nlp_value,
                                                         validation_value,
                                                         display_flg)
        elif validation_datum_key == 'FISH.Analysis.Summary':
            performance = fish_analysis_summary_performance(self.evaluation_manager,
                                                            nlp_value,
                                                            validation_value,
                                                            display_flg)
        elif validation_datum_key == 'karyotype':
            performance = karyotype_performance(self.evaluation_manager,
                                                nlp_value, validation_value,
                                                display_flg)
        elif validation_datum_key == 'Relapse.Date':
            performance = relapse_date_performance(self.evaluation_manager,
                                                   nlp_value, validation_value,
                                                   display_flg)
        elif validation_datum_key == 'Residual.dx':
            performance = residual_disease_performance(self.evaluation_manager,
                                                       nlp_value,
                                                       validation_value,
                                                       display_flg)
        elif validation_datum_key == 'surfaceAntigensImmunohistochemicalStains':
            performance = surface_antigens_performance(self.evaluation_manager,
                                                       nlp_value,
                                                       validation_value,
                                                       display_flg)
        elif validation_datum_key == 'dxAtSpecimenAcquisition':
            performance = diagnosis_performance(self.evaluation_manager,
                                                nlp_value, validation_value,
                                                display_flg)
        elif validation_datum_key == 'dx.Date':
            performance = diagnosis_date_performance(self.evaluation_manager,
                                                     nlp_value,
                                                     validation_value,
                                                     display_flg)
        elif validation_datum_key == 'specificDxAtAcquisition':
            performance = specific_diagnosis_performance(self.evaluation_manager,
                                                         nlp_value,
                                                         validation_value,
                                                         display_flg)
        arg_dict['performance'] = performance
        return arg_dict