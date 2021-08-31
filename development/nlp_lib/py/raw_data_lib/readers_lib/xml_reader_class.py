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
from nlp_lib.py.raw_data_lib.base_class_lib.reader_base_class import Reader_base

#
class Xml_reader(Reader_base):
    
    #
    def _read_data_file(self, raw_data_files_dict, raw_data_file):
        filename, file_extension = os.path.splitext(raw_data_file)
        tmp_file = filename + '.tmp'
        dt_labels = self.static_data['datetime_keys']
        text_identifiers = self.static_data['text_identifiers']
        with open(raw_data_file, 'rb') as f:
            xml_txt = f.read().decode(self.static_data['raw_data_encoding'], 'ignore')
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