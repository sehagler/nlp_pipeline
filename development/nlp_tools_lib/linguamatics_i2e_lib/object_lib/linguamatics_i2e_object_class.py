from __future__ import unicode_literals, print_function

# -*- coding: utf-8 -*-
"""
Created on Fri Jan 04 10:50:12 2019

@author: haglers
"""

#
import ast
import csv
from fnmatch import fnmatch
import i2e.easl
from i2e.wsapi.common import (ClientConnectionSettings, I2EConnection,
                              I2EServer, I2EUser, RequestMaker,
                              RequestConfiguration)
from i2e.wsapi.serialize import Resource
from i2e.wsapi.task import MakeIndexConfiguration, QueryConfiguration, TaskLauncher
from io import open
import json
import logging
import os
import re
import requests
import shutil
import sys
import time
import traceback
import unicodecsv
import urllib
import urllib3
from xml.dom import minidom
import xml.etree.ElementTree as ET

#
from nlp_tools_lib.linguamatics_i2e_lib.object_lib.linguamatics_i2e_file_object_class \
    import Linguamatics_i2e_file_object
from nlp_tools_lib.linguamatics_i2e_lib.check_queries \
    import QuerySetFixer, get_logger, yaml_constructor
from tools_lib.processing_tools_lib.file_processing_tools \
    import remove_file, write_file, write_zip_file
from tools_lib.processing_tools_lib.text_processing_tools \
    import make_ascii, make_xml_compatible
    
#
urllib3.disable_warnings()
EASL_MIME_TYPE = "application/vnd.linguamatics.i2e.yaml"
logging.basicConfig(format='[%(asctime)s.%(msecs)03d]%(levelname)s:%(module)s:%(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d,%H:%M:%S',
                    stream=sys.stderr, level=logging.INFO)
logger = logging.getLogger()

