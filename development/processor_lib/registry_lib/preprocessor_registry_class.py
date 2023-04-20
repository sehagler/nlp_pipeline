# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 08:12:07 2018

@author: haglers
"""

#
import os
import re
import traceback

#
from base_lib.preprocessor_base_class import Preprocessor_base
from base_lib.preprocessor_registry_base_class \
    import Preprocessor_registry_base
import lambda_lib.tool_lib.lambda_tools as lambda_tools
from tools_lib.processing_tools_lib.function_processing_tools \
    import sequential_composition
from tools_lib.regex_lib.regex_tools \
    import article, be, note_label, s, specimen_label
from tools_lib.processing_tools_lib.text_processing_tools \
    import substitution_endings_list
    
#
def _process_organizations(text):
    text = \
        lambda_tools.initialism_lambda_conversion('eastern cooperative oncology group', text, 'ECOG')
    text = \
        lambda_tools.initialism_lambda_conversion('(u( \. )?s( \.)? ?)?food and drug administration', text, 'FDA')
    text = \
        lambda_tools.initialism_lambda_conversion('world health organization', text, 'WHO')
    return text

#
def _process_past_medical_history(text):
    text = \
        lambda_tools.initialism_lambda_conversion('past medical hx', text, 'PMH')
    text = \
        lambda_tools.lambda_conversion('PMHx', text, 'PMH')
    text = \
        lambda_tools.lambda_conversion('PMH / o', text, 'PMH')
    return text
    

#
def _process_regular_initialisms(text):
    
    #
    text = \
        lambda_tools.initialism_lambda_conversion('cerebrospinal fluid', text, 'CSF')
    text = \
        lambda_tools.initialism_lambda_conversion('chronic kidney disease', text, 'CKD')
    text = \
        lambda_tools.initialism_lambda_conversion('chronic renal disease', text, 'CRD')
    text = \
        lambda_tools.initialism_lambda_conversion('chronic renal failure', text, 'CRF')
    text = \
        lambda_tools.initialism_lambda_conversion('fluorescen(ce|t) in situ hybridization', text, 'FISH')
    text = \
        lambda_tools.initialism_lambda_conversion('in situ hybridization', text, 'ISH')
    text = \
        lambda_tools.initialism_lambda_conversion('red blood cell', text, 'RBC')
    text = \
        lambda_tools.initialism_lambda_conversion('white blood cell', text, 'WBC')
    
    # miscellaneous
    text = \
        lambda_tools.initialism_lambda_conversion('columnar cell change', text, 'CCC')
    text = \
        lambda_tools.initialism_lambda_conversion('flat epithelial atypia', text, 'FEA')
    text = \
        lambda_tools.initialism_lambda_conversion('pathologic complete response', text, 'pCR')
    text = \
        lambda_tools.initialism_lambda_conversion('residual ca(ncer)? burden', text, 'RCB')
    text = \
        lambda_tools.lambda_conversion('(?i)FAB (?=[0-9])', text, 'FAB M')
    text = \
        lambda_tools.lambda_conversion('(?i)HLA-Dr', text, 'HLA-DR')
    text = \
        lambda_tools.lambda_conversion('(?i)blasts ?(\+|and|plus) ?promonocytes', text, 'blasts/promonocytes')
    text = \
        lambda_tools.initialism_lambda_conversion('(?i)minimal residual disease', text, 'MRD')
    text = \
        lambda_tools.initialism_lambda_conversion('(?i)myelodysplastic syndrome', text, 'MDS')
    return text
        
#
def _remove_extraneous_text(text):
    text = \
        lambda_tools.deletion_lambda_conversion('[\n\s]+based on pathologic finding' + s(), text)
    text = \
        lambda_tools.deletion_lambda_conversion('(?<=Dr [A-Z])\.', text)
    text = \
        lambda_tools.deletion_lambda_conversion('my electronic signature.*' + article() + ' final diagnosis( \.)?', text)
    text = \
        lambda_tools.deletion_lambda_conversion('i have reviewed.*and final diagnosis( \.)?', text)
    text = \
        lambda_tools.deletion_lambda_conversion('(?i)inclu(des|sive of) all specimens', text)
    text = \
        lambda_tools.deletion_lambda_conversion('(?i)pathologist interpretation ' + be() + ' based on ' + article() + ' review.*representative hematoxylin and eosin stains( \.)?', text)
    text = \
        lambda_tools.deletion_lambda_conversion('(?i)' + article() + ' test ' + be() + ' developed.*FDA( \.)?', text)
    text = \
        lambda_tools.deletion_lambda_conversion('(?i)' + article() + ' clinical interpretation ' + be() + ' made by ' + article() + ' clinical geneticist( \.)?', text)
    return text

#
def _remove_mychart(text):
    text = \
        lambda_tools.deletion_lambda_conversion('display progress note in mychart : (no|yes)', text)
    return text
    
#
def _remove_see(text):
    text = \
        lambda_tools.deletion_lambda_conversion('(?i)(\n\s*)?\( (please )?see [^\n\)\]]* \)', text)
    text = \
        lambda_tools.lambda_conversion('(?i)\s*see\n', text, '\n')
    match_str = '(?i)((\n\s*)?-( )?)?(please[\n\s]+)?see[\n\s]+' + \
                '(the )?(second )?(amendment|cancer|note|synoptic)?( )?' + \
                '(below|comment|report|synops(e|i))' + s() + \
                '( and synoptic summary)?( and tumor protocol)?' + \
                '( below)?( for (additional|technical) (details|information))?( \.)?'
    text = substitution_endings_list(text, match_str)
    match_str = '(?i)((\n\s*)?-( )?)?(please[\n\s]+)?see ' + \
                '(note|(staging )?summary|(cancer )?synopsis|synoptic report)' + \
                '( below)?( for (additional|technical) details)?'
    text = substitution_endings_list(text, match_str)
    match_str = '(?i)((\n\s*)?-( )?)?(please[\n\s]+)?see (also )?' + \
                'note' + s() + '( )?' + note_label() + '( to ' + note_label() + ')?'
    text = substitution_endings_list(text, match_str)
    match_str = '(?i)((\n\s*)?-( )?)?(please[\n\s]+)?see (also )?' + \
                'specimen' + s() + '( )?' + specimen_label() + '( to ' + specimen_label() + ')?'
    text = substitution_endings_list(text, match_str)
    return text
    
'''
#
def _substitution_endings_list(text, search_str):
    text = \
        lambda_tools.lambda_conversion(search_str + '\n', text, '\n')
    text = \
        lambda_tools.lambda_conversion(search_str + '\t', text, '\t')
    text = \
        lambda_tools.lambda_conversion(search_str + ' ', text, ' ')
    text = \
        lambda_tools.lambda_conversion(search_str + ',', text, ',')
    text = \
        lambda_tools.lambda_conversion(search_str + '\.', text, '.')
    text = \
        lambda_tools.lambda_conversion(search_str + ';', text, ';')
    text = \
        lambda_tools.lambda_conversion(search_str + '( )?-', text, '-')
    return text
'''
    
#
class Preprocessor_base(Preprocessor_base):
    
    #
    def run_preprocessor(self):
        normalize_text = sequential_composition(_remove_extraneous_text,
                                            _remove_see,
                                            _remove_mychart,
                                            _process_organizations,
                                            _process_past_medical_history,
                                            _process_regular_initialisms)
        self.text = normalize_text(self.text)

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
            os.path.join(software_dir, os.path.join(operation_mode, 'query_lib/processor_lib'))
        print(root_dir)
        for root, dirs, files in os.walk(root_dir):
            relpath = '.' + os.path.relpath(root, root_dir) + '.'
            relpath = re.sub('\.+', '.', relpath)
            for file in files:
                filename, extension = os.path.splitext(os.path.basename(file))
                try:
                    import_cmd = 'from query_lib.processor_lib' + relpath + \
                                 filename + ' import Preprocessor'
                    exec(import_cmd, globals())
                    self._register_preprocessor(filename, Preprocessor())
                    print('Registered Preprocessor from ' + filename)
                except Exception:
                    traceback.print_exc()