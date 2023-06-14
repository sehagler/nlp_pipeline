# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 12:28:51 2023

@author: haglers
"""

#
class Worker_base(object):
    
    #
    def __init__(self, static_data_object):
        self.static_data_object = static_data_object
    
    #
    def process_data(self, argument_queue, return_queue):
        run_flg = True
        while run_flg:
            if not argument_queue.empty():
                argument_dict = argument_queue.get()
                if 'command' in argument_dict:
                    if argument_dict['command'] == 'stop':
                        run_flg = False
                else:
                    process_idx = argument_dict['process_idx']
                    print('Process ' + str(process_idx) + ' starting')
                    return_dict = self._process_data(argument_dict)
                    print('Process ' + str(process_idx) + ' ending')
                    return_queue.put(return_dict)