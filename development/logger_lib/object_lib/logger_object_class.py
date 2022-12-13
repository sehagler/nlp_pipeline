# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 11:10:44 2019

@author: haglers
"""

#
import os
import traceback

#
class Logger_object(object):
    
    #
    def __init__(self, log_dir):
        self.log_dir = log_dir
        self.log_list = []
        
    #
    def create_file(self, filename):
        for i in range(len(self.log_list)):
            for j in range(len(self.log_list[i])):
                self.log_list[i][j] = ''.join(str(self.log_list[i][j]))
        log_text = ''
        for item in self.log_list:
            entry = ''
            for element in item:
                entry += '\t' + element
            log_text += '\n' + entry[1:]
        log_text = log_text[1:] + '\n'
        with open(os.path.join(self.log_dir, filename), 'w') as f:
            f.write(log_text)
        
    #
    def log_entry(self, patientId, labId, data_item, value0, value1):
        try:
            item = [ str(patientId), str(labId), str(data_item), str(value0), str(value1) ]
        except Exception:
            traceback.print_exc()
            item = []
        self.log_list.append(item)
        
    #
    def log_entry_merge_documents(self, MRN, specimen_date, date_str, delta_day, documents_in):
        delta_day = 'N\A'
        documents_out = documents_in
        item = [ str(MRN), str(specimen_date), str(date_str), str(delta_day), documents_out ]
        log_list_tmp = self.log_list
        for entry in log_list_tmp:
            if item[0] == entry[0] and item[1] == entry[1] and item[2] == entry[2] and item[3] == entry[3]:
                documents_out.extend(entry[4])
                documents_out = list(set(documents_out))
                item = [ str(MRN), str(specimen_date), str(date_str), str(delta_day), documents_out ]
                self.log_list.remove(entry)
        self.log_list.append(item)