# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 08:12:07 2018

@author: haglers
"""

#
from nlp_text_normalization_lib.base_lib.preprocessor_registry_base_class \
    import Preprocessor_registry_base
from tool_lib.py.query_tools_lib.base_lib.blasts_tools_base \
    import Summarization as Summarization_blasts
from tool_lib.py.query_tools_lib.base_lib.breast_cancer_biomarkers_tools_base \
    import Summarization as Summarization_breast_cancer_biomarkers
from tool_lib.py.query_tools_lib.ecog_status_tools \
    import Summarization as Summarization_ecog_status
from tool_lib.py.query_tools_lib.fish_analysis_summary_tools \
    import Summarization as Summarization_fish_analysis_summary
from tool_lib.py.query_tools_lib.histological_grade_tools \
    import Summarization as Summarization_histological_grade
from tool_lib.py.query_tools_lib.immunophenotype_tools \
    import Summarization as Summarization_immunophenotype
from tool_lib.py.query_tools_lib.serial_number_tools \
    import Summarization as Summarization_serial_number
from tool_lib.py.query_tools_lib.smoking_tools \
    import Summarization as Summarization_smoking
from tool_lib.py.query_tools_lib.tnm_staging_tools \
    import Summarization as Summarization_tnm_stage
#
class Summarization_registry(Preprocessor_registry_base):
    
    #
    def create_preprocessors(self):
        self._register_preprocessor('summarization_blasts',
                                    Summarization_blasts(self.static_data))
        self._register_preprocessor('summarization_breast_cancer_biomarkers',
                                    Summarization_breast_cancer_biomarkers(self.static_data))
        self._register_preprocessor('summarization_ecog_status',
                                    Summarization_ecog_status(self.static_data))
        self._register_preprocessor('summarization_fish_anlysis_summary',
                                    Summarization_fish_analysis_summary(self.static_data))
        self._register_preprocessor('summarization_histological_grade',
                                    Summarization_histological_grade(self.static_data))
        self._register_preprocessor('summarization_immunophenotype',
                                    Summarization_immunophenotype(self.static_data))
        self._register_preprocessor('summarization_serial_number',
                                    Summarization_serial_number(self.static_data))
        self._register_preprocessor('summarization_smoking',
                                    Summarization_smoking(self.static_data))
        self._register_preprocessor('summarization_tnm_stage',
                                    Summarization_tnm_stage(self.static_data))