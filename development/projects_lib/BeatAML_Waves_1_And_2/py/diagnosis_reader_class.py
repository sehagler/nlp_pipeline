# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 11:52:18 2019

@author: haglers
"""

#
import xlrd

#
class Diagnosis_reader(object):
    
    #
    def __init__(self, filename):
        book = xlrd.open_workbook(filename)
        self.diagnosis_dict = self._get_diagnosis_dict(book)
    
    #
    def _get_diagnosis_dict(self, book):
        diagnosis_dict = {}
        for idx in range(6):
            sheet = book.sheet_by_index(idx)
            diagnosis_dict[sheet.col_values(0)[0]] = {}
            diagnosis_dict[sheet.col_values(0)[0]]['abbreviation'] = sheet.col_values(1)[0]
            diagnosis_dict[sheet.col_values(0)[0]]['specific diagnosis'] = sheet.col_values(2)
        return diagnosis_dict
    
    #
    def get_dict_by_key(self, key):
        return self.diagnosis_dict[key]
        
    #
    def get_keys(self):
        return self.diagnosis_dict.keys() 