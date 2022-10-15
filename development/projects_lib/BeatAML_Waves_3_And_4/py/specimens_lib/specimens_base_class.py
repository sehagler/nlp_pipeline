# -*- coding: utf-8 -*-
"""
Created on Mon Mar 04 10:19:41 2019

@author: haglers
"""

#
class Specimens_base(object):
    
    #
    def _make_strings(self, column_values):
        for i in range(len(column_values)):
            column_values[i] = str(column_values[i])
        return column_values
    
    #
    def generate_json_file(self, jsons_out_dir, filename):
        with open(os.path.join(jsons_out_dir, filename), 'w') as f:
            json.dump(self.data_json, f)
            
    #
    def get_data_json(self):
        return self.data_json
    
    #
    def get_data_json_counts(self, data_json):
        print(len(data_json.keys()))
        ctr = 0
        for key in data_json.keys():
            ctr += len(data_json[key].keys())
        print(ctr)