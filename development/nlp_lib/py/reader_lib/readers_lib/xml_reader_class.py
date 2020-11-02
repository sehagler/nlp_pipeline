# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 12:56:34 2020

@author: haglers
"""

#
import codecs
import os
import re
import xml.etree.ElementTree as ET

#
from nlp_lib.py.manager_lib.server_manager_class import Server_manager
from nlp_lib.py.tool_lib.processing_tools_lib.text_processing_tools import make_ascii

#
class Xml_reader(object):
    
    #
    def __init__(self, project_data, password):
        self.project_data = project_data
        self.server_manager = Server_manager(project_data, password)
    
    #
    def _read_file_nokey(self, raw_data_files_dict, raw_data_file):
        filename, file_extension = os.path.splitext(raw_data_file)
        tmp_file = filename + '.tmp'
        dt_labels = self.project_data['datetime_keys']
        text_identifiers = self.project_data['text_identifiers']
        with open(raw_data_file, 'rb') as f:
            xml_txt = f.read().decode('utf-8', 'replace')
        xml_txt = re.sub('&#8226;', '*', xml_txt)
        xml_txt = re.sub('&#[0-9]+;', '', xml_txt)
        with open(tmp_file, 'w') as f:
            f.write(xml_txt)
        keys = []
        parser = ET.iterparse(tmp_file)
        for event, elem in parser:
            if elem.tag not in [ 'DATA_RECORD', 'RESULTS', 'ROW', 'ROWSET' ] and event == 'end':
                if elem.tag == 'COLUMN':
                    keys.append(elem.attrib['NAME'])
                else:
                    keys.append(elem.tag)
            elem.clear()
        keys = list(set(keys))
        data = {}
        if 'FILENAME' not in data.keys():
            data['FILENAME'] = []
        if 'NLP_MODE' not in data.keys():
            data['NLP_MODE'] = []
        if 'NLP_PROCESS' not in data.keys():
            data['NLP_PROCESS'] = []
        if 'SOURCE_SYSTEM' not in data.keys():
            data['SOURCE_SYSTEM'] = []
        for key in keys:
            if key not in data.keys():
                data[key] = []
        parser = ET.iterparse(tmp_file)
        keys_appended = []
        for (event, elem) in parser:
            if elem.tag not in [ 'DATA_RECORD', 'RESULTS', 'ROW', 'ROWSET' ] and event == 'end':
                if elem.tag == 'COLUMN':
                    keys_appended.append(elem.attrib['NAME'])
                    data[elem.attrib['NAME']].append(elem.text)
                else:
                    keys_appended.append(elem.tag)
                    data[elem.tag].append(elem.text)
            if elem.tag in [ 'DATA_RECORD', 'ROW' ] and event == 'end':
                keys_not_appended = list(set(keys) - set(keys_appended))
                for key in keys_not_appended:
                    data[key].append(None)
                data['FILENAME'].append(os.path.basename(raw_data_file))
                data['NLP_MODE'].append(raw_data_files_dict[os.path.basename(raw_data_file)]['NLP_MODE'])
                data['NLP_PROCESS'].append(raw_data_files_dict[os.path.basename(raw_data_file)]['NLP_PROCESS'])
                data['SOURCE_SYSTEM'].append(raw_data_files_dict[os.path.basename(raw_data_file)]['SOURCE_SYSTEM'])
                keys_appended = []
        for text_identifier in text_identifiers:
            if text_identifier in data.keys():
                if 'RAW_TEXT' not in data.keys():
                    data['RAW_TEXT'] = data[text_identifier]
                else:
                    data['RAW_TEXT'].extend(data[text_identifier])
                del data[text_identifier]
        os.remove(tmp_file)
        return data
    
    #
    def _trim_data_by_csn(self, data):
        data_csn_list = data['SOURCE_SYSTEM_NOTE_CSN_ID']
        if 'document_list' in self.project_data.keys():
            document_list = self.project_data['document_list']
        else:
            document_list = list(set(data_csn_list))
        csn_list = []
        delete_idx_list = []
        for i in range(len(data_csn_list)):
            if (data_csn_list[i] in document_list and
                data_csn_list[i] not in csn_list):
                csn_list.append(data_csn_list[i])
            else:
                delete_idx_list.append(i)
        for key in data.keys():
            for i in sorted(delete_idx_list, reverse=True):
                del data[key][i]
        return data
    
    #
    def read_files(self, raw_data_files_dict, raw_data_file):
        data = self._read_file_nokey(raw_data_files_dict, raw_data_file)
        try:
            data = self._trim_data_by_csn(data)
        except:
            pass
        return data