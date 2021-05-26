# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 10:38:15 2020

@author: haglers
"""

#
from word2number import w2n
import re

#
from nlp_lib.py.document_preprocessing_lib.base_class_lib.preprocessor_base_class \
    import Preprocessor_base
from tool_lib.py.processing_tools_lib.text_processing_tools import s

#
class Tokenizer(Preprocessor_base):
    
    #
    def process_abbreviations(self):
        self._general_command('(?i)%age', {None : 'percentage'})
        self._general_command('(?<=[Dd])iagnosis', {None : 'x'})
        self._general_command('(?<=[Dd])iagnosed', {None : 'xed'})
        self._general_command('(?<=[Dd])iagnoses', {None : 'xes'})
        self._general_command('(?<=[Ll])aboratories', {None : 'abs'})
        self._general_command('(?<=[Ll])aboratory', {None : 'ab'})
        self._general_command('(?<=[Mm])ets(?= )', {None : 'etastases'})
        self._general_command('(?<=[Mm])onth', {None : 'o'})
        self._general_command('(?<=[Pp])atient', {None : 't'})
        self._general_command('(?<=[Rr])efills', {None : 'fl'})
        self._general_command('(?<=[Rr])esection', {None : 'sxn'})
        self._general_command('(?<=[Yy])ear', {None : 'r'})
        
    #
    def process_chemical_abbreviations(self):
        self._general_command('(?i)alcohol(?!i)', {'(?i)alcohol' : 'ETOH'})
        self._normalize_regular_initialism('(?i)butyrate esterase', 'BE')
        self._normalize_regular_initialism('(>i)methotrexate', 'MTX')
        self._normalize_regular_initialism('(?i)myeloperoxidase', 'MPO')
        self._normalize_regular_initialism('(?i)sudan black B', 'SBB')
        
    #
    def process_measurements(self):
        self._general_command('(?i)(<=(\d+)(\-|\+)?) ((out )?of|per) (?= [0-9])', 
                              {'(?i) ((out )?of|per) ' : '/'})
        self._normalize_regular_initialism('high(-| )?power(ed)? field' + s(), 'HPF')
        self._general_command('(?i)HPF(\')?s', {None : 'HPF'})
        self._general_command('(?i)cmfn', {None : 'cm fn'})
        self._general_command('(?i)(?<=[0-9])cm', {None : ' cm'})
        self._general_command('(?i)(?<=[0-9])mm', {None : ' mm'})
        self._general_command('(?i)(?<=(cm|mm))\.', {None : ''})
        self._general_command('(?i)((only )?about|approx(( \.)|imate(ly)?)?|roughly)(?= [0-9])', {None : '~'})
        self._general_command('(?i)(greater|more) th(a|e)n(?= [0-9])', {None : '>'})
        self._general_command('(?i)less th(a|e)n(?= [0-9])', {None : '<'})
        self._general_command('(?i)[\n\s]+o(\')?clock', {None : ' : 00'})
        self._general_command('(?i)(?<=[0-9])of', {None : ' of'})
        self._general_command('(?i)of(?=[0-9])', {None : 'of '})
        
    #
    def process_initialisms(self):
        self._general_command('(?i)a( \. )?m( \. )', {None : 'AM'})
        self._general_command('(?i)D( \. )?O( \. )', {None : 'DO'})
        self._general_command('(?i)Dr( \. )', {None : 'Dr'})
        text_list = []
        text_list.append('(?i)m( \. )?d( \. )')
        text_list.append('(?i)m( \. )d( \. )?')
        self._general_command(text_list, {None : 'MD'})
        text_list = []
        text_list.append('(?i)ph( \. )?d( \. )')
        text_list.append('(?i)ph( \. )d( \. )?')
        self._general_command(text_list, {None : 'PhD'})
        self._general_command('(?i)p( \. )?m( \. )', {None : 'PM'})
        self._general_command('(?i)(U( \. )?S( \.)?)? Food and Drug Administration', {None : 'FDA'})
        
    #
    def process_medical_abbreviations(self):
        self._general_command('(?<=[Ff])ollow( |\-)up', {None : ' / u'})
        self._general_command('(?<=[Hh])istory', {None : 'x'})
        self._general_command('(?<=[Hh])x of', {None : ' / o'})
        self._general_command('(?<=[Ss])urgical procedure', {None : ' / p '})
        
    #
    def process_numbers(self):
        word_list = list(set(filter(None, re.split('[ \n\t]+', self.text))))
        change_list = []
        for word in word_list:
            if not re.search('(?i)([0-9]|point)', word):
                do_w2n = True
                if re.search('-', word):
                    element_list = word.split('-')
                    for element in element_list:
                        try:
                            num = w2n.word_to_num(element)
                        except:
                            do_w2n = False
                if do_w2n:
                    try:
                        num = w2n.word_to_num(word)
                        if num < 100:
                            change_list.append([word, str(num)])
                    except:
                        pass
        change_list.sort(key=lambda x: len(x[0]), reverse=True)
        for change in change_list:
            self._general_command('[ \n\t]' + change[0] + '[ \n\t]', {change[0] : change[1]})
        
    #
    def process_punctuation(self):
        self._general_command('(?<!(:|\d))\d+-\d+%', {'-' : '%-'})
        self._general_command('(?<!(:|\d))\d+-\d+:00', {'-' : ' : 00-'})
        self._general_command('(?i)(?<=[0-9]) %', {None : '%'})
        self._general_command('\)\(', {None : ') ('})
        self._general_command(' \?', {None : ''})
        self._general_command(':', {None : ' : '})
        self._general_command('(?<=[0-9]) : (?=[0-9])', {None : ':'})
        self._general_command(',', {None : ' , '})
        self._general_command('(?<=[0-9]) , (?=[0-9])', {None : ','})
        self._general_command('(?<=[0-9]),(?=[0-9]{4})', {None : ' , '})
        self._general_command('(?<=[0-9]),(?=[0-9]+/)', {None : ' , '})
        self._general_command(';', {None : ' ; '})
        self._general_command('(?<=[0-9])-(?=[0-9])', {None : ' - '})
        self._general_command('(?<=[0-9]) -(?=[0-9]+%)', {None : ' - '})
        self._general_command('(?<=[0-9])- (?=[0-9]+%)', {None : ' - '})
        self._general_command('(?<= )-(?=[A-Za-z])', {None : ' - '})
        self._general_command('=', {None : ' = '})
        self._general_command('\/', {None : ' / '})
        self._general_command('>', {None : ' > '})
        self._general_command('#', {None : ' # '})
        self._general_command('<', {None : ' < '})
        self._general_command('~', {None : ' ~ '})
        self._general_command('\(', {None : '( '})
        self._general_command('\)', {None : ' )'})
        self._general_command('(?i)(?<=[a-z0-9])\*', {None : ' *'})
        self._general_command('\.(?![0-9])', {None : ' . '})
        self._general_command('\( [0-9\.]+ ?\)', {'\( ' : '('})
        self._general_command('\( ?[0-9\.]+ \)', {' \)' : ')'})
        self._general_command('\( ! \)', {None : ''})
        
    #
    def process_simplifications(self):
        self._general_command('(?i)according to', {None : 'per'})
        self._general_command('(?i)for example', {None : 'e.g.'})
        self._general_command('(?i)w / ', {'(?i)w /' : 'with'})