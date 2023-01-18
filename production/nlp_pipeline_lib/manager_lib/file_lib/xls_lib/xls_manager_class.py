# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 14:57:36 2022

@author: haglers
"""

#
import os
import re
import traceback
import xlrd

#
from base_lib.manager_base_class import Manager_base
from tools_lib.processing_tools_lib.file_processing_tools \
    import read_xlsx_file
    
#
def _get_document_values(raw_data):
    nlp_mode = raw_data['NLP_MODE'][0]
    document_values = list(set(raw_data[nlp_mode]))
    return document_values
    
#
def _read_datetime(book, value):
    if value != '':
        try:
            value = float(value)
            y, m, d, h, mi, s = \
                xlrd.xldate_as_tuple(value, book.datemode)
            datetime_str = str(m) + '/' + str(d) + '/' + str(y)
        except Exception:
            traceback.print_exc()
            datetime_str = ''
    else:
        datetime_str = ''
    return datetime_str
    
#
class Xls_manager(Manager_base):
    
    #
    def __init__(self, static_data_object, raw_data_file, password):
        Manager_base.__init__(self, static_data_object)
        self.static_data = self.static_data_object.get_static_data()
        self.raw_data_file = raw_data_file
    
    #
    def _get_document(self, raw_data, document_value):
        document_dict = {}
        for key in raw_data.keys():
            document_dict[key] = []
        for i in range(len(raw_data['FILENAME'])):
            nlp_mode = raw_data['NLP_MODE'][i]
            if nlp_mode == 'CASE_NUMBER':
                label0 = 'MRN'
                label1 = 'CASE_NUMBER'
            elif nlp_mode == 'RESULT_ID':
                label0 = 'RESULT_ID'
                label1 = 'RESULT_ID'
            elif nlp_mode == 'SOURCE_SYSTEM_RESULT_ID':
                label0 = 'SOURCE_SYSTEM_RESULT_ID'
                label1 = 'SOURCE_SYSTEM_RESULT_ID'
            if raw_data[label1][i] == document_value:
                if raw_data['REPORT_HEADER'][i] in document_dict['REPORT_HEADER']:
                    idx = document_dict['REPORT_HEADER'].index(raw_data['REPORT_HEADER'][i])
                    for key in document_dict.keys():
                        del document_dict[key][idx]
                for key in raw_data.keys():
                    document_dict[key].append(raw_data[key][i])
        raw_text = ''
        for i in range(len(document_dict['REPORT_HEADER'])):
            report_header_item = document_dict['REPORT_HEADER'][i]
            raw_text_item = document_dict['RAW_TEXT'][i]
            if len(raw_text_item) > len(report_header_item) and \
               raw_text_item[:len(report_header_item)+1] == report_header_item + ':':
                   raw_text_item = raw_text_item[len(report_header_item)+1:]
            raw_text += '\n\n' + report_header_item + '\n\n' + raw_text_item + '\n\n'
        raw_text = raw_text[2:-2]
        raw_text = re.sub('\n\n\n+', '\n\n', raw_text)
        del document_dict['REPORT_HEADER']
        document_dict['RAW_TEXT'] = [ raw_text ]
        for key in document_dict.keys():
            document_dict[key] = list(set(document_dict[key]))
        for key in document_dict.keys():
            if len(document_dict[key]) == 0:
                document_dict[key] = [ '' ]
        return document_dict
        
    #
    def _read_data_file(self, raw_data_files_dict, raw_data_file):
        dt_labels = self.static_data['datetime_keys']
        key_label = 'REPORT_HEADER'
        raw_data = {}
        book = read_xlsx_file(raw_data_file)
        sheet = book.sheet_by_index(0)
        keys = sheet.row(0)
        for i in range(len(keys)):
            keys[i] = str(keys[i].value)
        if 'FILENAME' not in raw_data.keys():
            raw_data['FILENAME'] = []
        if 'NLP_MODE' not in raw_data.keys():
            raw_data['NLP_MODE'] = []
        for key in keys:
            if key not in raw_data.keys():
                raw_data[key] = []
        for row_idx in range(1, sheet.nrows):
            row = sheet.row(row_idx)
            raw_data['FILENAME'].append(os.path.basename(raw_data_file))
            raw_data['NLP_MODE'].append(raw_data_files_dict[os.path.basename(raw_data_file)]['NLP_MODE'])
            for i in range(len(keys)):
                if keys[i] in dt_labels:
                    raw_data[keys[i]].append(_read_datetime(book, row[i].value))
                else:
                    raw_data[keys[i]].append(row[i].value)
        raw_data['RAW_TEXT'] = raw_data[keys[-1]]
        del raw_data[keys[-1]]
        data = {}
        for key in raw_data.keys():
            data[key] = []
        del data['REPORT_HEADER']
        document_values = _get_document_values(raw_data)
        for i in range(len(document_values)):
            document_dict = self._get_document(raw_data, document_values[i])
            for key in document_dict.keys():
                data[key].append(document_dict[key][0])
        return data
    
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
    def column_to_int(self, column_label):
        column_labels = self.validation_data[0]
        idx = column_labels.index(column_label)
        for i in range(1, len(self.validation_data)):
            try:
                self.validation_data[i][idx] = \
                    str(int(float(self.validation_data[i][idx])))
            except Exception:
                traceback.print_exc()
    
    #
    def get_validation_csn_list(self):
        #static_data = self.static_data_object.get_static_data()
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
    def read_file(self):
        raw_data_files_dict = self.static_data['raw_data_files']
        print('Reading file: ' + self.raw_data_file)
        data = self._read_data_file(raw_data_files_dict, self.raw_data_file)
        return data
    
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
                cell_value = str(cell_value)
                '''
                try:
                    cell_value = str(int(cell_value))
                except Exception:
                    traceback.print_exc()
                '''
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
                cell_value = str(cell_value)
                validation_data_tmp.append(cell_value)
            validation_data.append(validation_data_tmp)
        self.validation_data = validation_data
    
    #
    def row(self, idx):
        return self.validation_data[idx]
    
    #
    def trim_validation_data(self):
        validation_data_in = self.validation_data
        #static_data = self.static_data_object.get_static_data()
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