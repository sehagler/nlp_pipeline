# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 14:57:36 2022

@author: haglers
"""

#
import codecs
import os
import re
import xml.etree.ElementTree as ET

#
from nlp_pipeline_lib.py.file_lib.base_class_lib.reader_base_class \
    import Reader_base
    
#
class Xml_manager(Reader_base):
    
    '''
    #
    def __init__(self, static_data_manager, filename):
        self.filename = filename
        self.static_data = static_data_manager.get_static_data()
    '''          
        
    #
    def _read_data_file(self, raw_data_files_dict, raw_data_file):
        filename = os.path.basename(raw_data_file)
        print('Reading: ' + filename)
        raw_data_encoding = \
            self.static_data['raw_data_files'][filename]['ENCODING']
        filename, file_extension = os.path.splitext(raw_data_file)
        tmp_file = filename + '.tmp'
        dt_labels = self.static_data['datetime_keys']
        text_identifiers = self.static_data['text_identifiers']
        with open(raw_data_file, encoding=raw_data_encoding, errors='ignore') as f:
            xml_txt = f.read()
        with codecs.open(tmp_file, 'w', self.static_data['tmp_data_encoding']) as f:
            f.write(xml_txt)
        keys = []
        parser = ET.iterparse(tmp_file)
        for (event, elem) in parser:
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
                if 'SOURCE_SYSTEM' in raw_data_files_dict[os.path.basename(raw_data_file)].keys():
                    print(raw_data_files_dict[os.path.basename(raw_data_file)].keys())
                    data['SOURCE_SYSTEM'].append(raw_data_files_dict[os.path.basename(raw_data_file)]['SOURCE_SYSTEM'])
                keys_appended = []
        if len(data['SOURCE_SYSTEM']) == 0:
            data['SOURCE_SYSTEM'] = data["SOURCE_SYSTEM_NAME"]
        #for text_identifier in text_identifiers:
        #    if text_identifier in data.keys():
        keys = list(data.keys())
        for key in keys:
            for text_identifier in text_identifiers:
                if text_identifier in key:
                    if 'RAW_TEXT' not in data.keys():
                        data['RAW_TEXT'] = data[key]
                    else:
                        data['RAW_TEXT'].extend(data[key])
                    del data[key]
        os.remove(tmp_file)
        return data