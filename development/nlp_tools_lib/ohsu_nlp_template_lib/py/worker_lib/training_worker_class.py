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
                          
    #
    def _cost(self, primary_template_outline, performance):
        N_generic_words = self._number_of_generic_words(primary_template_outline)
        N_templates = self._number_of_templates(primary_template_outline)
        N_words = self._number_of_words(primary_template_outline)
        cost = performance[1] - performance[0] - N_generic_words
        cost = - N_generic_words
        return cost
    
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
    def _generic_word(self):
        return '[A-Za-z0-9]+(\-[A-Za-z0-9]+)?'
    
    #
    def _maximally_generalize_template_outline(self, primary_template_outline):
        stopwords_list = stopwords.words('english')
        primary_template_outline = list(set(primary_template_outline))
        for i in range(len(primary_template_outline)):
            template_list = primary_template_outline[i].split(' ')
            for j in range(1, len(template_list)-1):
                word = template_list[j]
                if re.fullmatch(self._generic_word(), word) and \
                   word not in stopwords_list:
                    template_list[j] = self._generic_word()
            primary_template_outline[i] = ' '.join(template_list)
        primary_template_outline = list(set(primary_template_outline))
        primary_template_outline = \
            sorted(primary_template_outline, key=len)
        return primary_template_outline
                
                
    #
    def _number_of_generic_words(self, primary_template_outline):
        N_generic_words = 0
        for i in range(len(primary_template_outline)):
            template_list = primary_template_outline[i].split(' ')
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
            template_list = primary_template_outline[i].split(' ')
            for word in template_list:
                if word[:4] != 'NLP_':
                    N_words += 1
        return N_words
    
    #
    def _perturb_generic_word(self, primary_template_outline):
        stopwords_list = stopwords.words('english')
        i = random.choice(range(len(primary_template_outline)))
        template_list = primary_template_outline[i].split(' ')
        j = random.choice(range(len(template_list)))
        word = template_list[j]
        if re.fullmatch(self._generic_word(), word) and \
           word not in stopwords_list:
            template_list[j] = self._generic_word()
            primary_template_outline[i] = ' '.join(template_list)
        return primary_template_outline

    #
    def _perturb_primary_template_outline(self, primary_template_outline):
        primary_template_outline = \
            self._perturb_generic_word(primary_template_outline)
        return primary_template_outline
    
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
    def train(self):
        #num_epochs = 25
        primary_template_seed = \
            self.xls_manager.column('ANNOTATED_CANCER_STAGE_EXTRACT')
        '''
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
        primary_template_outline_best = \
           self._maximally_generalize_template_outline(primary_template_seed)
        primary_template_outline = list(set(primary_template_outline_best))
        self.template_manager.push_primary_template_outline(primary_template_outline)