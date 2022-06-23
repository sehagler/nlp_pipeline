# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 16:32:22 2020

@author: haglers
"""

#
class Network_manager(object):
    
    #
    def __init__(self):
        self.servers = {}
        self.servers['development'] = \
            [ 'development', 'hopper1.ohsu.edu', 'https://hopper1.ohsu.edu:8334' ]
        self.servers['production'] = \
            [ 'production', 'hopper2.ohsu.edu', 'https://hopper2.ohsu.edu:8334' ]
            
    #
    def pull_server(self, key):
        if key is not None:
            server = self.servers[key]
        else:
            server =  None
        return server