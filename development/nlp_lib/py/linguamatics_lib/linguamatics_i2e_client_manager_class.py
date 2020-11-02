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
import time

#
class Linguamatics_i2e_client_manager(object):
    
    #
    def __init__(self, project_data, password):
        server = project_data['acc_server']
        self.server = I2EServer(server[2])
        self.username = project_data['user']
        self.user = I2EUser(self.username, password)
        self.connection_settings = ClientConnectionSettings.create()

    #
    def create_resource(self, project_name, resource_type, resource_file):   
        with I2EConnection(self.server, self.user, connection_settings=self.connection_settings) as conn:
            conn.login()
            resource = "/api;type=" + resource_type + "/%s"
            if project_name is None:
                source_data_path = Resource(resource %
                                            os.path.basename(resource_file))
            else:
                source_data_path = Resource(resource %
                                            project_name + '/' + os.path.basename(resource_file))
            request_maker = RequestMaker(conn)
            with open(resource_file, 'rb') as source_data:
                request_maker.create_resource(source_data_path,
                                              "text/plain", source_data)

    #
    def delete_resource(self, resource):
        resource = Resource(resource)
        with I2EConnection(self.server, self.user, connection_settings=self.connection_settings) as conn:
            conn.login()
            request_maker = RequestMaker(conn)
            request_maker.delete_resource(resource)

    #
    def make_index_runner(self, index_template, project_name):
        template = Resource(index_template)
        with I2EConnection(self.server, self.user, connection_settings=self.connection_settings) as conn:
            conn.login()
            source_data_path = Resource("/api;type=source_data/%s" %
                                        project_name)
            task_launcher = TaskLauncher(conn)
            index_config = task_launcher.create_index_configuration()
            index_config.set_source_data(source_data_path)
            monitor = task_launcher.make_index(template, index_config)
            while monitor.is_running():
                time.sleep(5)
            print("Task status is %s" % monitor.get_status())
            
    #
    def set_index_configuration(self, project_name):
        with I2EConnection(self.server, self.user, connection_settings=self.connection_settings) as conn:
            conn.login()
            index_config = MakeIndexConfiguration()
            index_config.set_source_data("/api;type=source_data/" + project_name)
            
    #
    def upload_bundle(self, bundle):
        with I2EConnection(self.server, self.user, connection_settings=self.connection_settings) as conn:
            conn.login()
            request_maker = RequestMaker(conn)
            
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
        template = {"bundleHandle": unzip_location, "forceUpdate": True, "host": 'localhost', "user": self.username}
        request_maker2 = RequestMaker(conn)
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
        print('Uploading bundle...')
        while install_status == 'running':
            time.sleep(15)
            install_status_task = request_maker2.read_resource(install_location, "application/json", request_config2)
            install_status = json.loads(install_status_task.read())['status']
        # print(install_status)
        if install_status.startswith('succeeded'):
            print('Bundle upload succeeded')
        else:
            print('Bundle upload failed')