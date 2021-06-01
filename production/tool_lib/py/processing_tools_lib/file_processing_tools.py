# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 14:46:48 2020

@author: haglers
"""

#
import json
import math
import os
import sys
import time
import xlrd
import xml.etree.ElementTree as ET
from xmldiff import main
from zipfile import ZipFile

#
def __max_retries():
    return 12

#
def __retry_sleep():
    return 5

#
def _read_file(mode_flg, filename):
    max_retries = __max_retries()
    retry_sleep = __retry_sleep()
    read_file = False
    retry_ctr = 0
    while (not read_file) and (retry_ctr < max_retries):
        try:
            if mode_flg == 0:
                with open(filename,'r') as f:
                    data = json.load(f)
            elif mode_flg == 1:
                data = xlrd.open_workbook(filename)
            elif mode_flg == 2:
                data = ET.parse(filename)
            read_file = True
        except:
            if retry_ctr == 0:
                print('failed to read ' + filename)
            time.sleep(retry_sleep)
            if retry_ctr < max_retries:
                print('retrying...')
            retry_ctr += 1
    if not read_file:
        sys.exit('file failed to read file after ' + str(max_retries) + ' retries')
    return data

#
def _remove_file(filename):
    max_retries = __max_retries()
    retry_sleep = __retry_sleep()
    retry_ctr = 0
    removed_file = False
    while (not removed_file) and (retry_ctr < max_retries):
        try:
            if os.path.exists(filename):
                os.remove(filename)
                removed_file = True
            else:
                removed_file = True
        except:
            if retry_ctr == 0:
                print('failed to remove ' + filename)
            time.sleep(retry_sleep)
            if retry_ctr < max_retries:
                print('retrying...')
            retry_ctr += 1
    if not removed_file:
        sys.exit('file failed to remove file after ' + str(max_retries) + ' retries')

#
def _sort_files(files):
    file_array = []
    for file in files:
        file_array.append([os.path.splitext(os.path.basename(file))[0], file])
    is_numeric = True
    for item in file_array:
        if not item[0].isnumeric():
            is_numeric = False
    if is_numeric:
        for i in range(len(file_array)):
            file_array[i][0] = int(file_array[i][0])
    file_array = sorted(file_array, key=lambda x: x[0])
    return file_array, is_numeric

#
def _write_file(mode_flg, filename, data):
    max_retries = __max_retries()
    retry_sleep = __retry_sleep()
    _remove_file(filename)
    retry_ctr = 0
    wrote_file = False
    while (not wrote_file) and (retry_ctr < max_retries):
        try:
            if mode_flg == 0:
                with open(filename, 'w+') as f:
                    f.write(data)
            elif mode_flg == 1:
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=4)
            wrote_file = True
        except:
            if retry_ctr == 0:
                print('failed to write ' + filename)
            time.sleep(retry_sleep)
            if retry_ctr < max_retries:
                print('retrying...')
            retry_ctr += 1
    if not wrote_file:
        sys.exit('file failed to write file after ' + str(max_retries) + ' retries')
        
#
def _write_zip_file(filename, data_files, zip_path, max_files_per_zip, remove_file_flg):
    max_retries = __max_retries()
    retry_sleep = __retry_sleep()
    data_file_array, is_numeric = _sort_files(data_files)
    if len(data_file_array) > 0:
        data_files_list = []
        if is_numeric:
            num_zips = math.ceil(data_file_array[-1][0]/max_files_per_zip)
            for i in range(num_zips):
                data_files = [x[1] for x in data_file_array if (x[0] < (i+1)*max_files_per_zip)]
                data_file_array = [ x for x in data_file_array if (x[0] >= (i+1)*max_files_per_zip) ]
                data_files_list.append(data_files)
        else:
            data_files_list.append([x[1] for x in data_file_array])
        do_write = True
        wrote_file = False
        retry_ctr = 0
        filename_base = os.path.splitext(filename)[0]
        index_set = range(len(data_files_list))
        for i in index_set:
            data_files = data_files_list[i]
            if len(data_files) > 0:
                if len(data_files_list) > 1:
                    filename = filename_base + '_' + str(i) + '.zip'
                if remove_file_flg:
                    _remove_file(filename)
                with ZipFile(filename, 'a') as f:
                    for data_file in data_files:
                        if do_write:
                            wrote_file = False
                            while (not wrote_file) and (retry_ctr < max_retries):
                                try:
                                    zip_data_file = os.path.basename(data_file)
                                    if zip_path is not None:
                                        zip_data_file = os.path.join(zip_path, zip_data_file)
                                    f.write(data_file, zip_data_file)
                                    wrote_file = True
                                except:
                                    if retry_ctr == 0:
                                        print('failed to write ' + filename)
                                    time.sleep(retry_sleep)
                                    if retry_ctr < max_retries:
                                        print('retrying...')
                                    retry_ctr += 1
                        if not wrote_file:
                            do_write = False
        if not wrote_file:
            sys.exit('file failed to write file after ' + str(max_retries) + ' retries')

#
def read_json_file(filename):
    return _read_file(0, filename)

#
def read_nlp_data_from_package_json_file(static_data):
    
    json_structure_manager = static_data['json_structure_manager']
    document_wrapper_key = \
        json_structure_manager.pull_key('document_wrapper_key')
    documents_wrapper_key = \
        json_structure_manager.pull_key('documents_wrapper_key')
    metadata_key = \
        json_structure_manager.pull_key('metadata_key')
    nlp_data_key = \
        json_structure_manager.pull_key('nlp_data_key')
    nlp_datum_key = \
        json_structure_manager.pull_key('nlp_datum_key')
    nlp_metadata_key = \
        json_structure_manager.pull_key('nlp_metadata_key')
    nlp_query_key = \
        json_structure_manager.pull_key('nlp_query_key')
    nlp_section_key = \
        json_structure_manager.pull_key('nlp_section_key')
    nlp_specimen_key = \
        json_structure_manager.pull_key('nlp_specimen_key')
    nlp_tool_output_key = \
        json_structure_manager.pull_key('nlp_tool_output_key')
    
    nlp_data_tmp = read_package_json_file(static_data)
    patient_identifiers = static_data['patient_identifiers']
    if 'patient_list' in static_data.keys():
        patient_list = static_data['patient_list']
    else:
        patient_list = None
    nlp_data_tmp = nlp_data_tmp[documents_wrapper_key]
    nlp_data = {}
    for item in nlp_data_tmp:
        for patient_identifier in patient_identifiers:
            try:
                patient = \
                    item[document_wrapper_key][metadata_key][patient_identifier]
            except:
                pass
        document_idx = \
            item[document_wrapper_key][nlp_metadata_key]['NLP_DOCUMENT_IDX']
        if patient_list is None or patient in patient_list:
            nlp_data[document_idx] = {}
            for key in item[document_wrapper_key].keys():
                if key not in [nlp_data_key]:
                    nlp_data[document_idx][key] = \
                        item[document_wrapper_key][key]
                else:
                    data_in = item[document_wrapper_key][key]
            data = {}
            for item in data_in:
                nlp_query_key_tmp = \
                    item[nlp_datum_key][nlp_query_key]
                nlp_section_key_tmp = \
                    item[nlp_datum_key][nlp_section_key]
                try:
                    nlp_specimen_key_tmp = \
                        item[nlp_datum_key][nlp_specimen_key]
                except:
                    nlp_specimen_key_tmp = ''
                key_0 = str((nlp_section_key_tmp, nlp_specimen_key_tmp))
                for key_1 in item[nlp_datum_key].keys():
                    if key_0 not in data.keys():
                        data[key_0] = {}
                    if key_1 not in [nlp_query_key,
                                     nlp_section_key,
                                     nlp_specimen_key]:
                        if key_1 == 'DIAGNOSIS':
                            data[key_0]['DIAGNOSIS VALUE'] = \
                                item[nlp_datum_key][key_1]
                        else:
                            data[key_0][nlp_query_key_tmp + '_' + key_1] = \
                                item[nlp_datum_key][key_1]
            nlp_data[document_idx][nlp_data_key] = data
    return nlp_data

def read_package_json_file(static_data):
    project_name = static_data['project_name']
    directory_manager = static_data['directory_manager']
    data_dir = directory_manager.pull_directory('processing_data_dir')
    nlp_data = \
        read_json_file(os.path.join(data_dir, project_name + '.json'))
    return nlp_data

#
def read_xlsx_file(filename):
    return _read_file(1, filename)

#
def read_xml_file(filename):
    return _read_file(2, filename)

#
def remove_file(filename):
    _remove_file(filename)

#
def write_general_file(filename, data):
    _write_file(0, filename, data)
        
#
def write_json_file(filename, data):
    _write_file(1, filename, data)
    
#
def write_nlp_data_to_package_json_file(static_data, data_in):
    directory_manager = static_data['directory_manager']
    
    json_structure_manager = static_data['json_structure_manager']
    document_wrapper_key = \
        json_structure_manager.pull_key('document_wrapper_key')
    documents_wrapper_key = \
        json_structure_manager.pull_key('documents_wrapper_key')
    metadata_key = \
        json_structure_manager.pull_key('metadata_key')
    nlp_data_key = \
        json_structure_manager.pull_key('nlp_data_key')
    nlp_datetime_key = \
        json_structure_manager.pull_key('nlp_datetime_key')
    nlp_datum_key = \
        json_structure_manager.pull_key('nlp_datum_key')
    nlp_metadata_key = \
        json_structure_manager.pull_key('nlp_metadata_key')
    nlp_performance_key = \
        json_structure_manager.pull_key('nlp_performance_key')
    nlp_query_key = \
        json_structure_manager.pull_key('nlp_query_key')
    nlp_section_key = \
        json_structure_manager.pull_key('nlp_section_key')
    nlp_specimen_key = \
        json_structure_manager.pull_key('nlp_specimen_key')
    nlp_source_text_key = \
        json_structure_manager.pull_key('nlp_source_text_key')
    nlp_text_element_key = \
        json_structure_manager.pull_key('nlp_text_element_key')
    nlp_text_key = \
        json_structure_manager.pull_key('nlp_text_key')
    nlp_tool_output_key = \
        json_structure_manager.pull_key('nlp_tool_output_key')
    nlp_value_key = \
        json_structure_manager.pull_key('nlp_value_key')
        
    # to be moved to appropriate location
    multiple_specimens = \
        json_structure_manager.pull_key('multiple_specimens')
    multiple_values = \
        json_structure_manager.pull_key('multiple_values')
    #
    
    project_name = static_data['project_name']
    save_dir = directory_manager.pull_directory('processing_data_dir')
    
    documents = []
    for key_0 in data_in.keys():
        document_in = data_in[key_0]
        document = {}
        for key_1 in document_in.keys():
            if key_1 != 'RAW_TEXT':
                if key_1 not in [nlp_data_key, 'PREPROCESSED_TEXT']:
                    document[key_1] = document_in[key_1]
                elif key_1 == 'PREPROCESSED_TEXT':
                    document[nlp_source_text_key] = document_in[key_1]
                else:
                    data_tmp = document_in[key_1]
        data = []
        for key_1 in data_tmp:
            for key_2 in data_tmp[key_1]:
                data.append({ nlp_datum_key : data_tmp[key_1][key_2] })
        document[nlp_data_key] = data
        document_wrapper = {}
        document_wrapper[document_wrapper_key] = document
        documents.append(document_wrapper)
    documents_wrapper = {}
    documents_wrapper[documents_wrapper_key] = documents
    write_json_file(os.path.join(save_dir, project_name + '.json'),
                    documents_wrapper)
    
#
def write_zip_file(filename, data, zip_path, max_files_per_zip, remove_file_flg=True):
    _write_zip_file(filename, data, zip_path, max_files_per_zip, remove_file_flg)
    
#
def xml_diff(file0, file1):
    max_retries = __max_retries()
    retry_sleep = __retry_sleep()
    read_file = False
    retry_ctr = 0
    while (not read_file) and (retry_ctr < max_retries):
        try:
            diff_output = main.diff_files(file0, file1)
            read_file = True
        except:
            if retry_ctr == 0:
                print('failed to read ' + file0 + ' or ' + file1)
            time.sleep(retry_sleep)
            if retry_ctr < max_retries:
                print('retrying...')
            retry_ctr += 1
    if not read_file:
        sys.exit('file failed to read file after ' + str(max_retries) + ' retries')
    return diff_output