# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 11:37:05 2023

@author: haglers
"""

#
from base_lib.manager_base_class import Manager_base

#
class Evaluator_base(Manager_base):
    
    #
    def __init__(self, static_data_object, logger_object):
        Manager_base.__init__(self, static_data_object, logger_object)