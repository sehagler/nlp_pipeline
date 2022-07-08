# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 08:56:52 2021

@author: haglers
"""

 #
from word2number import w2n
import re

#
from nlp_text_normalization_lib.base_lib.preprocessor_base_class \
    import Preprocessor_base
from tool_lib.py.query_tools_lib.base_lib.date_tools_base \
    import Tokenizer as Tokenizer_date
from tool_lib.py.processing_tools_lib.text_processing_tools import s

#
class Tokenizer(Preprocessor_base):
    
    #
    def __init__(self, static_data):
        Preprocessor_base.__init__(self, static_data)
        self.tokenizer_date = Tokenizer_date(self.static_data)
    
    #
    def _process_abbreviations(self):
        self.text = \
            self.lambda_manager.lambda_conversion('%age', self.text, 'percentage')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[Dd])iagnosis', self.text, 'x')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[Dd])iagnosed', self.text, 'xed')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[Dd])iagnoses', self.text, 'xes')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[Ll])aboratories', self.text, 'abs')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[Ll])aboratory', self.text, 'ab')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[Mm])ets(?= )', self.text, 'etastases')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[Mm])onth', self.text, 'o')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[Pp])atient', self.text, 't')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[Rr])efills', self.text, 'fl')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[Rr])esection', self.text, 'sxn')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[Yy])ear', self.text, 'r')
        
    #
    def _process_chemical_abbreviations(self):
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('alcohol(?!i)', 'alcohol', self.text, 'ETOH')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('butyrate esterase', self.text, 'BE')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('methotrexate', self.text, 'MTX')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('myeloperoxidase', self.text, 'MPO')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('sudan black B', self.text, 'SBB')
            
    #
    def _process_credentials(self):
        self.text = \
            self.lambda_manager.lambda_conversion('D( \. )?O( \. )', self.text, 'DO')
        self.text = \
            self.lambda_manager.lambda_conversion('D( \. )O( \. )?', self.text, 'DO')
        self.text = \
            self.lambda_manager.lambda_conversion('Dr( \. )', self.text, 'Dr')
        self.text = \
            self.lambda_manager.lambda_conversion('m( \. )?d( \. )', self.text, 'MD')
        self.text = \
            self.lambda_manager.lambda_conversion('m( \. )d( \. )?', self.text, 'MD')
        self.text = \
            self.lambda_manager.lambda_conversion('ph( \. )?d( \. )', self.text, 'PhD')
        self.text = \
            self.lambda_manager.lambda_conversion('ph( \. )d( \. )?', self.text, 'PhD')
        
    #
    def _process_hash(self):
        self.text = \
            self.lambda_manager.lambda_conversion('#', self.text, ' # ')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('blocks? +#', '#', self.text, '')
        
    #
    def _process_measurements(self):
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(<=(\d+)(\-|\+)?) ((out )?of|per) (?= [0-9])', 
                                                             ' ((out )?of|per) ', self.text, '/')
        self.text = \
            self.lambda_manager.initialism_lambda_conversion('high(-| )?power(ed)? field' + s(), self.text, 'HPF')
        self.text = \
            self.lambda_manager.lambda_conversion('HPF(\')?s', self.text, 'HPF')
        self.text = \
            self.lambda_manager.lambda_conversion('cmfn', self.text, 'cm fn')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[0-9])%(?=[A-Za-z])', self.text, '% ')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[0-9])cm', self.text, ' cm ')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[0-9])mm', self.text, ' mm ')
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?<=(cm|mm))\.', self.text)
        self.text = \
            self.lambda_manager.lambda_conversion('[\n\s]+o(\')?clock', self.text, ' : 00')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[0-9])of', self.text, ' of')
        self.text = \
            self.lambda_manager.lambda_conversion('of(?=[0-9])', self.text, 'of ')
        
    #
    def _process_initialisms(self):
        self.text = \
            self.lambda_manager.lambda_conversion('a( \. )?m( \. )', self.text, 'AM')
        self.text = \
            self.lambda_manager.lambda_conversion('p( \. )?m( \. )', self.text, 'PM')
        
    #
    def _process_medical_abbreviations(self):
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[Ff])ollow( |\-)up', self.text, ' / u')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[Hh])istory', self.text, 'x')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[Hh])x of', self.text, ' / o')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[Ss])urgical procedure', self.text, ' / p ')
        
    #
    def _process_numbers(self):
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
            self.text = \
                self.lambda_manager.contextual_lambda_conversion('[ \n\t]' + change[0] + '[ \n\t]',
                                                                 change[0], self.text, change[1])
        
    #
    def _process_punctuation(self):
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('\*', self.text)
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=\d) %', self.text, '%')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(?<!(:|\d))\d+ ?- ?\d+%',
                                                             ' ?- ?', self.text, '%-')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(?<!(:|\d))\d+ to \d+%',
                                                             ' to ', self.text, '%-')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(?<!(:|\d))\d+-\d+:00',
                                                             '-', self.text, ' : 00-')
        self.text = \
            self.lambda_manager.lambda_conversion('\)\(', self.text, ') (')
        self.text = \
            self.lambda_manager.deletion_lambda_conversion(' \?', self.text)
        self.text = \
            self.lambda_manager.lambda_conversion(':', self.text, ' : ')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[0-9]) : (?=[0-9])', self.text, ':')
        self.text = \
            self.lambda_manager.lambda_conversion(',', self.text, ' , ')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[0-9]) , (?=[0-9])', self.text, ',')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[0-9]),(?=[0-9]{4})', self.text, ' , ')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[0-9]),(?=[0-9]+/)', self.text, ' , ')
        self.text = \
            self.lambda_manager.lambda_conversion(';', self.text, ' ; ')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[0-9])-(?=[0-9])', self.text, ' - ')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[0-9]) -(?=[0-9]+%)', self.text, ' - ')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[0-9])- (?=[0-9]+%)', self.text, ' - ')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<= )-(?=[A-Za-z])', self.text, ' - ')
        self.text = \
            self.lambda_manager.lambda_conversion('(?<=[0-9])\+(?=[A-Za-z])', self.text, '+ ')
        self.text = \
            self.lambda_manager.lambda_conversion('=', self.text, ' = ')
        self.text = \
            self.lambda_manager.lambda_conversion('\/', self.text, ' / ')
        self.text = \
            self.lambda_manager.lambda_conversion('>', self.text, ' > ')
        self.text = \
            self.lambda_manager.lambda_conversion('<', self.text, ' < ')
        self.text = \
            self.lambda_manager.lambda_conversion('~', self.text, ' ~ ')
        self.text = \
            self.lambda_manager.lambda_conversion('\(', self.text, '( ')
        self.text = \
            self.lambda_manager.lambda_conversion('\)', self.text, ' )')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)(?<=[a-z0-9])\*', self.text,' *')
        self.text = \
            self.lambda_manager.lambda_conversion('\.(?![0-9])', self.text, ' . ')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('\( [0-9\.]+ ?\)', '\( ', self.text, '(')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('\( ?[0-9\.]+ \)', ' \)', self.text, ')')
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('\( ! \)', self.text)
        
    #
    def _process_simplifications(self):
        self.text = \
            self.lambda_manager.lambda_conversion('at least(?= \d)', self.text, '>')
        self.text = \
            self.lambda_manager.lambda_conversion('estimated(?= \d)', self.text, '~')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)((only )?about|approx(( \.)|imate(ly)?)?|roughly)(?= \d)', self.text, '~')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)(greater|more) th(a|e)n(?= [0-9])', self.text, '>')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)less th(a|e)n(?= \d)', self.text, '<')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)up to( ~)?(?= \d)', self.text, '<')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)according to', self.text, 'per')
        self.text = \
            self.lambda_manager.lambda_conversion('(?i)for example', self.text, 'e.g.')
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('(?i)w / ', '(?i)w /', self.text, 'with')
        
    #
    def _process_underscore(self):
        self.text = \
            self.lambda_manager.contextual_lambda_conversion('_[A-Z][0-9]+_', '_', self.text, '')
    
    #
    def process_document(self, text):
        self.text = text
        self._normalize_whitespace()
        self._process_simplifications()
        self._process_punctuation()
        self._process_hash()
        self._process_underscore()
        self._process_initialisms()
        self._process_credentials()
        self._process_abbreviations()
        self._process_chemical_abbreviations()
        self._process_measurements()
        self._process_medical_abbreviations()
        self._process_numbers()
        self.tokenizer_date.push_text(self.text)
        self.tokenizer_date.process_month()
        self.text = self.tokenizer_date.pull_text()
        self._normalize_whitespace()
        return self.text