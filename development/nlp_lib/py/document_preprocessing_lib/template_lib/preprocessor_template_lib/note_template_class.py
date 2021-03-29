# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 16:28:34 2018

@author: haglers
"""

#
from nlp_lib.py.base_class_lib.template_base_class import Template_base
from nlp_lib.py.processor_lib.preprocessor_lib.rewriters_lib.normalizers_lib.section_header_normalizer_note_class \
    import Section_header_normalizer_note
from nlp_lib.py.processor_lib.preprocessor_lib.summarization_lib.summarization_class \
    import Summarization

#
class Note_template(Template_base):
        
    #
    def _extract_section_headers(self):
        section_header_normalizer = Section_header_normalizer_note(self.project_data)
        self.dynamic_data_manager.append_keywords_text(self.body_header)
        section_header_normalizer.push_dynamic_data_manager(self.dynamic_data_manager)
        section_header_normalizer.push_text(self.text)
        section_header_normalizer.allergies_section_header(self.formatting)
        section_header_normalizer.assessment_section_header(self.formatting)
        section_header_normalizer.datetime_section_header(self.formatting)
        section_header_normalizer.diagnosis_section_header(self.formatting)
        section_header_normalizer.evaluation_section_header(self.formatting)
        section_header_normalizer.goals_section_header(self.formatting)
        section_header_normalizer.history_section_header(self.formatting)
        section_header_normalizer.hospital_course_section_header(self.formatting)
        section_header_normalizer.icd9_section_header(self.formatting)
        section_header_normalizer.impression_and_recommendation_section_header(self.formatting)
        section_header_normalizer.insurance_section_header(self.formatting)
        section_header_normalizer.intervention_section_header(self.formatting)
        section_header_normalizer.lab_test_and_medication_section_header(self.formatting)
        section_header_normalizer.objective_section_header(self.formatting)
        section_header_normalizer.other_section_header(self.formatting)
        section_header_normalizer.person_section_header(self.formatting)
        section_header_normalizer.reason_section_header(self.formatting)
        section_header_normalizer.service_section_header(self.formatting)
        section_header_normalizer.subjective_section_header(self.formatting)
        section_header_normalizer.technique_section_header(self.formatting)
        section_header_normalizer.twenty_four_hour_events_section_header(self.formatting)
        self.text = section_header_normalizer.pull_text()
        self.dynamic_memory_manager = section_header_normalizer.pull_dynamic_data_manager()