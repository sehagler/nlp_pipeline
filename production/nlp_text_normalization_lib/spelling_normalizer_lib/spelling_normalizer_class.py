# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 08:56:52 2021

@author: haglers
"""
#
import distance
import inflect
import re

#
import lambda_lib.tool_lib.lambda_tools as lambda_tools

#
class Spelling_normalizer(object):
            
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
                self.text = \
                    lambda_tools.lambda_conversion(correction, self.text, correct_word)
                
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
                        self.text = \
                            lambda_tools.lambda_conversion(correction, self.text, correct_word)
    
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
        self.text = \
            lambda_tools.lambda_conversion('(?<=a)denomcarcinoa', self.text, 'denocarcinoma')
        self.text = \
            lambda_tools.lambda_conversion('(?<=d)iagnosises', self.text, 'iagnoses')
        self.text = \
            lambda_tools.lambda_conversion('(?<=f)lorescen', self.text, 'luorescen')
        self.text = \
            lambda_tools.lambda_conversion('(?<=r)epector', self.text, 'eceptor')
    
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
    def normalize_text(self, text):
        self.text = text
        self._correct_typos()
        return self.text