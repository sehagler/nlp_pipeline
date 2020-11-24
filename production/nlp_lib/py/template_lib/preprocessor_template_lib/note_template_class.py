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
from nlp_lib.py.tool_lib.query_tools_lib.ecog_tools \
    import Summarization as Summarization_ecog
from nlp_lib.py.tool_lib.query_tools_lib.tnm_stage_tools \
    import Summarization as Summarization_tnm_stage

#
class Note_template(Template_base):
        
    #
    def _extract_section_headers(self):
        section_header_normalizer = Section_header_normalizer_note(self.project_data)
        self.linguamatics_i2e_writer.append_keywords_text(self.body_header)
        section_header_normalizer.push_linguamatics_i2e_writer(self.linguamatics_i2e_writer)
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
        self.linguamatics_i2e_writer = section_header_normalizer.pull_linguamatics_i2e_writer()
        
    #
    def _summarization(self):
        self._normalize_whitespace()
        summarization_ecog = Summarization_ecog(self.project_data)
        summarization_ecog.push_text(self.text)
        summarization_ecog.process_ecog()
        self.text = summarization_ecog.pull_text()
        summarization_tnm_stage = Summarization_tnm_stage(self.project_data)
        summarization_tnm_stage.push_text(self.text)
        summarization_tnm_stage.remove_tnm_staging()
        self.text = summarization_tnm_stage.pull_text()
        summarization = Summarization(self.project_data)
        summarization.push_text(self.text)
        summarization.process_names()
        summarization.remove_extraneous_text()
        self.text = summarization.pull_text()
        self._normalize_whitespace()