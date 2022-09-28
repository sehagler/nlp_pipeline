# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 10:44:47 2020

@author: haglers
"""

#
import os
import paramiko
import re
from stat import S_ISDIR, S_ISREG
import time
import traceback

#
from lambda_lib.lambda_manager_class import Lambda_manager

#
class Server_manager(object):
    
    #
    def __init__(self, static_data_manager, password):
        static_data = static_data_manager.get_static_data()
        if static_data['acc_server'] is not None:
            self.server = static_data['acc_server'][1]
        self.user = static_data['user']
        self.password = password
        self.lambda_manager = Lambda_manager
        
    #
    def _recursive_delete_directory(self, sftp, target_dir_in):
        for entry in sftp.listdir_attr(target_dir_in):
            mode = entry.st_mode
            if S_ISDIR(mode):
                target_dir = os.path.join(target_dir_in, entry.filename)
                target_dir = \
                    self.lambda_manager.lambda_conversion('\\\\', target_dir, '/')
                self._recursive_delete_directory(sftp, target_dir)
            elif S_ISREG(mode):
                target_file = os.path.join(target_dir_in, entry.filename)
                target_file = \
                    self.lambda_manager.lambda_conversion('\\\\', target_file, '/')
                sftp.remove(target_file)
        sftp.rmdir(target_dir_in)
        
    #
    def close_ssh_client(self):
        self.ssh_client.close()
        
    #
    def exec_sudo_command(self, cmd):
        cmd = 'sudo ' + cmd
        session = self.ssh_client.get_transport().open_session()
        session.get_pty()
        session.setblocking(1)
        session.exec_command(cmd)
        while session.recv_ready() == False:
            stdout = session.recv(4096)
            if re.search('[Pp]assword', stdout.decode('utf-8')):
                session.send(self.password + '\n')
            time.sleep(1)
        session.close()
        
    #
    def open_ssh_client(self):
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(hostname=self.server, username=self.user, 
                                password=self.password, allow_agent=True)
        
    #
    def push_directory(self, source_dir, target_dir):
        sftp = self.ssh_client.open_sftp()
        dir_path = ''
        for dir_folder in target_dir.split("/"):
            if dir_folder == "":
                continue
            dir_path += r"/{0}".format(dir_folder)
            try:
                sftp.listdir(dir_path)
            except Exception:
                traceback.print_exc()
                sftp.mkdir(dir_path)
        for root, dirs, files in os.walk(source_dir):
            for name in dirs:
                dir_path = os.path.join(root, name)
                dir_path = \
                    self.lambda_manager.lambda_conversion(source_dir, dir_path, target_dir)
                dir_path = \
                    self.lambda_manager.lambda_conversion('\\\\', dir_path, '/')
                try:
                    sftp.listdir(dir_path)
                except Exception:
                    traceback.print_exc()
                    sftp.mkdir(dir_path)
            for name in files:
                source_file = os.path.join(root, name)
                target_file = \
                    self.lambda_manager.lambda_conversion(source_dir, source_file, target_dir)
                source_file = \
                    self.lambda_manager.lambda_conversion('\\\\', source_file, '/')
                target_file = \
                    self.lambda_manager.lambda_conversion('\\\\', target_file, '/')
                sftp.put(source_file, target_file)
        sftp.close()
    
    #
    def push_file(self, source_file, target_file):
        sftp = self.ssh_client.open_sftp()
        sftp.put(source_file, target_file)
        sftp.close()
        
    #
    def remove_directory(self, target_dir):
        sftp = self.ssh_client.open_sftp()
        try:
            self._recursive_delete_directory(sftp, target_dir)
        except Exception:
            traceback.print_exc()
        sftp.close()