# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 11:27:35 2021

@author: haglers
"""

#
import glob
import os

#
def clean_directory(directory):
    if os.path.exists(directory):
        items = glob.glob(directory + '/*')
        for item in items:
            if os.path.isfile(item):
                os.remove(item)

'''                        
#
def clean_directory(label):
    directory = self.directory_dict[label]
    if os.path.exists(directory):
        items = glob.glob(directory + '/*')
        for item in items:
            if os.path.isfile(item):
                os.remove(item)
'''
                
#
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
                
'''
#
def create_directory(directory):
    if self.create_dir_flg:
        if not os.path.exists(directory):
            os.makedirs(directory)
'''