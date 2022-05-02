# -*- coding: utf-8 -*-
"""
Created on Tue Mar 2 10:02:08 2021

@author: haglers
"""
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 04 10:50:12 2019

@author: haglers
"""

#
import ast
import csv
from i2e.wsapi.common import (ClientConnectionSettings, I2EConnection,
                              I2EServer, I2EUser, RequestMaker,
                              RequestConfiguration)
from i2e.wsapi.serialize import Resource
from i2e.wsapi.task import MakeIndexConfiguration, TaskLauncher
import json
import logging
import os
import requests
import shutil
import sys
import time
import urllib
from xml.dom import minidom
import xml.etree.ElementTree as ET

#
from nlp_tools_lib.linguamatics_i2e_lib.py.check_queries \
    import QuerySetFixer, get_logger, yaml_constructor
from nlp_tools_lib.linguamatics_i2e_lib.py.generate_gold \
    import generate_gold
from nlp_tools_lib.linguamatics_i2e_lib.py.linguamatics_i2e_file_manager_class \
    import Linguamatics_i2e_file_manager
from nlp_tools_lib.linguamatics_i2e_lib.py.linguamatics_i2e_writer_class \
    import Linguamatics_i2e_writer
from tool_lib.py.processing_tools_lib.file_processing_tools \
    import write_file
from tool_lib.py.processing_tools_lib.text_processing_tools \
    import make_ascii, make_xml_compatible

#
class Linguamatics_i2e_manager(object):
    
    #
    def __init__(self, static_data_manager, server_manager, password):
        self.static_data_manager = static_data_manager
        self.static_data = self.static_data_manager.get_static_data()
        self.project_name = self.static_data['project_name']
        self.server = self.static_data['acc_server'][2]
        self.user = self.static_data['user']
        self.linguamatics_i2e_file_manager = \
            Linguamatics_i2e_file_manager(self.project_name, self.user)
        self.linguamatics_i2e_writer = \
            Linguamatics_i2e_writer(self.linguamatics_i2e_file_manager,
                                    server_manager)
        self.i2e_server = I2EServer(self.server)
        self.i2e_user = I2EUser(self.user, password)
        self.connection_settings = ClientConnectionSettings.create()
        self.license_pool = 'admin'
        self.conn = I2EConnection(self.i2e_server, self.i2e_user,
                                  connection_settings=self.connection_settings,
                                  license_pool=self.license_pool)
        
    #
    def _build_data_dictionary(self):
        for key in self.data_csv.keys():
            document_dict = {}
            document_dict['DOCUMENT_ID'] = key
            document_frame = []
            document_frame = self._build_document_frame(self.data_csv[key])
            document_dict['DOCUMENT_FRAME'] = document_frame
            self.data_dict_list.append(document_dict)
            
    #
    def _build_document_frame(self, data_list):
        document_frame = []
        for item in data_list:
            entry = []
            entry.append(tuple([item[1], item[2]]))
            entry.append(item[0])
            entry.append(item[3])
            document_frame.append(entry)
            num_elements = len(item) - 4
            for i in range(num_elements):
                entry.append(item[4+i])
        return(document_frame)
        
    #
    def _fix_queries(self, query_paths):
        '''
        args = None
        parser = get_parser()
        parsed_args = parser.parse_args(args=args)
        '''
        log_level = logging.INFO
        '''
        if parsed_args.debug:
            log_level = logging.DEBUG
        elif parsed_args.errors_only:
            log_level = logging.WARNING
        '''
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
    def _put_keywords_file(self, keywords_file, linguamatics_i2e_writer):
        keywords_tmp_file = '/tmp/keywords_default.txt'
        if self.static_data['root_dir_flg'] in ''.join([ 'X', 'Z' ]):
            linguamatics_i2e_writer.prepare_keywords_file_ssh(keywords_file, keywords_tmp_file)
        elif self.static_data['root_dir_flg'] in ''.join([ 'dev_server', 'prod_server' ]):
            linguamatics_i2e_writer.prepare_keywords_file(keywords_file, keywords_tmp_file)

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
    def create_source_data_file(self, ctr, metadata, raw_text, rpt_text):
        static_data = self.static_data_manager.get_static_data()
        directory_manager = static_data['directory_manager']
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
        outdir = directory_manager.pull_directory('linguamatics_i2e_preprocessing_data_out')
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
        directory_manager = self.static_data['directory_manager']
        general_queries_dir = \
            directory_manager.pull_directory('linguamatics_i2e_general_queries_dir')
        project_queries_dir = \
            directory_manager.pull_directory('linguamatics_i2e_project_queries_dir')
        ret_val = self._fix_queries(general_queries_dir)
        ret_val = self._fix_queries(project_queries_dir)

    #
    def folder_downloader(self, query_folder, local_destination):
        folder = Resource(query_folder)
        parent = folder.uri.replace(os.path.basename(os.path.normpath(folder.uri)),'')
        download_path = os.path.normpath(local_destination) if local_destination is not None else os.path.normpath(os.getcwd())
        request_maker = RequestMaker(self.conn)
        self._folder_downloader(request_maker, folder, parent, download_path)
        
    #
    def generate_csv_files(self):
        directory_manager = self.static_data['directory_manager']
        data_dir = directory_manager.pull_directory('postprocessing_data_in')
        for filename in os.listdir(data_dir):
            filename_base, extension = os.path.splitext(filename)
            if extension in [ '.xml' ]:
                print('Converting ' + filename)
                filename = data_dir + '/' + filename
                generate_gold(filename, True)
                
    #
    def generate_data_dict(self, data_file):
        directory_manager = self.static_data['directory_manager']
        data_dir = directory_manager.pull_directory('postprocessing_data_in')
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
        self.data_csv = data_dict
        self.data_dict_list = []
        if bool(self.data_csv):
            self._build_data_dictionary()
        return self.data_dict_list
        
    #
    def generate_i2e_resource_files(self, max_files_per_zip):
        directory_manager = self.static_data['directory_manager']
        general_queries_source_dir = directory_manager.pull_directory('linguamatics_i2e_general_queries_dir')
        preprocessing_data_out_dir = directory_manager.pull_directory('linguamatics_i2e_preprocessing_data_out')
        processing_data_dir = directory_manager.pull_directory('processing_data_dir')
        project_queries_source_dir = directory_manager.pull_directory('linguamatics_i2e_project_queries_dir')
        self.linguamatics_i2e_writer.generate_query_bundle_file(self.project_name,
                                                                general_queries_source_dir,
                                                                processing_data_dir,
                                                                project_queries_source_dir,
                                                                max_files_per_zip)
        self.linguamatics_i2e_writer.generate_regions_file(preprocessing_data_out_dir,
                                                           processing_data_dir)
        self.linguamatics_i2e_writer.generate_xml_configuation_file(preprocessing_data_out_dir,
                                                                    processing_data_dir)
        
    #
    def get_i2e_version(self, password):
        auth_values = (self.user, password)
        headers = {'X-License-Pool': self.license_pool}
        with requests.get(self.server + '/api', auth=auth_values, headers=headers, verify=False) as r:
            try:
                response = r.headers['X-Version']
            except:
                response = 'FAILED_TO_CONNECT'
        return response
    
    #
    def login(self):
        self.conn.login()
        
    #
    def logout(self):
        self.conn.logout()

    #
    def make_index_runner(self):
        index_template = \
            self.linguamatics_i2e_file_manager.i2e_resource('index_template')
        print('Making I2E index ' + self.project_name)
        template = Resource(index_template)
        source_data_path = Resource("/api;type=source_data/%s" %
                                    self.project_name)
        task_launcher = TaskLauncher(self.conn)
        index_config = task_launcher.create_index_configuration()
        index_config.set_source_data(source_data_path)
        monitor = task_launcher.make_index(template, index_config)
        while monitor.is_running():
            time.sleep(5)
        print("Task status is %s" % monitor.get_status())
        
    #
    def preindexer(self, keywords_file, processing_data_dir, source_data_dir,
                   max_files_per_zip):
        directory_manager = self.static_data['directory_manager']
        preprocessing_data_out_dir = directory_manager.pull_directory('linguamatics_i2e_preprocessing_data_out')
        self.linguamatics_i2e_writer.generate_source_data_file(self.project_name,
                                                               preprocessing_data_out_dir,
                                                               source_data_dir,
                                                               max_files_per_zip)
        self._put_keywords_file(keywords_file, self.linguamatics_i2e_writer)
        for resource in [ 'regions', 'source_data', 'xmlconf' ]:
            filename = os.path.join(processing_data_dir,
                                    self.linguamatics_i2e_file_manager.filename(resource))
            if resource == 'regions':
                resource_type = 'region_list'
            elif resource == 'source_data':
                resource_type = 'source_data'
            elif resource == 'xmlconf':
                resource_type = 'xml_and_html_config_file'
            try:
                self.delete_resource(self.linguamatics_i2e_file_manager.i2e_resource(resource_type))
            except Exception as e:
                print(e)
            if resource_type == 'source_data':
                for source_data_file in sorted(os.listdir(source_data_dir)):
                    try:
                        self.create_resource(self.project_name, resource_type,
                                             os.path.join(source_data_dir, source_data_file))
                    except Exception as e:
                        print(e)
            else:
                try:
                    self.create_resource(None, resource_type, filename)
                except Exception as e:
                    print(e)
        try:
            bundle = os.path.join(processing_data_dir,
                                  self.linguamatics_i2e_file_manager.query_bundle_filename())
            self.upload_bundle(bundle)
        except Exception as e:
            print(e)
            
    #
    def set_index_configuration(self, project_name):
        index_config = MakeIndexConfiguration()
        index_config.set_source_data("/api;type=source_data/" + project_name)
            
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
        # print(install_status)
        if install_status.startswith('succeeded'):
            print('Bundle upload succeeded')
        else:
            print('Bundle upload failed')