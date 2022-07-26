# -*- coding: utf-8 -*-
"""
Created on Fri May  6 15:38:06 2022

@author: haglers
"""

#
import nltk
nltk.download('stopwords')

#
import copy
from nltk.corpus import stopwords
import os
import random
import re

#
from nlp_tools_lib.ohsu_nlp_template_lib.py.worker_lib.worker_base_class \
    import Worker_base
from tool_lib.py.processing_tools_lib.file_processing_tools \
    import read_json_file
from tool_lib.py.processing_tools_lib.text_processing_tools \
    import regex_from_list

#
class Training_worker(Worker_base):
    
    #
    def __init__(self, static_data_manager, template_manager, metadata_manager,
                 data_dir, text_dict):
        Worker_base.__init__(self)
        self.static_data_manager = static_data_manager
        self.template_manager = template_manager
        self.metadata_manager = metadata_manager
        self.data_dir = data_dir
        self.text_dict = text_dict
        self.blank_space = ' NLP_BLANK_SPACE '
        
    #
    def _annotate_blank_space(self, template_list):
        for i in range(len(template_list)):
            template_list[i] = \
                re.sub(' ', self.blank_space, template_list[i])
        return template_list
                          
    #
    def _cost(self, primary_template_list, performance):
        N_generic_words = self._number_of_generic_words(primary_template_list)
        N_templates = self._number_of_templates(primary_template_list)
        N_words = self._number_of_words(primary_template_list)
        cost = performance[1] - performance[0] - N_generic_words
        cost = - N_generic_words
        return cost
    
    #
    def _escape_template_list(self, template_list):
        for i in range(len(template_list)):
            template_list[i] = re.sub('\(', '\(', template_list[i])
            template_list[i] = re.sub('\)', '\)', template_list[i])
            template_list[i] = re.sub('\.', '\.', template_list[i])
            template_list[i] = re.sub('\+', '\+', template_list[i])
        return template_list
        
    #
    def _finish_templates(self, template_list):
        for i in range(len(template_list)):
            template_list[i] = \
                re.sub(self.blank_space, '[ \n\r]([^A-Za-z0-9 ]+[ \n\r])*', template_list[i])
            template_list[i] = \
                '(?i)([^A-Za-z0-9 ]+[ \n\r])*' + template_list[i] + '([ \n\r][^A-Za-z0-9 ]+)*'
        template_list.append('(?i)([^A-Za-z0-9 ]+[ \n\r])*[^A-Za-z0-9 ]+')
        return template_list
    
    #
    def _generalize_nonwords_template_outline(self, template_list):
        for i in range(len(template_list)):
            template_split = template_list[i].split(self.blank_space)
            for j in range(1, len(template_split)-1):
                word = template_split[j]
                if re.fullmatch(self._generic_nonword(), word):
                    template_split[j] = '' #self._generic_nonword()
            template_list[i] = self.blank_space.join(template_split)
        return template_list
    
    #
    def _generalize_grammatical_class_template_outline(self, template_list,
                                                       grammatical_class_regex):
        for i in range(len(template_list)):
            template_split = template_list[i].split(self.blank_space)
            for j in range(1, len(template_split)-1):
                word = template_split[j]
                if re.fullmatch(grammatical_class_regex, word):
                    template_split[j] = grammatical_class_regex
            template_list[i] = self.blank_space.join(template_split)
        return template_list
    
    #
    def _generalize_words_template_outline(self, template_list):
        stopwords_list = stopwords.words('english')
        for i in range(len(template_list)):
            template_split = template_list[i].split(self.blank_space)
            for j in range(1, len(template_split)-1):
                word = template_split[j]
                if re.fullmatch(self._generic_word(), word) and \
                   word not in stopwords_list:
                    template_split[j] = self._generic_word()
            template_list[i] = self.blank_space.join(template_split)
        return template_list
        
    #
    def _generate_XY_field_list(self, primary_template_list, A_label, B_label):
        AB_field_list = []
        for i in range(len(primary_template_list)):
            template_list = primary_template_list[i].split(self.blank_space)
            if A_label in template_list:
                A_idx = template_list.index(A_label)
            else:
                A_idx = None
            if B_label in template_list:
                B_idx = template_list.index(B_label)
            else:
                B_idx = None
            if A_idx is not None and B_idx is not None:
                field_idxs = list(range(A_idx+1, B_idx))
                field_list = []
                for j in range(len(field_idxs)):
                    field_list.append(template_list[field_idxs[j]])
                AB_field_list.append(self.blank_space.join(field_list))
        AB_field_list = list(set(AB_field_list))
        AB_field_list = sorted(AB_field_list, key=len, reverse=True)
        if '' in AB_field_list:
            AB_field_list.remove('')
        AB_field_list = \
            self._finish_templates(AB_field_list)
        return AB_field_list 
    
    #
    def _generic_article(self):
        article_list = [ 'an?', 'the' ]
        return regex_from_list(article_list)
    
    #
    def _generic_conjunction(self):
        conjunction_list = [ 'and', 'or' ]
        return regex_from_list(conjunction_list)
    
    #
    def _generic_nonword(self):
        return '[^A-Za-z0-9 ]+'
    
    #
    def _generic_preposition(self):
        preposition_list = [ 'after', 'at', 'for', 'in', 'of', 'on', 'to', 'with' ]
        return regex_from_list(preposition_list)
        
    #
    def _generic_word(self):
        return '[A-Za-z0-9]+([\-/][A-Za-z0-9]+)?'
                
    #
    def _number_of_generic_words(self, primary_template_list):
        N_generic_words = 0
        for i in range(len(primary_template_list)):
            template_list = primary_template_list[i].split(self.blank_space)
            for word in template_list:
                if word == '[A-Za-z0-9]+':
                    N_generic_words += 1
        return N_generic_words
    
    #
    def _number_of_templates(self, primary_template_list):
        return len(primary_template_list)
    
    #
    def _number_of_words(self, primary_template_list):
        N_words = 0
        for i in range(len(primary_template_list)):
            template_list = primary_template_list[i].split(self.blank_space)
            for word in template_list:
                if word[:4] != 'NLP_':
                    N_words += 1
        return N_words
    
    #
    def _read_validation_data(self):
        static_data = self.static_data_manager.get_static_data()
        validation_filename = static_data['validation_file']
        directory_manager = static_data['directory_manager']
        project_name = static_data['project_name']
        data_dir = directory_manager.pull_directory('raw_data_dir')
        filename = os.path.join(data_dir, validation_filename)
        validation_data = \
            self.xls_manager_registry[filename].read_validation_data()
        return validation_data
    
    #
    def _remove_newlines_template_outline(self, template_list):
        for i in range(len(template_list)):
            template_list[i] = \
                self._remove_newlines(template_list[i])
        return template_list
    
    #
    def _trim_context(self, template_list):
        #template_list_add = []
        for i in range(len(template_list)):
            template_split = template_list[i].split(self.blank_space)
            delete_idxs = []
            delete_flg = True
            for j in range(len(template_split)):
                if delete_flg:
                    if 'NLP_' in template_split[j]:
                        delete_flg = False
                    else:
                        delete_idxs.append(j)
                else:
                    if 'NLP_' in template_split[j]:
                        delete_flg = True
            if len(delete_idxs) > 0:
                delete_idxs = sorted(delete_idxs, reverse=True)
                for j in range(len(delete_idxs)):
                    del template_split[delete_idxs[j]]
                template_list[i] = \
                    self.blank_space.join(template_split)
                #template_list_add.append(self.blank_space.join(template_split))
        #template_list.extend(template_list_add)
        return template_list
    
    #
    def _trim_blank_spaces(self, primary_template_list):
        for i in range(len(primary_template_list)):
            primary_template_list[i] = \
                re.sub('(' +  self.blank_space + ')+', self.blank_space, primary_template_list[i])
            primary_template_list[i] = \
                re.sub('^' + self.blank_space, '', primary_template_list[i])
            primary_template_list[i] = \
                re.sub(self.blank_space + '$', '', primary_template_list[i])
        return primary_template_list
    
    #
    def _trim_template_outline(self, primary_template_list_in):
        primary_template_list_in = list(set(primary_template_list_in))
        N_list = []
        for i in range(len(primary_template_list_in)):
            template_list = primary_template_list_in[i].split(self.blank_space)
            N_list.append(len(template_list))
        N_list = list(set(N_list))
        N_list = sorted(N_list, reverse=True)
        primary_template_list_out = []
        for N in N_list:
            primary_template_list_N = []
            for i in range(len(primary_template_list_in)):
                template_list = primary_template_list_in[i].split(self.blank_space)
                if len(template_list) == N:
                    primary_template_list_N.append(primary_template_list_in[i])
            if N > 1:
                delete_idxs = []
                for i in range(len(primary_template_list_N)):
                    for j in range(len(primary_template_list_N)):
                        if i != j:
                            X = primary_template_list_N[i].split(self.blank_space)
                            Y = primary_template_list_N[j].split(self.blank_space)
                            diffs = [(X[x], Y[x]) for x in range(len(X)) if X[x] != Y[x]]
                            delete_flg = False
                            continue_flg = True
                            for diff in diffs:
                                if diff[0] != self._generic_word():
                                    continue_flg = False
                            if continue_flg:
                                delete_flg = True
                                for diff in diffs:
                                    if not re.fullmatch(self._generic_word(), diff[1]):
                                        delete_flg = False
                            if delete_flg:
                                delete_idxs.append(j)
                delete_idxs = list(set(delete_idxs))
                delete_idxs = sorted(delete_idxs, reverse=True)
                for i in range(len(delete_idxs)):
                    del primary_template_list_N[delete_idxs[i]]
            for template_outline in primary_template_list_N:
                primary_template_list_out.append(template_outline)
        return primary_template_list_out
    
    #
    def train(self, primary_template_list, A_charge, B_charge):          
        primary_template_list = \
            self._remove_newlines_template_outline(primary_template_list)
        primary_template_list = \
            self._annotate_blank_space(primary_template_list)
        primary_template_list = \
            self._trim_context(primary_template_list)
        primary_template_list = \
            self._escape_template_list(primary_template_list)
        primary_template_list = \
            self._generalize_words_template_outline(primary_template_list)
        primary_template_list = \
            self._generalize_nonwords_template_outline(primary_template_list)
        primary_template_list = \
            self._generalize_grammatical_class_template_outline(primary_template_list,
                                                                self._generic_article())
        primary_template_list = \
            self._generalize_grammatical_class_template_outline(primary_template_list,
                                                                self._generic_conjunction())
        primary_template_list = \
            self._generalize_grammatical_class_template_outline(primary_template_list,
                                                                self._generic_preposition())
        primary_template_list = \
            self._trim_blank_spaces(primary_template_list)
        primary_template_list = \
            self._trim_template_outline(primary_template_list)
        AB_field_list = self._generate_XY_field_list(primary_template_list,
                                                     A_charge, B_charge)
        BA_field_list = self._generate_XY_field_list(primary_template_list,
                                                     B_charge, A_charge)
        primary_template_list = self._finish_templates(primary_template_list)
        self.template_manager.push_primary_template_list(AB_field_list,
                                                            BA_field_list,
                                                            primary_template_list)