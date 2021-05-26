# -*- coding: utf-8 -*-
"""
Created on Mon Mar 04 10:19:41 2019

@author: haglers
"""

#
import json
import os
import xlrd

#
class Specimens_base(object):

    #
    def _get_deidentifier_keys(self):
        deidentifier_key_dict = {}
        book = xlrd.open_workbook(self.deidentifier_xlsx)
        sheet = book.sheet_by_index(0)
        patientids = sheet.col_values(0)[1:]
        mrns = sheet.col_values(1)[1:]
        labids = sheet.col_values(2)[1:]
        specimen_dates = self._make_strings(sheet.col_values(3)[1:])
        for mrn in list(set(mrns)):
            idxs = [ i for i, j in enumerate(mrns) if j == mrn ]
            patientid_tmp = list(set([ patientids[i] for i in idxs ]))
            for i in range(len(patientid_tmp)):
                patientid_tmp[i] = int(patientid_tmp[i])
            tmp_list = [ [labids[i], specimen_dates[i]] for i in idxs ]
            doc_dict = {}
            for item in tmp_list:
                doc_dict[item[1]] = item[0]
            if len(patientid_tmp) == 1:
                deidentifier_key_dict[mrn] = {}
                deidentifier_key_dict[mrn]['patientId'] = str(patientid_tmp[0])
                deidentifier_key_dict[mrn]['labIds'] = doc_dict
        return deidentifier_key_dict
    
    #
    def _make_strings(self, column_values):
        for i in range(len(column_values)):
            column_values[i] = str(column_values[i])
        return column_values
    
    #
    def generate_json_file(self, jsons_out_dir, filename):
        with open(os.path.join(jsons_out_dir, filename), 'w') as f:
            json.dump(self.data_json, f)
            
    #
    def get_data_json(self):
        return self.data_json
    
    #
    def get_data_json_counts(self, data_json):
        print(len(data_json.keys()))
        ctr = 0
        for key in data_json.keys():
            ctr += len(data_json[key].keys())
        print(ctr)