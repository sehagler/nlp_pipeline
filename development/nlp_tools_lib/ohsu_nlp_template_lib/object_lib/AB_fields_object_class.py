# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 12:40:03 2022

@author: haglers
"""

#
import nltk
nltk.download('stopwords')

#
import copy
import errno
from nltk.corpus import stopwords
import os
import random
import re

#
from tools_lib.regex_lib.regex_tools \
    import (
        article,
        be,
        conjunction,
        nonword,
        preposition,
        word
    )
from tools_lib.processing_tools_lib.file_processing_tools \
    import read_json_file

#
from tools_lib.processing_tools_lib.file_processing_tools \
    import read_xlsx_file, write_file

#
class AB_fields_object(object):
    
    #
    def __init__(self, static_data_object):
        self.static_data_object = static_data_object
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
    def _generalize_nonwords_template_outline(self, template_list):
        for i in range(len(template_list)):
            template_split = template_list[i].split(self.blank_space)
            for j in range(1, len(template_split)-1):
                word_var = template_split[j]
                if re.fullmatch(nonword(), word_var):
                    template_split[j] = '' #nonword()
            template_list[i] = self.blank_space.join(template_split)
        return template_list
    
    #
    def _generalize_grammatical_class_template_outline(self, template_list,
                                                       grammatical_class_regex):
        for i in range(len(template_list)):
            template_split = template_list[i].split(self.blank_space)
            for j in range(1, len(template_split)-1):
                word_var = template_split[j]
                if re.fullmatch(grammatical_class_regex, word_var):
                    template_split[j] = grammatical_class_regex
            template_list[i] = self.blank_space.join(template_split)
        return template_list
    
    #
    def _generate_phrases(self, template_list_in):
        template_list_out = []
        for i in range(len(template_list_in)):
            template = template_list_in[i]
            if len(template) > 0:
                phrase = template.split(self.blank_space)   
                for j in range(len(phrase)):
                    phrase[j] = '(?i)([^A-Za-z0-9 ]+[ \n\r])*' + phrase[j] + \
                                '([ \n\r][^A-Za-z0-9 ]+)*'
                template_list_out.append(phrase)
        return template_list_out
    
    #
    def _generalize_words_template_outline(self, template_list):
        stopwords_list = stopwords.words('english')
        for i in range(len(template_list)):
            template_split = template_list[i].split(self.blank_space)
            for j in range(1, len(template_split)-1):
                word_var = template_split[j]
                if re.fullmatch(word(), word_var) and \
                   word_var not in stopwords_list:
                    template_split[j] = word()
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
        AB_field_list = \
            self._infer_lower_order_templates(AB_field_list)
        AB_field_list = \
            self._sort_template_outline(AB_field_list)
        '''
        AB_field_list = \
            self._trim_template_outline(AB_field_list)
        AB_field_list = \
            self._sort_template_outline(AB_field_list)
        '''
        
        AB_field_list = self._generate_phrases(AB_field_list)

        '''        
        #
        AB_field_list = \
            self._replace_blank_spaces(AB_field_list)
        AB_field_list = \
            self._sort_template_outline(AB_field_list)
        #
        '''

        return AB_field_list 
    
    #
    def _infer_lower_order_templates(self, primary_template_list):
        generic_template_lengths = []
        for template in primary_template_list:
            template_list = template.split(self.blank_space)
            is_generic_template = True
            for item in template_list:
                if item != word():
                    is_generic_template = False
            if is_generic_template:
                generic_template_lengths.append(len(template_list))
        if len(generic_template_lengths) > 0:
            max_generic_template_length = max(generic_template_lengths)
            for i in range(max_generic_template_length - 1):
                template =  []
                for j in range(i):
                    template.append(word())
                primary_template_list.append(self.blank_space.join(template))
        return primary_template_list
                
    #
    def _number_of_generic_words(self, primary_template_list):
        N_generic_words = 0
        for i in range(len(primary_template_list)):
            template_list = primary_template_list[i].split(self.blank_space)
            for word_var in template_list:
                if word_var == '[A-Za-z0-9]+':
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
            for word_var in template_list:
                if word_var[:4] != 'NLP_':
                    N_words += 1
        return N_words
    
    #
    def _read_validation_data(self):
        static_data = self.static_data_object.get_static_data()
        validation_filename = static_data['validation_file']
        directory_manager = static_data['directory_manager']
        project_name = static_data['project_name']
        data_dir = directory_manager.pull_directory('raw_data_dir')
        filename = os.path.join(data_dir, validation_filename)
        validation_data = \
            self.xls_manager_registry[filename].read_validation_data()
        return validation_data
    
    #
    def _remove_newlines(self, text):
        text = re.sub('\n', ' ', text)
        text = re.sub(' +', ' ', text)
        return text
    
    #
    def _remove_newlines_template_outline(self, template_list):
        for i in range(len(template_list)):
            template_list[i] = \
                self._remove_newlines(template_list[i])
        return template_list
            
    #
    def _replace_blank_spaces(self, template_list):
        for i in range(len(template_list)):
            template_list[i] = \
                re.sub(self.blank_space, '[ \n\r]([^A-Za-z0-9 ]+[ \n\r])*', template_list[i])
        return template_list
    
    #
    def _sort_template_outline(self, template_list):
        if '' in template_list:
            template_list.remove('')
        template_list = list(set(template_list))
        for i in range(len(template_list)):
            template_list[i] = template_list[i].split(self.blank_space)
        template_list = sorted(template_list, key=len, reverse=True)
        for i in range(len(template_list)):
            template_list[i] = self.blank_space.join(template_list[i])
        return template_list
    
    #
    def _train(self, primary_template_list, A_charge, B_charge):          
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
                                                                article())
        primary_template_list = \
            self._generalize_grammatical_class_template_outline(primary_template_list,
                                                                be())
        primary_template_list = \
            self._generalize_grammatical_class_template_outline(primary_template_list,
                                                                conjunction())
        primary_template_list = \
            self._generalize_grammatical_class_template_outline(primary_template_list,
                                                                preposition())
        primary_template_list = \
            self._trim_blank_spaces(primary_template_list)
        primary_template_list = \
            self._sort_template_outline(primary_template_list)
        AB_field_list = self._generate_XY_field_list(primary_template_list,
                                                     A_charge, B_charge)
        BA_field_list = self._generate_XY_field_list(primary_template_list,
                                                     B_charge, A_charge)
        self.template_manager.push_primary_template_list(AB_field_list,
                                                         BA_field_list)
    
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
    def _trim_template_outline(self, primary_template_list):
        N_list = []
        for i in range(len(primary_template_list)):
            template_list = primary_template_list[i].split(self.blank_space)
            N_list.append(len(template_list))
            N_list = sorted(N_list, reverse=True)
        if 1 in N_list:
            N_list.remove(1)
        primary_template_list_out = []
        for N in N_list:
            primary_template_list_N = []
            for i in range(len(primary_template_list)):
                template_list = primary_template_list[i].split(self.blank_space)
                if len(template_list) == N:
                    primary_template_list_N.append(primary_template_list[i])
            generic_template_exists = False
            for i in range(len(primary_template_list_N)):
                X = list(set(primary_template_list_N[i].split(self.blank_space)))
                if len(X) == 1 and X[0] == word():
                    generic_template_exists = True
                    generic_template = X
            if generic_template_exists:
                for i in range(len(primary_template_list_N)):
                    primary_template_list.remove(primary_template_list_N[i])
                primary_template_list.append(self.blank_space.join(generic_template))
        return primary_template_list
    
    #
    def train_template(self, template_manager, metadata_manager, data_dir,
                       text_dict):
        self.template_manager = template_manager
        self.metadata_manager = metadata_manager
        self.data_dir = data_dir
        self.text_dict = text_dict
        A_charge = template_manager.pull_A_charge()
        B_charge = template_manager.pull_B_charge()
        primary_template_list = \
            template_manager.pull_primary_template_list()
        self._train(primary_template_list, A_charge, B_charge)
        template_dict = template_manager.training_template()
        self.AB_field_list = template_dict['AB_field_list']
        self.BA_field_list = template_dict['BA_field_list']
        
    #
    def write_ab_fields(self, template_outlines_dir, filename):
        filename = os.path.join(template_outlines_dir, filename)
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open(os.path.join(filename + '_AB_field.txt'), 'w+') as f:
            f.write(str(self.AB_field_list))
        with open(os.path.join(filename + '_BA_field.txt'), 'w+') as f:
            f.write(str(self.BA_field_list))