# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 17:43:29 2020

@author: haglers
"""

#
import re

#
from nlp_lib.py.document_preprocessing_lib.base_class_lib.report_preprocessor_base_class \
    import Report_preprocessor_base_class
from nlp_lib.py.document_preprocessing_lib.preprocessing_lib.rewriters_lib.pretokenizers_lib.pretokenizer_class \
    import Pretokenizer
from nlp_lib.py.document_preprocessing_lib.preprocessing_lib.rewriters_lib.normalizers_lib.section_header_normalizer_class \
    import Section_header_normalizer

#
class Note_preprocessor(Report_preprocessor_base_class):
    
    #
    def _extract_section_headers(self):
        section_header_normalizer = Section_header_normalizer(self.project_data)
        self.dynamic_data_manager.append_keywords_text(self.body_header)
        section_header_normalizer.push_dynamic_data_manager(self.dynamic_data_manager)
        section_header_normalizer.push_text(self.text)
        #section_header_normalizer.allergies_section_header(self.formatting)
        #section_header_normalizer.assessment_section_header(self.formatting)
        #section_header_normalizer.datetime_section_header(self.formatting)
        #section_header_normalizer.diagnosis_section_header(self.formatting)
        #section_header_normalizer.evaluation_section_header(self.formatting)
        #section_header_normalizer.goals_section_header(self.formatting)
        section_header_normalizer.history_section_header(self.formatting)
        #section_header_normalizer.hospital_course_section_header(self.formatting)
        #section_header_normalizer.icd9_section_header(self.formatting)
        section_header_normalizer.impression_and_recommendation_section_header(self.formatting)
        #section_header_normalizer.insurance_section_header(self.formatting)
        #section_header_normalizer.intervention_section_header(self.formatting)
        #section_header_normalizer.lab_test_and_medication_section_header(self.formatting)
        #section_header_normalizer.objective_section_header(self.formatting)
        #section_header_normalizer.other_section_header(self.formatting)
        section_header_normalizer.person_section_header(self.formatting)
        #section_header_normalizer.reason_section_header(self.formatting)
        #section_header_normalizer.service_section_header(self.formatting)
        #section_header_normalizer.subjective_section_header(self.formatting)
        #section_header_normalizer.technique_section_header(self.formatting)
        #section_header_normalizer.twenty_four_hour_events_section_header(self.formatting)
        section_header_list = [ 'DATETIME' ]
        section_header_normalizer.general_command(section_header_list,
                                                  self.formatting)
        section_header_list = \
            [ 'ALLERGIES', 'ASSESSMENT', 'DIAGNOSIS', 'EVALUATION', 'GOALS',
              'HOSPITAL COURSE', 'ICD-9', 'INSURANCE', 'INTERVENTION',
              'LAB DATA AND MEDICATION', 'LAB DATA', 'OBJECTIVE', 'OTHER',
              'REASON', 'SUBJECTIVE', 'TECHNIQUE', 'TWENTY-FOUR HOUR EVENTS' ]
        section_header_normalizer.normalize_section_header_1(section_header_list,
                                                             self.formatting)
        section_header_list = \
            [ 'MEDICATION', 'SERVICE' ]
        section_header_normalizer.normalize_section_header_2(section_header_list,
                                                             self.formatting)
        self.text = section_header_normalizer.pull_text()
        self.dynamic_memory_manager = \
            section_header_normalizer.pull_dynamic_data_manager()