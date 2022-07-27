# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 08:12:07 2018

@author: haglers
"""

#
import os
import re

#
from nlp_text_normalization_lib.tool_lib.regex_tools \
    import article, be, note_label, s, specimen_label
from tool_lib.py.query_tools_lib.base_lib.preprocessor_base_class \
    import Preprocessor_base
from tool_lib.py.registry_lib.base_lib.preprocessor_registry_base_class \
    import Preprocessor_registry_base
from tool_lib.py.processing_tools_lib.text_processing_tools \
    import substitution_endings_list
    
#
class Preprocessor_base(Preprocessor_base):
    
    #
    def _process_organizations(self):
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('eastern cooperative oncology group', self.text, 'ECOG')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('(u( \. )?s( \.)? ?)?food and drug administration', self.text, 'FDA')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('world health organization', self.text, 'WHO')
    
    #
    def _process_past_medical_history(self):
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('past medical hx', self.text, 'PMH')
        self.text = \
            self.lambda_manager.lambda_conversion('PMHx', self.text, 'PMH')
        self.text = \
            self.lambda_manager.lambda_conversion('PMH / o', self.text, 'PMH')
        
    
    #
    def _process_regular_initialisms(self):
        
        #
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('cerebrospinal fluid', self.text, 'CSF')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('chronic kidney disease', self.text, 'CKD')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('chronic renal disease', self.text, 'CRD')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('chronic renal failure', self.text, 'CRF')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('fluorescen(ce|t) in situ hybridization', self.text, 'FISH')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('in situ hybridization', self.text, 'ISH')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('red blood cell', self.text, 'RBC')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('white blood cell', self.text, 'WBC')
            
        #
        self._process_past_medical_history()
        self._process_organizations()
        
        # miscellaneous
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('columnar cell change', self.text, 'CCC')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('flat epithelial atypia', self.text, 'FEA')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('pathologic complete response', self.text, 'pCR')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('residual ca(ncer)? burden', self.text, 'RCB')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)FAB (?=[0-9])', self.text, 'FAB M')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)HLA-Dr', self.text, 'HLA-DR')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)blasts ?(\+|and|plus) ?promonocytes', self.text, 'blasts/promonocytes')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('(?i)minimal residual disease', self.text, 'MRD')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('(?i)myelodysplastic syndrome', self.text, 'MDS')  
            
    #
    def _remove_extraneous_text(self):
        self._remove_mychart()
        self._remove_see()
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('[\n\s]+based on pathologic finding' + s(), self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?<=Dr [A-Z])\.', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('my electronic signature.*' + article() + ' final diagnosis( \.)?', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('i have reviewed.*and final diagnosis( \.)?', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)inclu(des|sive of) all specimens', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)pathologist interpretation ' + be() + ' based on ' + article() + ' review.*representative hematoxylin and eosin stains( \.)?', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)' + article() + ' test ' + be() + ' developed.*FDA( \.)?', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)' + article() + ' clinical interpretation ' + be() + ' made by ' + article() + ' clinical geneticist( \.)?', self.text)
    
    #
    def _remove_mychart(self):
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('display progress note in mychart : (no|yes)', self.text)
        
    #
    def _remove_see(self):
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?i)(\n\s*)?\( (please )?see [^\n\)\]]* \)', self.text)
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)\s*see\n', self.text, '\n')
        match_str = '(?i)((\n\s*)?-( )?)?(please[\n\s]+)?see[\n\s]+' + \
                    '(the )?(second )?(amendment|cancer|note|synoptic)?( )?' + \
                    '(below|comment|report|synops(e|i))' + s() + \
                    '( and synoptic summary)?( and tumor protocol)?' + \
                    '( below)?( for (additional|technical) (details|information))?( \.)?'
        self.text = substitution_endings_list(self.text, match_str)
        match_str = '(?i)((\n\s*)?-( )?)?(please[\n\s]+)?see ' + \
                    '(note|(staging )?summary|(cancer )?synopsis|synoptic report)' + \
                    '( below)?( for (additional|technical) details)?'
        self.text = substitution_endings_list(self.text, match_str)
        match_str = '(?i)((\n\s*)?-( )?)?(please[\n\s]+)?see (also )?' + \
                    'note' + s() + '( )?' + note_label() + '( to ' + note_label() + ')?'
        self.text = substitution_endings_list(self.text, match_str)
        match_str = '(?i)((\n\s*)?-( )?)?(please[\n\s]+)?see (also )?' + \
                    'specimen' + s() + '( )?' + specimen_label() + '( to ' + specimen_label() + ')?'
        self.text = substitution_endings_list(self.text, match_str)
        
    '''
    #
    def _substitution_endings_list(self, search_str):
        self.text = \
            self.lambda_manager.lambda_conversion(search_str + '\n', self.text, '\n')
        self.text = \
            self.lambda_manager.lambda_conversion(search_str + '\t', self.text, '\t')
        self.text = \
            self.lambda_manager.lambda_conversion(search_str + ' ', self.text, ' ')
        self.text = \
            self.lambda_manager.lambda_conversion(search_str + ',', self.text, ',')
        self.text = \
            self.lambda_manager.lambda_conversion(search_str + '\.', self.text, '.')
        self.text = \
            self.lambda_manager.lambda_conversion(search_str + ';', self.text, ';')
        self.text = \
            self.lambda_manager.lambda_conversion(search_str + '( )?-', self.text, '-')
    '''
    
    #
    def run_preprocessor(self):
        self._process_regular_initialisms()
        self._remove_extraneous_text()

#
class Preprocessor_registry(Preprocessor_registry_base):
    
    #
    def create_preprocessors(self):
        directory_manager = self.static_data['directory_manager']
        operation_mode = self.static_data['operation_mode']
        software_dir = directory_manager.pull_directory('software_dir')
        self._register_preprocessor('preprocessor_base',
                                    Preprocessor_base())
        root_dir = \
            os.path.join(software_dir, os.path.join(operation_mode, 'tool_lib/py/query_tools_lib'))
        for root, dirs, files in os.walk(root_dir):
            relpath = '.' + os.path.relpath(root, root_dir) + '.'
            relpath = re.sub('\.+', '.', relpath)
            for file in files:
                filename, extension = os.path.splitext(os.path.basename(file))
                try:
                    import_cmd = 'from tool_lib.py.query_tools_lib' + relpath + \
                                 filename + ' import Preprocessor'
                    exec(import_cmd, globals())
                    self._register_preprocessor(filename, Preprocessor())
                    print('Registered Preprocessor from ' + filename)
                except:
                    pass