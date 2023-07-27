# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 12:28:51 2023

@author: haglers
"""

#
class Worker_base(object):
    
    #
    def __init__(self, static_data_object, directory_object, logger_object):
        self.static_data_object = static_data_object
        self.directory_object = directory_object
        self.logger_object = logger_object
    
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
                    log_text = 'Process ' + str(process_idx) + ' starting'
                    self.logger_object.print_log(log_text)
                    return_dict = self._process_data(argument_dict)
                    log_text = 'Process ' + str(process_idx) + ' ending'
                    self.logger_object.print_log(log_text)
                    return_queue.put(return_dict)