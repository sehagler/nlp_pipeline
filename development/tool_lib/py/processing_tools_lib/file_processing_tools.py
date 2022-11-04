# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 14:46:48 2020

@author: haglers
"""

#
from datetime import datetime
import json
import math
import os
import sys
import time
import traceback
import xlrd
import xml.etree.ElementTree as ET
from xmldiff import main
from zipfile import ZipFile

#
from tool_lib.py.processing_tools_lib.directory_processing_tools \
    import create_directory

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
        except Exception:
            traceback.print_exc()
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
        except Exception:
            traceback.print_exc()
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
def _write_file(filename, data, include_datetime_flg, verbose_flg):
    extension = os.path.splitext(filename)[1]
    if include_datetime_flg:
        now = datetime.now()
        datetime_str = now.strftime('_%Y%m%d_%H%M%S')
        filename = os.path.splitext(filename)[0]
        filename = filename + datetime_str + extension
    if verbose_flg:
        print('Writing file: ' + filename)
    max_retries = __max_retries()
    retry_sleep = __retry_sleep()
    _remove_file(filename)
    retry_ctr = 0
    wrote_file = False
    while (not wrote_file) and (retry_ctr < max_retries):
        try:
            if extension == '.json':
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=4)
            else:
                with open(filename, 'w+') as f:
                    f.write(data)
            wrote_file = True
        except Exception:
            traceback.print_exc()
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
                                except Exception:
                                    traceback.print_exc()
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

'''
#
def read_package_json_file(static_data):
    project_name = static_data['project_name']
    directory_manager = static_data['directory_manager']
    data_dir = directory_manager.pull_directory('processing_data_dir')
    nlp_data = \
        read_json_file(os.path.join(data_dir, project_name + '.json'))
    return nlp_data
'''

#
def read_txt_file(filename):
    with open(filename,'r') as f:
        data = f.read()
    return data

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
def write_file(filename, data, include_datetime_flg, multiple_files_flg):
    if multiple_files_flg:
        max_documents = 1000
        documents = data['DOCUMENTS']
        documents_chunks = []
        head, tail = os.path.split(filename)
        filename, extension = os.path.splitext(tail)
        head = os.path.join(head, filename)
        if not os.path.exists(head):
            os.makedirs(head)
        while len(documents) > max_documents:
            documents_chunks.append(documents[0:max_documents])
            del documents[0:max_documents]
        documents_chunks.append(documents)
        for chunk in documents_chunks:
            data = {}
            data['DOCUMENTS'] = chunk
            filename = os.path.join(head, tail)
            _write_file(filename, data, include_datetime_flg, True)
            time.sleep(1)
    else:
        _write_file(filename, data, include_datetime_flg, False)
    
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
        except Exception:
            traceback.print_exc()
            if retry_ctr == 0:
                print('failed to read ' + file0 + ' or ' + file1)
            time.sleep(retry_sleep)
            if retry_ctr < max_retries:
                print('retrying...')
            retry_ctr += 1
    if not read_file:
        sys.exit('file failed to read file after ' + str(max_retries) + ' retries')
    return diff_output