#
class Linguamatics_i2e_object(object):
    
    #
    def __init__(self, server_manager, project_name, server, user, password):
        self.server_manager = server_manager
        self.server = server
        self.user = user
        self.linguamatics_i2e_file_object = \
            Linguamatics_i2e_file_object(project_name, user)
        self.license_pool = 'admin'
        self.query_bundle_path = \
            '/Repository/Saved Queries/__private__/' + user + '/'
        self.i2e_resources_dict = {}
        self.i2e_resources_dict['index_template'] = \
            "/api;type=index_template/" + project_name
        self.i2e_resources_dict['region_list'] = \
            "/api;type=region_list/" + \
            self.linguamatics_i2e_file_object.filename('regions')
        self.i2e_resources_dict['source_data'] = \
            "/api;type=source_data/" + project_name
        self.i2e_resources_dict['xml_and_html_config_file'] = \
            '/api;type=xml_and_html_config_file/' + \
            self.linguamatics_i2e_file_object.filename('xmlconf')
        self.i2e_server = I2EServer(server)
        self.i2e_user = I2EUser(user, password)
        self.connection_settings = ClientConnectionSettings.create()
        self.connection_settings.disable_ssl_verification()         
        self.conn = I2EConnection(self.i2e_server, self.i2e_user,
                                  connection_settings=self.connection_settings,
                                  license_pool=self.license_pool)
        
    #
    def _fix_queries(self, query_paths):
        log_level = logging.INFO
        with yaml_constructor():
            query_fixer = QuerySetFixer(query_paths,
                                        dry_run=False,
                                        logger=get_logger(log_level,
                                                          log_file_path=None))
            all_queries_ok = query_fixer.check_queries()
        return 0 if all_queries_ok else 1
        
    #
    def _folder_downloader(self, request_maker, folder_name, parent_folder,
                           download_folder):
        folder_content = request_maker.list_resource(folder_name)
        try:
            local_folder = os.path.normpath(download_folder + '/' + urllib.parse.unquote(folder_name.uri.replace(parent_folder,'')))
            os.mkdir(local_folder)
        except FileExistsError:
            selection = input('The folder ' + local_folder + ' already exists on your filesystem. Would you like to overwrite (Yes/No)? ')
            if selection.lower() == 'yes':
                pass
            else:
                sys.exit()
        for child in folder_content:
            if child.uri.endswith('.i2qy'):
                local_filename = os.path.normpath(download_folder + '/' + urllib.parse.unquote(child.uri.replace(parent_folder,'')))
                with request_maker.read_resource(child, "*/*") as response:
                    with open(local_filename, "wb") as output:
                        shutil.copyfileobj(response, output)
            else:
                self._folder_downloader(request_maker, child, parent_folder, download_folder)
                
    #
    def _generate_gold(self, inxml, text_spans):
        outfile = inxml.replace('.xml', '.csv')
        headers, rows = self._xml_to_gold(inxml, text_spans)
        with open(outfile, 'wb') as outf:
            logger.info('written {}'.format(outfile))
            writer = unicodecsv.writer(outf, delimiter=str(','), lineterminator='\n')
            writer.writerow(headers)
            for row in rows:
                writer.writerow(row)
    
    #
    def _generate_query_bundle_file_component(self, filename, queries_dir,
                                              dest_path_base, max_files_per_zip):
        for path, subdirs, files in os.walk(queries_dir):
            rel_path = os.path.relpath(path, queries_dir)
            dest_path = os.path.join (dest_path_base, rel_path)
            data_files = []
            for file in files:
                if fnmatch(file, '*.i2qy'):
                    data_files.append(os.path.join(path, file))
            write_zip_file(filename, data_files, dest_path, max_files_per_zip, remove_file_flg=False)
                   
    #
    def _generate_source_data_file(self, project_name, preprocessing_data_out_dir,
                                   source_data_dir, max_files_per_zip):
        source_data_filename = self.linguamatics_i2e_file_object.source_data_filename()
        data_files = [os.path.join(preprocessing_data_out_dir, file) \
                      for file in os.listdir(preprocessing_data_out_dir) \
                      if os.path.splitext(file)[1] == '.xml']
        write_zip_file(os.path.join(source_data_dir, source_data_filename),
                       data_files, None, max_files_per_zip)
        
    #
    def _get_col_ids(self, xml):
        column_names = dict()
        query_items = list()
        colset = xml.find('.//ColumnSet')
        for col in colset.findall('.//Column'):
            if col.attrib['type'] != 'queryItem':
                key = col.attrib['type']
            else:
                key = col.find('.//Name').text
                if key != 'docId' and '[PT]' not in key:
                    query_items.append(key)
            if key != 'docId' and '[PT]' not in key:
                column_names[key] = int(col.attrib['id'])
        return column_names, query_items
    
    #
    def _get_hit_highlights(self, text_in, targets):
        text = []
        for target in targets:
            target_in_hit = target[0]
            target_in_text = target[1]
            start = target_in_hit[0]
            stop = target_in_hit[1]
            text_tmp = tuple([ target_in_text, text_in[start:stop] ])
            text.append(text_tmp)
        return text
        
    #
    def _prepare_keywords_file(self, keywords_file, keywords_tmp_file):
        self.server_manager.open_ssh_client()
        self.server_manager.exec_sudo_command('cp ' + keywords_tmp_file + ' ' + self.linguamatics_i2e_file_object.server_file('keywords'))
        self.server_manager.exec_sudo_command('chmod 664 ' + self.linguamatics_i2e_file_object.server_file('keywords'))
        self.server_manager.exec_sudo_command('chown i2e:i2e ' + self.linguamatics_i2e_file_object.server_file('keywords'))
        self.server_manager.close_ssh_client()
        
    #
    def _prepare_keywords_file_ssh(self, keywords_file, keywords_tmp_file):
        self.server_manager.open_ssh_client()
        self.server_manager.push_file(keywords_file, keywords_tmp_file)
        self.server_manager.exec_sudo_command('mv ' + keywords_tmp_file + ' ' + self.linguamatics_i2e_file_object.server_file('keywords'))
        self.server_manager.exec_sudo_command('chmod 664 ' + self.linguamatics_i2e_file_object.server_file('keywords'))
        self.server_manager.exec_sudo_command('chown i2e:i2e ' + self.linguamatics_i2e_file_object.server_file('keywords'))
        self.server_manager.close_ssh_client()
    
    #
    def _put_keywords_file(self, root_dir_flg, keywords_file):
        keywords_tmp_file = '/tmp/keywords_default.txt'
        if root_dir_flg in ''.join([ 'X', 'Z' ]):
            self._prepare_keywords_file_ssh(keywords_file, keywords_tmp_file)
        elif root_dir_flg in ''.join([ 'dev_server', 'prod_server' ]):
            self._prepare_keywords_file(keywords_file, keywords_tmp_file)
            
    #
    def _read_file_metadata(self, preprocessing_data_out_dir):
        files = os.listdir(preprocessing_data_out_dir)
        xml = ET.parse(os.path.join(preprocessing_data_out_dir, files[0]))
        root_element = xml.getroot()
        self.metadata_keys = []
        for child in root_element:
            self.metadata_keys.append(child.tag)
            
    # 
    def _xml_to_gold(self, xml, text_spans=True, old_format=False):
        logger.info('parsing XML')
        parsed = ET.parse(xml)
        col_to_id, query_cols = self._get_col_ids(parsed)
        logger.info('query output columns: {}'.format(query_cols))
        logger.info('evaluate text spans: {}'.format(text_spans))
        id_to_col = {v: k for k, v in list(col_to_id.items())}
        first_cols = []
        headers = first_cols + query_cols + ['Coords']
        cell_to_colix = {k: headers.index(k) for k in query_cols}
        cell_to_colix['hit'] = headers.index('Coords')
        if text_spans:
            cell_to_colix['coords'] = headers.index('Coords')
        rows = list()
    
        for n, rowxml in enumerate(parsed.findall('.//Row')):
            extractions = []
            row = ['' for _ in headers]
            for cell_group in rowxml:
                if cell_group.tag == 'List':
                    cells = cell_group.findall('.//Cell')
                else:
                    cells = [cell_group]
                for cell in cells:
                    cellid = int(cell.attrib['columnId'])
                    if cellid in id_to_col.keys():
                        colname = id_to_col[cellid]
                    else:
                        colname = None
                    if colname is not None and colname in cell_to_colix:
                        htext = cell.find('.//Text').text
                        if colname != 'hit':
                            if htext is not None:
                                if row[cell_to_colix[colname]]:
                                    htext = ' {}'.format(htext)
                                    row[cell_to_colix[colname]] += htext
                                else:
                                    htext = htext.strip()
                                    row[cell_to_colix[colname]] = htext
                            else:
                                row[cell_to_colix[colname]] = ''
                            if colname not in [ 'DOCUMENT_ID', 'DATETIME', 'Section Title', 'Speciment Id'] and \
                               htext is not None:
                                extractions.append(htext)
                        else:
                            hit_spans = cell.findall('.//HitSpan')
                            if hit_spans:
                                hit_spans = set(
                                    [ET.tostring(h).strip() for h in hit_spans])
                                targets = list()
                                for hit_span in hit_spans:
                                    hit_span = ET.fromstring(hit_span)
                                    is_sent = hit_span.find('.//IsSentence')
                                    if is_sent is None:
                                        url = hit_span.find('.//URL').text
                                        target_id = re.search(r"#(.+)", url).group(1)
                                        start = int(target_id.split('-')[1])
                                        hit_len = int(hit_span.find('.//Length').text)
                                        stop = start + hit_len
                                        start_in_hit = int(
                                            hit_span.find('.//Start').text) - 1
                                        stop_in_hit = start_in_hit + hit_len
                                        #if (start_in_hit, stop_in_hit) not in targets_in_hit:
                                        targets_in_hit = (start_in_hit, stop_in_hit)
                                        #if (start, stop) not in targets_in_text:
                                        targets_in_text = (start, stop)
                                        targets.append(tuple([ targets_in_hit,
                                                               targets_in_text ]))
                                highlighted_spans = self._get_hit_highlights(htext,
                                                                             targets)
                                targets = []
                                for i in range(len(extractions)):
                                    extraction = extractions[i]
                                    highlighted_span_found_flg = False
                                    for highlighted_span in highlighted_spans:
                                        if not highlighted_span_found_flg and \
                                           highlighted_span[1] == extraction:
                                            targets.append(highlighted_span[0])
                                            highlighted_span_found_flg = True
                                    if not highlighted_span_found_flg:
                                        targets.append('')
                                targets = targets[1:-1]
                                if len(targets) == 0:
                                    for i in range(len(extractions)):
                                        extraction = extractions[i]
                                        prefix = htext.replace(extraction, '')
                                        highlighted_span_found_flg = False
                                        for highlighted_span in highlighted_spans:
                                            if not highlighted_span_found_flg and \
                                               extraction.startswith(highlighted_span[1]):
                                                x = highlighted_span[0][0] + len(prefix)
                                                targets.append(tuple([x, x + len(extraction)]))
                                                highlighted_span_found_flg = True
                                        if not highlighted_span_found_flg:
                                            targets.append('')
                                if text_spans:
                                    row[cell_to_colix['coords']] = targets
                            else:
                                if text_spans:
                                    row[cell_to_colix['coords']] = '[]'
            rows.append(row)
        return headers, rows

    #
    def create_resource(self, project_name, resource_type, resource_file): 
        print('Creating I2E resource ' + resource_file)
        resource = "/api;type=" + resource_type + "/%s"
        if project_name is None:
            source_data_path = Resource(resource %
                                        os.path.basename(resource_file))
        else:
            source_data_path = Resource(resource %
                                        project_name + '/' + \
                                        os.path.basename(resource_file))
        request_maker = RequestMaker(self.conn)
        with open(resource_file, 'rb') as source_data:
            request_maker.create_resource(source_data_path,
                                          "text/plain", source_data)
            
    #
    def create_source_data_file(self, outdir, document_idx, document_dict):
        ctr = document_idx
        metadata = document_dict[document_idx]['xml_metadata']
        raw_text = document_dict[document_idx]['processed_raw_text']
        rpt_text = document_dict[document_idx]['processed_report_text']
        raw_text = make_ascii(raw_text)
        raw_text = make_xml_compatible(raw_text)
        keys = metadata.keys()
        for key in keys:
            key_value = metadata[key]
            if key_value is not None:
                key_value = key_value.replace('\'','\\\'')
            metadata[key] = key_value
        report = ET.Element('REPORT')
        for key in keys:
            subelement = ET.SubElement(report, key)
            subelement.text = metadata[key]
        subelement = ET.SubElement(report, 'RAW_TEXT')
        subelement.text = raw_text
        subelement = ET.SubElement(report, 'rpt_text')
        subelement.text = rpt_text
        xml_str = minidom.parseString(ET.tostring(report)).toprettyxml(indent = "   ")
        filename = str(ctr) + '.xml'
        write_file(os.path.join(outdir, filename), xml_str, False, False)
        ret_val = True
        return ret_val

    #
    def delete_resource(self, resource):
        print('Deleting I2E resource ' + resource)
        resource = Resource(resource)
        request_maker = RequestMaker(self.conn)
        request_maker.delete_resource(resource)
        
    #
    def fix_queries(self):
        self._fix_queries(self.linguamatics_i2e_common_queries_dir)
        self._fix_queries(self.linguamatics_i2e_general_queries_dir)
        self._fix_queries(self.linguamatics_i2e_project_queries_dir)

    #
    def folder_downloader(self, query_folder, local_destination):
        folder = Resource(query_folder)
        parent = folder.uri.replace(os.path.basename(os.path.normpath(folder.uri)),'')
        download_path = os.path.normpath(local_destination) if local_destination is not None else os.path.normpath(os.getcwd())
        request_maker = RequestMaker(self.conn)
        self._folder_downloader(request_maker, folder, parent, download_path)
        
    #
    def generate_csv_files(self, data_dir):
        for filename in os.listdir(data_dir):
            filename_base, extension = os.path.splitext(filename)
            if extension in [ '.xml' ]:
                print('Converting ' + filename)
                filename = data_dir + '/' + filename
                self._generate_gold(filename, True)
                
    #
    def generate_data_dict(self, data_dir, data_file):
        data_file = os.path.join(data_dir, data_file)
        data_dict = {}
        with open(data_file,'r') as f:
            csv_reader = csv.reader(f, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count > 0:
                    if row[0] not in data_dict.keys():
                        data_dict[row[0]] = []
                    row[-1] = ast.literal_eval(row[-1])
                    data_dict[row[0]].append(row[1:])
                line_count += 1
        return data_dict
    
    #
    def generate_query_bundle_file(self, project_name,
                                   max_files_per_zip):
        dest_path_base = self.query_bundle_path
        filename = os.path.join(self.processing_data_dir,
                                self.linguamatics_i2e_file_object.query_bundle_filename())
        remove_file(filename)
        common_dest_path_base = dest_path_base + 'Common'
        self._generate_query_bundle_file_component(filename,
                                                   self.linguamatics_i2e_common_queries_dir,
                                                   common_dest_path_base,
                                                   max_files_per_zip)
        general_dest_path_base = dest_path_base + 'General'
        self._generate_query_bundle_file_component(filename,
                                                   self.linguamatics_i2e_general_queries_dir,
                                                   general_dest_path_base,
                                                   max_files_per_zip)
        project_dest_path_base = dest_path_base + project_name
        self._generate_query_bundle_file_component(filename,
                                                   self.linguamatics_i2e_project_queries_dir,
                                                   project_dest_path_base,
                                                   max_files_per_zip)
    
    #
    def generate_regions_file(self):
        self._read_file_metadata(self.linguamatics_i2e_preprocessing_data_out_dir)
        text = []
        text.append('hc.metadata\t\"Record Metadata\"\t-\tnonleaf\n')
        for key in self.metadata_keys:
            text.append('\thc.' + key + '\t\"' + key + '\"\thc.metadata\tleaf\n')
        text.append('\n')
        text.append('hc.pathology_reports\t\"Healthcare Pathology Reports\"\t-\tnonleaf\n')
        text.append('\n')
        text.append('hc.section\t\"Section\"\thc.pathology_reports\tnonleaf\n')
        text.append('\thc.titled_section\t\"Titled Section\"\thc.section\tleaf\n')
        text.append('\thc.untitled_section\t\"Untitled Section\"\thc.section\tleaf\n')
        text.append('hc.subsection\t\"Subsection\"\thc.pathology_reports\tnonleaf\n')
        text.append('\thc.section_title\t\"Section Title\"\thc.subsection\tleaf\n')
        text.append('\thc.section_body\t\"Section Body\"\thc.subsection\tleaf\n')
        text.append('hc.shared_field\t\"Shared Field\"\thc.pathology_reports\tnonleaf\n')
        text.append('\thc.specimen\t\"Specimen Description\"\thc.shared_field\tleaf\n')
        text.append('\n')
        text.append('hc.shadow\t\"Healthcare Pathology Reports Shadow Regions\"\t-\tnonleaf,shadow\n')
        text.append('\thc.specimen_id\t\"Specimen Id\"\thc.shadow\tleaf,shadow\n')
        text.append('\n')
        text.append('linguamatics.metadata\t\"File Metadata\"\t-\tnonleaf,shadow\n')
        text.append('\tlinguamatics.filename\t"File Name"\tlinguamatics.metadata\tleaf,shadow\n')
        text.append('\tlinguamatics.indextype\t"Index Type"\tlinguamatics.metadata\tleaf,shadow\n')
        text.append('\tlinguamatics.lastmodified\t"Last Modified"\tlinguamatics.metadata\tleaf,shadow\n')
        text.append('\tlinguamatics.relativepath\t"Relative Path"\tlinguamatics.metadata\tleaf,shadow\n')
        text.append('\tlinguamatics.sourcetype\t"Source Type"\tlinguamatics.metadata\tleaf,shadow\n')
        text = ''.join(text)
        filename = os.path.join(self.processing_data_dir,
                                self.linguamatics_i2e_file_object.regions_filename())
        write_file(filename, text, False, False)
        
    #
    def generate_xml_configuation_file(self):
        self._read_file_metadata(self.linguamatics_i2e_preprocessing_data_out_dir)
        text = []
        text.append('split Report\n')
        text.append('\n')
        for key in self.metadata_keys:
            text.append('region\t' + key + '\t' + 'hc.' + key + '\t2\n')
        text.append('\n')
        text.append('region\tsection\thc.titled_section\t2\n')
        text.append('region\tuntitled_section\thc.untitled_section\t2\n')
        text.append('region\tsection_title\thc.section_title\t2\n')
        text.append('region\tsection_body\thc.section_body\t2\n')
        text.append('region\tspecimen\thc.specimen\t2\n')
        text.append('region\tspecimen/@id\thc.specimen_id\t2\n')
        text.append('\n')
        text.append('alias\ti2e_metadata_filename = file.name\n')
        text.append('token\ti2e_metadata_filename\t2\n')
        text.append('regionname\ti2e_metadata_filename\tlinguamatics.filename\t2\n')
        text.append('matchclass\ti2e_metadata_filename\texclude\t*\n')
        text.append('\n')
        text.append('alias\ti2e_metadata_relativepath = file.relativePath\n')
        text.append('token\ti2e_metadata_relativepath\t2\n')
        text.append('region\ti2e_metadata_relativepath\tlinguamatics.relativepath\t2\n')
        text.append('matchclass\ti2e_metadata_relativepath\texclude\t*\n')
        text.append('\n')
        text.append('alias\ti2e_metadata_indextype = \"XML\"\n')
        text.append('region\ti2e_metadata_indextype\tlinguamatics.indextype\t2\n')
        text.append('matchclass\ti2e_metadata_indextype\texclude\t*\n')
        text.append('\n')
        text.append('alias\ti2e_metadata_lastmodified = file.lastWriteTime\n')
        text.append('region\ti2e_metadata_lastmodified\tlinguamatics.lastmodified\t2\n')
        text.append('matchclass\ti2e_metadata_lastmodified\tinclude\tSEMANTIC_DATE_COMMON_FORMATS\texclude\t*\n')
        text.append('\n')
        text.append('createontology\tFirst\t1\t\"lineboundaries.Words per Line\"\t0\n')
        text.append('createontology\tLast\t1\t\"lineboundaries.Words per Line\"\t0\n')
        text.append('\n')
        text.append('regions\n')
        text.append('include\t*\t0\n')
        text = ''.join(text)
        filename = os.path.join(self.processing_data_dir,
                                self.linguamatics_i2e_file_object.xmlconf_filename())
        write_file(filename, text, False, False)
        
    #
    def get_i2e_version(self, password):
        auth_values = (self.user, password)
        headers = {'X-License-Pool': self.license_pool}
        with requests.get(self.server + '/api', auth=auth_values, headers=headers, verify=False) as r:
            try:
                response = r.headers['X-Version']
            except Exception:
                traceback.print_exc()
                response = 'FAILED_TO_CONNECT'
        return response
    
    #
    def insert_field(self, sub_query_file, alternative_file):
        sub_query_uri = '/api;type=saved_query/__private__/' + sub_query_file
        sub_query = Resource(sub_query_uri)
        filename = alternative_file
        if filename:
            with open(filename) as f:
                alternative_source = f.read()
        alternative_list = ast.literal_eval(alternative_source)
        query = i2e.easl.query.Query(5.5)
        document = query.root  
        alternative = document.add_alternative()
        for item in alternative_list:
            if isinstance(item, str):
                word_item = document.add_word(item)
                word_item.match_type = "Raw regexp"
                query.move_item(word_item, new_parent=alternative)
            elif isinstance(item, list):
                phrase_item = document.add_phrase()
                phrase_item.multi_sentence = True
                for sub_item in item:
                    word_item = document.add_word(sub_item)
                    word_item.match_type = "Raw regexp"
                    query.move_item(word_item, new_parent=phrase_item)
                query.move_item(phrase_item, new_parent=alternative)
        query_source = query.to_string()
        request_maker = RequestMaker(self.conn)
        task_launcher = TaskLauncher(self.conn)
        request_config = RequestConfiguration()
        result = request_maker.update_resource(sub_query,
                                               EASL_MIME_TYPE,
                                               query_source, request_config)
    
    #
    def login(self):
        self.conn.login()
        
    #
    def logout(self):
        self.conn.logout()

    #
    def make_index_runner(self, project_name, project_subdir, user):
        request_maker = RequestMaker(self.conn)
        index_template = self.i2e_resources_dict['index_template']
        print('Making I2E index ' + project_name)
        template = Resource(index_template)
        task_launcher = TaskLauncher(self.conn)
        index_config = task_launcher.create_index_configuration()
        #region_list_path = Resource("/api;type=region_list/%s" %
        #                            project_name)
        #index_config.set_region_list(region_list_path)
        source_data_path = Resource("/api;type=source_data/%s" %
                                    project_name)
        index_config.set_source_data(source_data_path)
        #xml_or_html_config_path = Resource("/api;type=xml_and_html_config/%s" %
        #                                   project_name)
        #index_config.set_xml_or_html_config(xml_or_html_config_path)
        monitor = task_launcher.make_index(template, index_config)
        while monitor.is_running():
            time.sleep(5)
        print("Task status is %s" % monitor.get_status())
        '''
        index_resource = monitor.get_created_indexes()
        print(len(index_resource))
        index_name = str(index_resource[0])
        index_name = re.sub('/api;type=index/','', index_name)
        index_name = re.sub('/Part_*', '', index_name)
        index_name = index_name[:-1]
        if project_subdir == 'test':
            publication_uri = '/api;type=published_index/__private__%2f' + user + '/' + index_name
        elif project_subdir == 'production':
            publication_uri = '/api;type=published_index/All/' + index_name
        else:
            print('Bad project_subdir')
        published_resource = Resource(publication_uri)
        published_response = request_maker.copy_resource(index_resource[0],
                                                         published_resource)
        print (published_response)
        '''
        
    #
    def push_linguamatics_i2e_common_queries_directory(self, directory):
        self.linguamatics_i2e_common_queries_dir = directory
        
    #
    def push_linguamatics_i2e_general_queries_directory(self, directory):
        self.linguamatics_i2e_general_queries_dir = directory
        
    #
    def push_linguamatics_i2e_project_queries_directory(self, directory):
        self.linguamatics_i2e_project_queries_dir = directory
        
    #
    def push_linguamatics_i2e_preprocessing_data_out_directory(self, directory):
        self.linguamatics_i2e_preprocessing_data_out_dir = directory
        
    #
    def push_processing_data_directory(self, directory):
        self.processing_data_dir = directory
        
    #
    def push_queries(self):
        try:
            bundle = os.path.join(self.processing_data_dir,
                                  self.linguamatics_i2e_file_object.query_bundle_filename())
            self.upload_bundle(bundle)
        except Exception:
            traceback.print_exc()
        
    #
    def push_resources(self, project_name, keywords_file, max_files_per_zip,
                       root_dir_flg):
        self._generate_source_data_file(project_name, 
                                        self.linguamatics_i2e_preprocessing_data_out_dir,
                                        self.source_data_dir, max_files_per_zip)
        self._put_keywords_file(root_dir_flg, keywords_file)
        for resource in [ 'regions', 'source_data', 'xmlconf' ]:
            filename = os.path.join(self.processing_data_dir,
                                    self.linguamatics_i2e_file_object.filename(resource))
            if resource == 'regions':
                resource_type = 'region_list'
            elif resource == 'source_data':
                resource_type = 'source_data'
            elif resource == 'xmlconf':
                resource_type = 'xml_and_html_config_file'
            try:
                self.delete_resource(self.i2e_resources_dict[resource_type])
            except Exception:
                traceback.print_exc()
            if resource_type == 'source_data':
                for source_data_file in sorted(os.listdir(self.source_data_dir)):
                    try:
                        self.create_resource(project_name, resource_type,
                                             os.path.join(self.source_data_dir,
                                                          source_data_file))
                    except Exception:
                        traceback.print_exc()
            else:
                try:
                    self.create_resource(None, resource_type, filename)
                except Exception:
                    traceback.print_exc()
                    
    #
    def push_source_data_directory(self, directory):
        self.source_data_dir = directory
            
    '''
    #
    def set_index_configuration(self, project_name):
        index_config = MakeIndexConfiguration()
        index_config.set_publishing_path("api;type=publishing_path/__private__/" + 'mccoyda')
        index_config.set_region_list("/api;type=region_list/" + project_name)
        index_config.set_source_data("/api;type=source_data/" + project_name)
        index_config.set_xml_or_html_config("/api;type=xml_or_html_config/" + project_name)
    '''        
   
    #
    def upload_bundle(self, bundle):
        
        request_maker = RequestMaker(self.conn)
            
        head, tail = os.path.split(bundle)
    
        # Read the file
        bundlecontent = open(bundle, 'rb').read()
    
        # Bundle Upload endpoints
        zbundle_upload_uri = Resource('/api;type=zipped_repository_bundle')
        bundle_upload_uri = Resource('/api;type=repository_bundle')
        bundle_task_uri = Resource('/api;type=bundle_installation_task')
        ## Step 1: upload the upload bundle (zipped) to the I2E server
        request_config = RequestConfiguration()
        request_config.add_parameter(RequestConfiguration.QueryParameter.BASE, tail)
        result = request_maker.create_resource(zbundle_upload_uri, "application/octet-stream",
                                               bundlecontent, request_config)
        zip_location = result.resource.uri
    
        ## Step 2: unzip the zipped bundle by moving it to type=repository_bundle
        request_config.add_parameter(RequestConfiguration.QueryParameter.COPYFROM, zip_location)
        unzip = request_maker.create_resource(bundle_upload_uri, "application/octet-stream", '', request_config)
        unzip_location = unzip.resource.uri
    
        ## Step 3: Submit the bundle install task
        # Create a barebones "template" containing a references to my repository bundle
        template = {"bundleHandle": unzip_location, "forceUpdate": True, "host": 'localhost', "user": self.user}
        request_maker2 = RequestMaker(self.conn)
        request_config2 = RequestConfiguration()
        request_config2.add_parameter(RequestConfiguration.QueryParameter.BASE, tail)
        install = request_maker2.create_resource(bundle_task_uri, "application/json", json.dumps(template), request_config2)
        install_location = install.resource.uri
        # track the status of the bundle install task
        request_config2 = RequestConfiguration()
        request_config2.set_attribute(RequestConfiguration.AttributeSpecifier.STATUS)
        install_status_task = request_maker2.read_resource(install_location, "application/json", request_config2)
        # Note: read_resource() returns a file object, so we need to read() it to get its content
        install_status = json.loads(install_status_task.read())['status']
        
        #
        print('Uploading I2E bundle ' + bundle)
        while install_status == 'running':
            time.sleep(15)
            install_status_task = request_maker2.read_resource(install_location, "application/json", request_config2)
            install_status = json.loads(install_status_task.read())['status']
        if install_status.startswith('succeeded'):
            print('Bundle upload succeeded')
        else:
            print('Bundle upload failed')