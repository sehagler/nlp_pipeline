# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 10:50:58 2021

@author: haglers
"""

#
import distance
import inflect
import re

#
from nlp_pipeline_lib.py.base_lib.preprocessor_base_class \
    import Preprocessor_base
from tool_lib.py.query_tools_lib.antigens_tools \
    import Posttokenizer as Posttokenizer_antigens
from tool_lib.py.query_tools_lib.cancer_tools \
    import Posttokenizer as Posttokenizer_cancer
from tool_lib.py.query_tools_lib.karyotype_tools \
    import Posttokenizer as Posttokenizer_karyotype
from tool_lib.py.query_tools_lib.histological_grade_tools \
    import Posttokenizer as Posttokenizer_histological_grade

#
class Posttokenizer(Preprocessor_base):
    
    #
    def __init__(self, static_data):
        Preprocessor_base.__init__(self, static_data)
        self.posttokenizer_antigens = Posttokenizer_antigens(self.static_data)
        self.posttokenizer_cancer = Posttokenizer_cancer(self.static_data)
        self.posttokenizer_histological_grade = \
            Posttokenizer_histological_grade(self.static_data)
        self.posttokenizer_karyotype = \
            Posttokenizer_karyotype(self.static_data)
            
    #
    def _correct_deletions_insertions_replacements(self, words, 
                                                   correct_word_list):
        for correct_word in correct_word_list:
            distances = \
                [ (w, distance.levenshtein(w, correct_word)) for w in words \
                  if w.lower() != correct_word.lower() ]
            distances = list(set(distances))
            corrections = \
                [ w[0] for w in distances if w[1] == 1 ]
            corrections = [ w for w in corrections if w not in correct_word_list]
            for correction in corrections:
                self._general_command(correction, {None : correct_word})
                
    #
    def _correct_transpositions(self, words, correct_word_list):
        for correct_word in correct_word_list:
            distances = \
                [ (w, distance.levenshtein(w, correct_word)) for w in words \
                  if ( (len(w) == len(correct_word)) and \
                       (w.lower() != correct_word.lower()) ) ]
            distances = list(set(distances))
            corrections = \
                [ w[0] for w in distances if w[1] == 2 ]
            corrections = [ w for w in corrections if w not in correct_word_list]
            if len(corrections) > 0:
                for correction in corrections:
                    diffs = [ (i, correct_word[i], correction[i]) \
                              for i in range(len(correct_word)) \
                              if correct_word[i] != correction[i] ]
                    if (abs(diffs[0][0] - diffs[1][0]) == 1) and \
                       (diffs[0][1] == diffs[1][2]) and \
                       (diffs[0][2] == diffs[1][1]):
                        self._general_command(correction, {None : correct_word})
    
    #
    def _correct_typos(self):
        correct_seed_list_others = [ 'estrogen', 'progesterone', 'serious' ]
        correct_seed_list_with_plurals = [ 'edible', 'patient', 'positive',
                                           'referral' ]
        correct_word_list_others = \
            self._generate_correct_word_list(correct_seed_list_others)
        correct_word_list_with_plurals = \
            self._generate_correct_word_list_with_plurals(correct_seed_list_with_plurals)
        correct_word_list = correct_word_list_others
        correct_word_list.extend(correct_word_list_with_plurals)
        correct_word_list = sorted(correct_word_list, key=len, reverse=True)
        words = re.findall(r'\b\w+\b', self.text)
        self._correct_deletions_insertions_replacements(words,
                                                        correct_word_list)
        self._correct_transpositions(words, correct_word_list)
        self._general_command('(?i)(?<=[Aa])denomcarcinoa', {None : 'denocarcinoma'})
        self._general_command('(?i)(?<=[Dd])iagnosises', {None : 'iagnoses'})
        #self._general_command('(?i)(?<=[Ee])ddible', {None : 'dible'})
        #self._general_command('(?i)(?<=[Ee])strogren', {None : 'strogen'})
        self._general_command('(?i)(?<=[Ff])lorescen', {None : 'luorescen'})
        #self._general_command('(?i)(?<=[Pp])ateint', {None : 'atient'})
        #self._general_command('(?i)(?<=[Pp])ositve', {None : 'ositive'})
        #self._general_command('(?i)(?<=[Pp])ostiive', {None : 'ositive'})
        #self._general_command('(?i)(?<=[Pp])rogestrone', {None : 'rogesterone'})
        #self._general_command('(?i)(?<=[Rr])efrral', {None : 'eferral'})
        self._general_command('(?i)(?<=[Rr])epector', {None : 'eceptor'})
        #self._general_command('(?i)(?<=[Ss])erous', {None : 'erious'})
    
    #
    def _generate_correct_word_list(self, correct_seed_list):
        correct_word_list = []
        for seed in correct_seed_list:
            correct_word_list.append(seed)
            correct_word_list.append(seed[0].upper() + seed[1:])
            correct_word_list.append(seed.upper())
        correct_word_list = list(set(correct_word_list))
        return correct_word_list
    
    #
    def _generate_correct_word_list_with_plurals(self, correct_seed_list_in):
        engine = inflect.engine()
        correct_seed_list = []
        for seed in correct_seed_list_in:
            correct_seed_list.append(seed)
            correct_seed_list.append(engine.plural(seed))
        correct_word_list = []
        for seed in correct_seed_list:
            correct_word_list.append(seed)
            correct_word_list.append(seed[0].upper() + seed[1:])
            correct_word_list.append(seed.upper())
        correct_word_list = list(set(correct_word_list))
        return correct_word_list
    
    #
    def _process_general(self):
        self._general_command(' M [:/] E ', {None : ' M:E '})
        self._general_command(' N [:/] C ', {None : ' N:C '})
        self._general_command('(?i) n / a ', {None : ' n/a '})
        
    #
    def _process_medical_abbreviations(self):
        self._general_command('(?i) f / u ', {None : ' f/u '})
        self._general_command('(?i) h / o ', {None : ' h/o '})
        self._general_command('(?i) s / p ', {None : ' s/p '})
    
    #
    def process_document(self, text):
        self.text = text
        self._normalize_whitespace()
        self._correct_typos()
        self._process_general()
        self._process_medical_abbreviations()
        self._normalize_whitespace()  
        self.posttokenizer_antigens.push_text(self.text)
        self.posttokenizer_antigens.process_antigens()
        self.text = self.posttokenizer_antigens.pull_text()
        self.posttokenizer_cancer.push_text(self.text)
        self.posttokenizer_cancer.process_general()
        self.text = self.posttokenizer_cancer.pull_text()
        self.posttokenizer_histological_grade.push_text(self.text)
        self.posttokenizer_histological_grade.process_grade()
        self.text = self.posttokenizer_histological_grade.pull_text()
        self.posttokenizer_karyotype.push_text(self.text)
        self.posttokenizer_karyotype.process_karyotype()
        self.text = self.posttokenizer_karyotype.pull_text()
        self._clear_command_list()
        self._general_command('\( [0-9]+ - [0-9]+ \)', {' \)' : '.0 )'})
        self._general_command('\( [0-9]+ - [0-9]+\.[0-9]+ \)', {' - ' : '.0 - '})
        self._general_command('day 0( is equal to | ?= ?)', {None : ''})
        self._process_command_list()
        return self.text