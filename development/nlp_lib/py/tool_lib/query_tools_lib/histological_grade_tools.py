# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 11:45:17 2020

@author: haglers
"""

#
from nlp_lib.py.base_class_lib.preprocessor_base_class import Preprocessor_base

#
class Named_entity_recognition(Preprocessor_base):
        
    #
    def process_msbr(self):
        self._clear_command_list()
        text_list = []
        text_list.append('(?i)modified Scarff(-| )Bloom(-| )(and(-| ))?Richardson( \(mSBR\))?')
        text_list.append('(?i)modified Bloom(-| )(and(-| ))?Richardson( \(mBR\))?')
        text_list.append('(?i)Scarff(-| )Bloom(-| )(and(-| ))?Richardson( \(SBR\))?')
        text_list.append('(?i)modified Richardson')
        text_list.append('(?i)Bloom(-| )(and(-| ))?Richardson( \(BR\))?')
        self._general_command(text_list, {None : 'mSBR'})
        self._process_command_list()

#
class Posttokenizer(Preprocessor_base):

    #
    def process_grade(self):
        self._clear_command_list()
        self._general_command('(?<= )I( / | of )III(?=( |\n))', {None : '1 / 3'})
        self._general_command('(?<= )II( / | of )III(?=( |\n))', {None : '2 / 3'})
        self._general_command('(?<= )III( / | of )III(?=( |\n))', {None : '3 / 3'})
        self._general_command('(?<= )1 of 3(?=( |\n))', {None : '1 / 3'})
        self._general_command('(?<= )2 of 3(?=( |\n))', {None : '2 / 3'})
        self._general_command('(?<= )3 of 3(?=( |\n))', {None : '3 / 3'})
        self._process_command_list()

#
class Summarization(Preprocessor_base):
    
    #
    def process_mitotic_rate(self):
        self._clear_command_list()
        self._general_command('(?i)(points )?for mito(s(e|i)s|tic)( (activity|count|figure(s)?|index|rate))',
                              {None : 'for mitoses'})
        match_str0 = '(?i)mito(s(e|i)s|tic)( (activity|count|figure(s)?|index|rate))? \( \d \)'
        match_str1 = '(?i)mito(s(e|i)s|tic)( (activity|count|figure(s)?|index|rate))?'
        self._general_command(match_str0, {match_str1: 'mitoses = '})
        match_str0 = '(?i)mito(s(e|i)s|tic)( (activity|count|figure(s)?|index|rate))?' + \
                     '(:)?((\s)?(grade|score)?( of)?)? \d'
        match_str1 = '(?i)mito(s(e|i)s|tic)( (activity|count|figure(s)?|index|rate))?' + \
                     '(:)?((\s)?(grade|score)?( of)?)?'
        self._general_command(match_str0, {match_str1: 'mitoses = '})
        self._general_command('(?i)mito(ses|sis|tic) (activity|count|figure(s)?|index|rate)',
                              {None : 'mitoses'})
        self._general_command('(?i)mitos(e|i)s', {None : 'mitoses'})
        self._general_command('(?i)mito(ses|sis|tic) (activity|count|figure(s)?|index|rate)',
                              {None : 'mitoses'})
        self._general_command('(?i) mitoses per ', {None : '/'})
        self._general_command(' a mitoses', {None : ' mitoses'})
        self._process_command_list()
        
    #
    def process_nuclear_pleomorphism(self):
        self._clear_command_list()
        self._general_command('(?i)pleomorphism', {None : 'nuclear pleomorphism'} )
        self._general_command('(?i)nuclear nuclear', {None : 'nuclear'})
        self._general_command('(?i)(points )?for nuclear (atypia|grade|pleomorphism|score)',
                              {None : 'for nuclei'})
        match_str = '(?i)nuclear (atypia|grade|pleomorphism|score) \( \d \)'
        self._general_command(match_str, {' \)': ''})
        match_str = '(?i)nuclear (atypia|grade|pleomorphism|score) \( \d'
        self._general_command(match_str, {'\( ': ''})
        match_str0 = '(?i)nuclear (atypia|grade|pleomorphism|score) \d'
        match_str1 = '(?i)nuclear (atypia|grade|pleomorphism|score)'
        self._general_command(match_str0, {match_str1: 'nuclei = '})
        match_str0 = '(?i)nucle(ar|i)( (atypia|grade|pleomorphism|score))?' + \
                    '(:)?((\s)?(grade|score)?( of)?)? \d'
        match_str1 = '(?i)nucle(ar|i)( (atypia|grade|pleomorphism|score))?' + \
                    '(:)?((\s)?(grade|score)?( of)?)?'
        self._general_command(match_str0, {match_str1: 'nuclei = '})
        self._general_command('(?i)nuclei', {None : 'nuclei'})
        self._general_command('(?i)nuclear (atypia|grade|pleomorphism|score)',
                              {None : 'nuclei'})
        self._general_command(' a nuclei', {None : ' nuclei'})
        self._process_command_list()
        
    #
    def process_tubule_formation(self):
        self._clear_command_list()
        match_str = '(?i)(points )?for (glandular )?(\(acinar\)-)?tub(al|ular|ule(s)?)' + \
                    '( (differentiation|formation))?'
        self._general_command(match_str, {None : 'for tubules'})
        match_str = '(?i)(glandular )?(\(acinar\)-)?tub(al|ular|ule(s)?)' + \
                    '( (differentiation|formation))? \( \d \)'
        self._general_command(match_str, {' \)': ''})
        match_str = '(?i)(glandular )?(\(acinar\)-)?tub(al|ular|ule(s)?)' + \
                    '( (differentiation|formation))? \( \d'
        self._general_command(match_str, {'\( ': ''})
        match_str0 = '(?i)(glandular )?(\(acinar\)-)?tub(al|ular|ule(s)?)' + \
                     '( (differentiation|formation))? \d'
        match_str1 = '(?i)(glandular )?(\(acinar\)-)?tub(al|ular|ule(s)?)' + \
                     '( (differentiation|formation))?'
        self._general_command(match_str0, {match_str1: 'tubules = '})
        match_str0 = '(?i)(glandular )?(\(acinar\)-)?tub(al|ular|ule(s)?)' + \
                     '( (differentiation|formation))?' + \
                     '(:)?((\s)?(grade|score)?( of)?)? \d'
        match_str1 = '(?i)(glandular )?(\(acinar\)-)?tub(al|ular|ule(s)?)' + \
                     '( (differentiation|formation))?' + \
                     '(:)?((\s)?(grade|score)?( of)?)?'
        self._general_command(match_str0, {match_str1: 'tubules = '})
        match_str = '(?i)(glandular )?(\(acinar\)-)?tub(al|ular|ule(s)?)' + \
                    '( (differentiation|formation))'
        self._general_command(match_str, {None : 'tubules'})
        self._general_command(' a tubules', {None : ' tubules'})
        self._process_command_list()