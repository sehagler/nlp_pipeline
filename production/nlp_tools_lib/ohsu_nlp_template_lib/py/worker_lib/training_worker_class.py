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
                 xls_manager_registry, xls_manager, data_dir, text_dict):
        Worker_base.__init__(self)
        self.static_data_manager = static_data_manager
        self.template_manager = template_manager
        self.metadata_manager = metadata_manager
        self.xls_manager_registry = xls_manager_registry
        self.xls_manager = xls_manager
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
    def _cost(self, primary_template_outline, performance):
        N_generic_words = self._number_of_generic_words(primary_template_outline)
        N_templates = self._number_of_templates(primary_template_outline)
        N_words = self._number_of_words(primary_template_outline)
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
    def _evaluate_performance(self):
        metadata_json_file = self.metadata_manager.get_metadata_json_file()
        metadata = read_json_file(metadata_json_file)
        csn_list = self.xls_manager.column("CSN")
        validation_data_list = self.xls_manager.column('RAW_CANCER_STAGE_EXTRACT')
        validation_data = self._read_validation_data()
        template_dict = self.template_manager.training_template()
        primary_template_list = template_dict['primary_template_list']
        if 'secondary_template_list' in template_dict.keys():
            secondary_template_list = template_dict['secondary_template_list']
        else:
            secondary_template_list = []
        template_sections_list = template_dict['sections_list']
        self._apply_template(primary_template_list,
                             secondary_template_list,
                             template_sections_list, self.text_dict)
        performance_correct_ctr = 0
        performance_incorrect_ctr = 0
        for i in range(len(csn_list)):
            csn = csn_list[i]
            for key in metadata.keys():
                if metadata[key]['METADATA']['SOURCE_SYSTEM_DOCUMENT_ID'] == csn:
                    hit_list = []
                    for item in self.template_output:
                        if item[0] == key:
                            hit_list.append(item[4])
                    hit_list = list(set(hit_list))
                    for item in hit_list:
                        if item == validation_data_list[i]:
                            performance_correct_ctr += 1
                        else:
                            performance_incorrect_ctr += 1
        performance = [ performance_correct_ctr, performance_incorrect_ctr ]
        return performance
    
    #
    def _generalize_nonwords_template_outline(self, template_list):
        for i in range(len(template_list)):
            template_split = template_list[i].split(self.blank_space)
            for j in range(1, len(template_split)-1):
                word = template_split[j]
                if re.fullmatch(self._generic_nonword(), word):
                    template_split[j] = self._generic_nonword()
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
        return '[A-Za-z0-9]+(\-[A-Za-z0-9]+)?'
                
    #
    def _number_of_generic_words(self, primary_template_outline):
        N_generic_words = 0
        for i in range(len(primary_template_outline)):
            template_list = primary_template_outline[i].split(self.blank_space)
            for word in template_list:
                if word == '[A-Za-z0-9]+':
                    N_generic_words += 1
        return N_generic_words
    
    #
    def _number_of_templates(self, primary_template_outline):
        return len(primary_template_outline)
    
    #
    def _number_of_words(self, primary_template_outline):
        N_words = 0
        for i in range(len(primary_template_outline)):
            template_list = primary_template_outline[i].split(self.blank_space)
            for word in template_list:
                if word[:4] != 'NLP_':
                    N_words += 1
        return N_words
    
    '''
    #
    def _perturb_generic_word(self, primary_template_outline):
        stopwords_list = stopwords.words('english')
        i = random.choice(range(len(primary_template_outline)))
        template_list = primary_template_outline[i].split(self.blank_space)
        j = random.choice(range(len(template_list)))
        word = template_list[j]
        if re.fullmatch(self._generic_word(), word) and \
           word not in stopwords_list:
            template_list[j] = self._generic_word()
            primary_template_outline[i] = self.blank_space.join(template_list)
        return primary_template_outline

    #
    def _perturb_primary_template_outline(self, primary_template_outline):
        primary_template_outline = \
            self._perturb_generic_word(primary_template_outline)
        return primary_template_outline
    '''
    
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
    def _trim_template_outline(self, primary_template_outline_in):
        primary_template_outline_in = list(set(primary_template_outline_in))
        N_list = []
        for i in range(len(primary_template_outline_in)):
            template_list = primary_template_outline_in[i].split(self.blank_space)
            N_list.append(len(template_list))
        N_list = list(set(N_list))
        N_list = sorted(N_list, reverse=True)
        primary_template_outline_out = []
        for N in N_list:
            primary_template_outline_N = []
            for i in range(len(primary_template_outline_in)):
                template_list = primary_template_outline_in[i].split(self.blank_space)
                if len(template_list) == N:
                    primary_template_outline_N.append(primary_template_outline_in[i])
            if N > 1:
                delete_idxs = []
                for i in range(len(primary_template_outline_N)):
                    for j in range(len(primary_template_outline_N)):
                        if i != j:
                            X = primary_template_outline_N[i].split(self.blank_space)
                            Y = primary_template_outline_N[j].split(self.blank_space)
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
                    del primary_template_outline_N[delete_idxs[i]]
            for template_outline in primary_template_outline_N:
                primary_template_outline_out.append(template_outline)
        return primary_template_outline_out
    
    #
    def train(self):
        primary_template_outline = \
            self.xls_manager.column('ANNOTATED_CANCER_STAGE_EXTRACT')
        primary_template_outline = \
            self._annotate_blank_space(primary_template_outline)
        primary_template_outline = \
            self._trim_context(primary_template_outline)
        primary_template_outline = \
            self._escape_template_list(primary_template_outline)
        primary_template_outline = \
            self._generalize_words_template_outline(primary_template_outline)
        primary_template_outline = \
            self._generalize_nonwords_template_outline(primary_template_outline)
        primary_template_outline = \
            self._generalize_grammatical_class_template_outline(primary_template_outline,
                                                                self._generic_article())
        primary_template_outline = \
            self._generalize_grammatical_class_template_outline(primary_template_outline,
                                                                self._generic_conjunction())
        primary_template_outline = \
            self._generalize_grammatical_class_template_outline(primary_template_outline,
                                                                self._generic_preposition())
        primary_template_outline = \
            self._remove_newlines_template_outline(primary_template_outline)
        primary_template_outline = \
            self._trim_template_outline(primary_template_outline)
        self.template_manager.push_primary_template_outline(primary_template_outline)
        
        '''
        num_epochs = 25
        self.template_manager.push_primary_template_outline(primary_template_seed)
        performance = self._evaluate_performance()
        cost = self._cost(primary_template_seed, performance)
        primary_template_outline_best = copy.deepcopy(primary_template_seed)
        cost_best = copy.copy(cost)
        primary_template_outline = copy.deepcopy(primary_template_seed)
        for _ in range(num_epochs):
            primary_template_outline = \
                self._perturb_primary_template_outline(primary_template_outline)
            if primary_template_outline != primary_template_outline_best:
                self.template_manager.push_primary_template_outline(primary_template_outline)
                performance = self._evaluate_performance()
                cost = self._cost(primary_template_outline, performance)
                if cost < cost_best:
                    primary_template_outline_best = copy.deepcopy(primary_template_outline)
                    cost_best = copy.copy(cost)
        print(cost_best)
        '''