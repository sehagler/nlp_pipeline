# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 14:57:36 2022

@author: haglers
"""

#
import os
import re

#
from nlp_pipeline_lib.file_lib.base_class_lib.reader_base_class import Reader_base
from tool_lib.py.processing_tools_lib.file_processing_tools import read_xlsx_file
    
#
class Xls_manager(Reader_base):
        
    #
    def _read_data_file(self, raw_data_files_dict, raw_data_file):
        dt_labels = self.static_data['datetime_keys']
        key_label = 'REPORT_HEADER'
        if 'BeatAML' in self.static_data['project_name']:
            key_value_list = [ 'Final Diagnosis', 'Final Pathologic Diagnosis',
                               'Karyotype', 'Clinical History',
                               'Immunologic Analysis', 'Laboratory Data',
                               'Microscopic Description',
                               'Cytogenetic Analysis Summary',
                               'Impressions and Recommendations' ]
        elif self.static_data['project_name'] == 'BreastCancerPathology':
            key_value_list = [ 'Final Pathologic Diagnosis' ]
        data = {}
        book = read_xlsx_file(raw_data_file)
        sheet = book.sheet_by_index(0)
        keys = sheet.row(0)
        for i in range(len(keys)):
            keys[i] = str(keys[i].value)
        if 'FILENAME' not in data.keys():
            data['FILENAME'] = []
        if 'NLP_MODE' not in data.keys():
            data['NLP_MODE'] = []
        for key in keys:
            if key not in data.keys():
                data[key] = []
        for row_idx in range(1, sheet.nrows):
            row = sheet.row(row_idx)
            idx = [ i for i, x in enumerate(keys) if x == key_label]
            REPORT_KEY_tmp = re.sub(':', '', row[idx[0]].value)
            if REPORT_KEY_tmp.lower() in map(str.lower, key_value_list):
                data['FILENAME'].append(os.path.basename(raw_data_file))
                data['NLP_MODE'].append(raw_data_files_dict[os.path.basename(raw_data_file)]['NLP_MODE'])
                for i in range(len(keys)):
                    if keys[i] in dt_labels:
                        data[keys[i]].append(self._read_datetime(book, row[i].value))
                    else:
                        data[keys[i]].append(row[i].value)
        if 'RAW_TEXT' not in data.keys():
            data['RAW_TEXT'] = data[keys[-1]]
        else:
            data['RAW_TEXT'].extend(data[keys[-1]])
        del data[keys[-1]]
        return data
    
    '''
    #
    def _read_data_file_nokey(self, raw_data_files_dict, raw_data_file, dt_labels):
        data = {}
        book = read_xlsx_file(raw_data_file)
        sheet = book.sheet_by_index(0)
        keys = sheet.row(0)
        for i in range(len(keys)):
            keys[i] = str(keys[i].value)
        if 'FILENAME' not in data.keys():
            data['FILENAME'] = []
        if 'NLP_MODE' not in data.keys():
            data['NLP_MODE'] = []
        for key in keys:
            if key not in data.keys():
                data[key] = []
        for row_idx in range(1, sheet.nrows):
            row = sheet.row(row_idx)
            data['FILENAME'].append(os.path.basename(raw_data_file))
            data['NLP_MODE'].append(raw_data_files_dict[os.path.basename(raw_data_file)]['NLP_MODE'])
            for i in range(len(keys)):
                if keys[i] in dt_labels:
                    data[keys[i]].append(self._read_datetime(book, row[i].value))
                else:
                    data[keys[i]].append(row[i].value)
        if 'RAW_TEXT' not in data.keys():
            data['RAW_TEXT'] = data[keys[-1]]
        else:
            data['RAW_TEXT'].extend(data[keys[-1]])
        del data[keys[-1]]
        return data
    '''
    
    #
    def column(self, column_label):
        column_labels = self.training_data[0]
        idx = column_labels.index(column_label)
        column_values = []
        for i in range(1, len(self.training_data)):
            column_values.append(self.training_data[i][idx])
        return column_values
    
    #
    def column_labels(self):
        return self.validation_data[0]
    
    #
    def get_validation_csn_list(self):
        #static_data = self.static_data_manager.get_static_data()
        static_data = self.static_data
        if 'document_list' in static_data.keys():
            csn_list = static_data['document_list']
        else:
            csn_list = None
        validation_csn_list =  []
        for row in self.validation_data:
            if csn_list is None or row[2] in csn_list:
                validation_csn_list.append(row[2])
        validation_csn_list = list(set(validation_csn_list))
        return validation_csn_list
    
    #
    def get_validation_data(self):
        return self.validation_data
    
    #
    def length(self):
        return len(self.validation_data)
    
    #
    def read_training_data(self):
        book = read_xlsx_file(self.raw_data_file)
        sheet = book.sheet_by_index(0)
        ncols = sheet.ncols
        nrows = sheet.nrows
        training_data = []
        for row_idx in range(nrows):
            training_data_tmp = []
            for col_idx in range(ncols):
                cell_value = sheet.cell_value(row_idx, col_idx)
                try:
                    cell_value = str(int(cell_value))
                except:
                    pass
                training_data_tmp.append(cell_value)
            training_data.append(training_data_tmp)
        self.training_data = training_data
    
    #
    def read_validation_data(self):
        book = read_xlsx_file(self.raw_data_file)
        sheet = book.sheet_by_index(0)
        ncols = sheet.ncols
        nrows = sheet.nrows
        validation_data = []
        for row_idx in range(nrows):
            validation_data_tmp = []
            for col_idx in range(ncols):
                cell_value = sheet.cell_value(row_idx, col_idx)
                try:
                    cell_value = str(int(cell_value))
                except:
                    pass
                validation_data_tmp.append(cell_value)
            validation_data.append(validation_data_tmp)
        self.validation_data = validation_data
    
    #
    def row(self, idx):
        return self.validation_data[idx]
    
    #
    def trim_validation_data(self):
        validation_data_in = self.validation_data
        #static_data = self.static_data_manager.get_static_data()
        static_data = self.static_data
        if 'patient_list' in static_data.keys():
            patient_list = static_data['patient_list']
            for i in range(len(patient_list)):
                patient_list[i] = int(patient_list[i])
        else:
            patient_list = None
        validation_data_out =  []
        validation_data_out.append(validation_data_in[0])
        validation_data_in = validation_data_in[1:]
        for item in validation_data_in:
            if patient_list is None or int(item[1]) in patient_list:
                validation_data_out.append(item)
        self.validation_data = validation_data_out