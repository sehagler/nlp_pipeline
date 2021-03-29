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
from i2e.wsapi.common import (ClientConnectionSettings, I2EConnection,
                  I2EServer, I2EUser, RequestMaker, RequestConfiguration)
from i2e.wsapi.serialize import Resource
from i2e.wsapi.task import MakeIndexConfiguration, TaskLauncher
import json
import os
import requests
import shutil
import sys
import time
import urllib

#
from linguamatics_i2e_lib.py.linguamatics_i2e_file_manager_class \
    import Linguamatics_i2e_file_manager
from linguamatics_i2e_lib.py.linguamatics_i2e_writer_class \
    import Linguamatics_i2e_writer

#
class Linguamatics_i2e_manager(object):
    
    #
    def __init__(self, project_data, password):
        self.project_data = project_data
        self.project_name = project_data['project_name']
        self.server = project_data['acc_server'][2]
        self.user = project_data['user']
        self.linguamatics_i2e_file_manager = \
            Linguamatics_i2e_file_manager(self.project_data)
        self.linguamatics_i2e_writer = \
            Linguamatics_i2e_writer(self.project_data, password)
        self.i2e_server = I2EServer(self.server)
        self.i2e_user = I2EUser(self.user, password)
        self.connection_settings = ClientConnectionSettings.create()
        self.license_pool = 'admin'
        self.conn = I2EConnection(self.i2e_server, self.i2e_user,
                                  connection_settings=self.connection_settings,
                                  license_pool=self.license_pool)
        
    #
    def _folder_downloader(self, request_maker, folder_name, parent_folder, download_folder):
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
    def _put_keywords_file(self, linguamatics_i2e_writer):
        keywords_tmp_file = '/tmp/keywords_default.txt'
        if self.project_data['root_dir_flg'] in ''.join([ 'X', 'Z' ]):
            linguamatics_i2e_writer.prepare_keywords_file_ssh(keywords_tmp_file)
        elif self.project_data['root_dir_flg'] in ''.join([ 'dev_server', 'prod_server' ]):
            linguamatics_i2e_writer.prepare_keywords_file(keywords_tmp_file)

    #
    def create_resource(self, project_name, resource_type, resource_file): 
        print('Creating I2E resource ' + resource_file)
        resource = "/api;type=" + resource_type + "/%s"
        if project_name is None:
            source_data_path = Resource(resource %
                                        os.path.basename(resource_file))
        else:
            source_data_path = Resource(resource %
                                        project_name + '/' + os.path.basename(resource_file))
        request_maker = RequestMaker(self.conn)
        with open(resource_file, 'rb') as source_data:
            request_maker.create_resource(source_data_path,
                                          "text/plain", source_data)

    #
    def delete_resource(self, resource):
        print('Deleting I2E resource ' + resource)
        resource = Resource(resource)
        request_maker = RequestMaker(self.conn)
        request_maker.delete_resource(resource)

    #
    def folder_downloader(self, query_folder, local_destination):
        folder = Resource(query_folder)
        parent = folder.uri.replace(os.path.basename(os.path.normpath(folder.uri)),'')
        download_path = os.path.normpath(local_destination) if local_destination is not None else os.path.normpath(os.getcwd())
        request_maker = RequestMaker(self.conn)
        self._folder_downloader(request_maker, folder, parent, download_path)
        
    #
    def generate_i2e_resource_files(self, dynamic_data_manager):
        self.linguamatics_i2e_writer.merge_dynamic_data_manager(dynamic_data_manager)
        self.linguamatics_i2e_writer.generate_keywords_file()
        self.linguamatics_i2e_writer.generate_query_bundle_file(self.project_name)
        self.linguamatics_i2e_writer.generate_regions_file()
        self.linguamatics_i2e_writer.generate_xml_configuation_file()
        
    #
    def generate_xml_file(self, ctr, metadata, raw_text, rpt_text):
        xml_ret_val = self.linguamatics_i2e_writer.generate_xml_file(ctr, 
                                                                     metadata,
                                                                     raw_text,
                                                                     rpt_text)
        return xml_ret_val
        
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
    def preindexer(self):
        self.linguamatics_i2e_writer.generate_source_data_file(self.project_name)
        self._put_keywords_file(self.linguamatics_i2e_writer)
        for resource_type in self.linguamatics_i2e_file_manager.resource_files_keys():
            try:
                self.delete_resource(self.linguamatics_i2e_file_manager.i2e_resource(resource_type))
            except Exception as e:
                print(e)
            if resource_type == 'source_data':
                data_dir = self.linguamatics_i2e_file_manager.source_data_directory()
                for source_data_file in sorted(os.listdir(data_dir)):
                    try:
                        self.create_resource(self.project_name, resource_type,
                                             os.path.join(data_dir, source_data_file))
                    except Exception as e:
                        print(e)
            else:
                try:
                    self.create_resource(None, resource_type,
                                         self.linguamatics_i2e_file_manager.resource_file(resource_type))
                except Exception as e:
                    print(e)
        for bundle_type in self.linguamatics_i2e_file_manager.bundles_keys():
            try:
                self.upload_bundle(self.linguamatics_i2e_file_manager.bundle(bundle_type))
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