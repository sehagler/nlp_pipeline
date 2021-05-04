# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 13:47:40 2019

@author: haglers
"""

#
from nlp_lib.py.document_preprocessing_lib.base_class_lib.report_preprocessor_base_class \
    import Report_preprocessor_base_class
from nlp_lib.py.document_preprocessing_lib.preprocessing_lib.rewriters_lib.normalizers_lib.section_header_normalizer_class \
    import Section_header_normalizer
from tool_lib.py.query_tools_lib.antigens_tools \
    import Posttokenizer as Posttokenizer_antigens
from tool_lib.py.query_tools_lib.cancer_tools \
    import Named_entity_recognition as Named_entity_recognition_cancer
from tool_lib.py.query_tools_lib.cancer_tools \
    import Posttokenizer as Posttokenizer_cancer
from tool_lib.py.query_tools_lib.cancer_tools \
    import Text_preparation as Text_preparation_cancer

#
class Hematopathology_report_preprocessor(Report_preprocessor_base_class):
    
    #
    def _extract_section_headers(self):
        section_header_normalizer = Section_header_normalizer(self.project_data)
        self.dynamic_data_manager.append_keywords_text(self.body_header)
        section_header_normalizer.push_dynamic_data_manager(self.dynamic_data_manager)
        section_header_normalizer.push_text(self.text)
        section_header_normalizer.amendment_section_header(self.formatting)
        #section_header_normalizer.antibodies_tested_section_header(self.formatting)
        #section_header_normalizer.background_section_header(self.formatting)
        #section_header_normalizer.bone_marrow_section_header(self.formatting)
        section_header_normalizer.comment_section_header('pull_out_section_header_to_bottom_of_report')
        #section_header_normalizer.cytogenetic_and_fish_studies_section_header(self.formatting)
        #section_header_normalizer.diagnosis_section_header(self.formatting)
        #section_header_normalizer.explanation_section_header(self.formatting)
        #section_header_normalizer.flow_cytometric_analysis_section_header(self.formatting)
        section_header_normalizer.history_section_header(self.formatting)
        section_header_normalizer.impression_and_recommendation_section_header(self.formatting)
        #section_header_normalizer.immunohistochemical_stains_section_header(self.formatting)
        #section_header_normalizer.immunologic_analysis_section_header(self.formatting)
        #section_header_normalizer.interpretation_section_header(self.formatting)
        #section_header_normalizer.laboratory_data_section_header(self.formatting)
        #section_header_normalizer.materials_received_section_header(self.formatting)
        #section_header_normalizer.method_section_header(self.formatting)
        #section_header_normalizer.molecular_studies_section_header(self.formatting)
        #section_header_normalizer.peripheral_blood_morphology_section_header(self.formatting)
        section_header_normalizer.person_section_header(self.formatting)
        #section_header_normalizer.references_section_header(self.formatting)
        #section_header_normalizer.special_stains_section_header(self.formatting)
        #section_header_normalizer.synopsis_section_header(self.formatting)
        section_header_list = \
            [ 'ANTIBODIES TESTED', 'BONE MARROW ASPIRATE SMEARS',
              'BONE MARROW CLOT SECTION', 'BONE MARROW DIFFERENTIAL' ]
        section_header_normalizer.normalize_section_header_1(section_header_list,
                                                             self.formatting)
        section_header_list = \
            [ 'BACKGROUND', 'CYTOGENETIC ANALYSIS SUMMARY',
              'PREAMENDMENT DIAGNOSIS', 'DIAGNOSIS', 'EXPLANATION',
              'FLOW CYTOMETRIC ANALYSIS', 'IMMUNOHISTOCHEMICAL STAINS', 
              'IMMUNOLOGIC ANALYSIS', 'INTERPRETATION', 'LAB DATA', 
              'MATERIALS RECEIVED', 'METHOD', 'MOLECULAR STUDIES',
              'PERIPHERAL BLOOD MORPHOLOGY', 'REFERENCES', 'SPECIAL STAINS',
              'SYNOPSIS' ]
        section_header_normalizer.normalize_section_header_2(section_header_list,
                                                             self.formatting)
        self.text = section_header_normalizer.pull_text()
        self.dynamic_memory_manager = \
            section_header_normalizer.pull_dynamic_data_manager()
    
    #
    def _format_beakerap(self):
        Report_preprocessor_base_class._format_beakerap(self)
        #self._format_section_headers()
        self._format_hematopathology_table_beaker_ap()
        
    #
    def _format_hematopathology_table_beaker_ap(self):
        self._clear_command_list()
        self._pull_out_section_header('(?i)[ \t]antibodies tested')
        self._pull_out_section_header('(?i)[ \t]bone marrow aspirate smears')
        self._pull_out_section_header('(?i)[ \t]bone marrow (biopsy/)?clot section')
        self._pull_out_section_header('(?i)[ \t]bone marrow differential')
        self._pull_out_section_header('(?i)[ \t]cbc')
        self._pull_out_section_header('(?i)[ \t]component value')
        self._pull_out_section_header('(?i)[ \t]cytogenetic and fish studies')
        self._pull_out_section_header('(?i)[ \t]flow cytometric analysis')
        self._pull_out_section_header('(?i)[ \t]immunohistochemical stains:')
        self._pull_out_section_header('(?i)[ \t]immunologic analysis:')
        self._pull_out_section_header('(?i)[ \t]molecular studies:')
        self._pull_out_section_header('(?i)[ \t]peripheral blood differential')
        self._pull_out_section_header('(?i)[ \t]peripheral blood morphology')
        self._pull_out_section_header('(?i)[ \t]resulting agency')
        self._pull_out_section_header('(?i)[ \t]special stains')
        self._pull_out_table_entry('[ \t]ANISOCYTOSIS')
        self._pull_out_table_entry('[ \t]ATYPICAL CELLS? [#%]')
        self._pull_out_table_entry('[ \t]BASO(PHIL)? [#%]')
        self._pull_out_table_entry('[ \t]EOS(INOPHIL)? [#%]')
        self._pull_out_table_entry('[ \t]HCT(?= [0-9])')
        self._pull_out_table_entry('[ \t]HEMATOCRIT')
        self._pull_out_table_entry('[ \t]HEMOGLOBIN')
        self._pull_out_table_entry('[ \t]HGB(?= [0-9])')
        self._pull_out_table_entry('[ \t]IG[#%]')
        self._pull_out_table_entry('[ \t]LY#(?= [0-9])')
        self._pull_out_table_entry('[ \t]LYMPHOCYTE [#%]')
        self._pull_out_table_entry('[ \t]MANUAL DIFFERENTIAL')
        self._pull_out_table_entry('[ \t]MCHC')
        self._pull_out_table_entry('[ \t]MCV')
        self._pull_out_table_entry('[ \t]METAMYELOCYTES [#%]')
        self._pull_out_table_entry('[ \t]MONOCYTE [#%]')
        self._pull_out_table_entry('[ \t]MYELOCYTES [#%]')
        self._pull_out_table_entry('[ \t]MPV')
        self._pull_out_table_entry('[ \t]NE#(?= [0-9])')
        self._pull_out_table_entry('[ \t]NEUTROPHIL [#%]')
        self._pull_out_table_entry('[ \t]NRBC[#%]')
        self._pull_out_table_entry('[ \t]PLT(?= [0-9])')
        self._pull_out_table_entry('[ \t]PLASMA CELLS? [#%]')
        self._pull_out_table_entry('[ \t]PLATELET COUNT')
        self._pull_out_table_entry('[ \t]POLYCHROMASIA')
        self._pull_out_table_entry('[ \t]PROMYELOCYTES [#%]')
        self._pull_out_table_entry('[ \t]RBC [0-9]')
        self._pull_out_table_entry('[ \t]RDW SD')
        self._pull_out_table_entry('[ \t]REACTIVE LYMPHS? [#%]')
        self._pull_out_table_entry('[ \t]RED CELL COUNT')
        self._pull_out_table_entry('[ \t]ROW(?= [0-9])')
        self._pull_out_table_entry('[ \t]WHITE CELL COUNT')
        self._pull_out_table_entry('[ \t]WBC(?= [0-9])')
        self._general_command('\nFinal Diagnosis\n', {None : '\nFINAL DIAGNOSIS\n'})
        self._general_command('\n(MANUAL|PERIPHERAL BLOOD) DIFFERENTIAL', {None : '\n\nMANUAL DIFFERENTIAL'})
        self._process_command_list()
        
    #
    def _format_hematopathology_table_powerpath(self):
        self._clear_command_list()
        self._pull_out_table_entry('[ \t]Bands[ \t]+[0-9]')
        self._pull_out_table_entry('[ \t](?<!% )Baso(phil)?s[ \t]+(x )?[0-9]')
        self._pull_out_table_entry('[ \t](?<!% )Eos(inophils)?[ \t]+(x )?[0-9]')
        self._pull_out_table_entry('[ \t](?<!% )Lymph(ocyte)?s[ \t]+(x )?[0-9]')
        self._pull_out_table_entry('[ \t](?<!% )Mono(cyte)?s[ \t]+(x )?[0-9]')
        self._pull_out_table_entry('[ \t](?<!% )Neutrophils[ \t]+[0-9]')
        self._pull_out_table_entry('[ \t]PMNs[ \t]+(x )?[0-9]')
        self._process_command_list()
        
    #
    def _format_powerpath(self):
        Report_preprocessor_base_class._format_powerpath(self)
        #self._format_section_headers()
        self._format_hematopathology_table_powerpath()
        
    #
    def _format_section_headers(self):
        self._clear_command_list()
        self._general_command('(?i)\nFinal (Pathologic )?Diagnosis\n', {None : ''})
        self._general_command('\nDIFFERENTIAL', {None : '\nMANUAL DIFFERENTIAL'})
        self._general_command('\nImmunologic Analysis\n', {None : ''})
        self._general_command('\nMicroscopic Description\n', {None : ''})
        self._process_command_list()
        
    #
    def _named_entity_recognition(self):
        Report_preprocessor_base_class._named_entity_recognition(self)
        self._normalize_whitespace()
        named_entity_recognition_cancer = Named_entity_recognition_cancer(self.project_data)
        named_entity_recognition_cancer.push_text(self.text)
        named_entity_recognition_cancer.process_abbreviations()
        named_entity_recognition_cancer.process_initialisms()
        self.text = named_entity_recognition_cancer.pull_text()
        self._normalize_whitespace()
            
    #
    def _posttokenizer(self, clear_section_headers=True):
        Report_preprocessor_base_class._posttokenizer(self)
        posttokenizer_antigens = Posttokenizer_antigens(self.project_data)
        posttokenizer_antigens.push_text(self.text)
        posttokenizer_antigens.process_antigens()
        self.text = posttokenizer_antigens.pull_text()
        posttokenizer_cancer = Posttokenizer_cancer(self.project_data)
        posttokenizer_cancer.push_text(self.text)
        posttokenizer_cancer.process_general()
        self.text = posttokenizer_cancer.pull_text()
        self._clear_command_list()
        self._general_command('\( [0-9]+ - [0-9]+ \)', {' \)' : '.0 )'})
        self._general_command('\( [0-9]+ - [0-9]+\.[0-9]+ \)', {' - ' : '.0 - '})
        self._general_command('day 0( is equal to | ?= ?)', {None : ''})
        self._process_command_list()
        if clear_section_headers:
            self._clear_section_header_tags()
        
    '''
    #
    def _pretokenizer(self):
        Report_preprocessor_base_class._pretokenizer(self)
        #self._normalize_table
        
    #
    def _remove_false_specimen(self):
        self._clear_command_list()
        self._general_command('(?i) \((([a-o]|[r-z])+[0-9]+(,( )?)?)+\)', {None : ''})
        self._process_command_list()
    '''
        
    #
    def _text_cleanup(self):
        self._normalize_whitespace()
        text_preparation = Text_preparation_cancer(self.project_data)
        text_preparation.push_text(self.text)
        text_preparation.cleanup_text()
        self.text = text_preparation.pull_text()
        self._normalize_whitespace()
        
    #
    def _text_setup(self):
        Report_preprocessor_base_class._text_setup(self)
        self._normalize_whitespace()
        text_preparation = Text_preparation_cancer(self.project_data)
        text_preparation.push_text(self.text)
        text_preparation.normalize_text()
        text_preparation.setup_text()
        self.text = text_preparation.pull_text()
        self._normalize_whitespace()