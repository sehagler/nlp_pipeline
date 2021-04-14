# -*- coding: utf-8 -*-
"""
Created on Wed Aug 1 9:05:23 2018

@author: haglers
"""

#
import getpass
import sys

#
server_base = '/home/groups/hopper2/RDW_NLP_WORKSPACE/NLP'
x_root_base = 'X:/OHSU Shared/Restricted/OCTRI/Informatics/NLP'
z_root_base = 'Z:/NLP'

#
operation_modes = [ 'development', 'production' ]
project_names = [ 'AdverseEvents', 'BeatAML_Waves_1_And_2', 'BeatAML_Waves_3_And_4', 
                  'BreastCancerPathology', 'CCC19' ]
project_subdirs = [ 'production', 'test' ]
root_dir_flg = [ 'X', 'Z', 'server' ]

#
operation_mode = operation_modes[0]
project_name = project_names[2]
project_subdir = project_subdirs[1]
root_dir_flg = root_dir_flg[2]

#
if root_dir_flg == 'server':
    root_base = server_base + '/NLP_Sandbox/' + getpass.getuser()
elif root_dir_flg == 'X':
    root_base = x_root_base + '/NLP_Sandbox/' + getpass.getuser()
elif root_dir_flg == 'Z':
    root_base = z_root_base + '/NLP_Sandbox/' + getpass.getuser()
else:
    print('unknown root_base')
    
#
software_base = root_base + '/NLP_Software/'

#
if False:
                
    #
    software_path = software_base + 'development'
    sys.path.insert(0, software_path)
    from nlp_lib.py.nlp_processor_lib.nlp_processor import Nlp_processor
    password = getpass.getpass()
    nlp_process = Nlp_processor()
    nlp_process.software_manager(password, root_dir_flg)
    nlp_process.move_software()
    
#
if True:

    #
    software_path = software_base + operation_mode
    sys.path.insert(0, software_path)
    from nlp_lib.py.nlp_processor_lib.nlp_processor import Nlp_processor
    password = getpass.getpass()
    nlp_process = Nlp_processor()
    nlp_process.pipeline_manager(password, operation_mode, project_name,
                                 project_subdir, root_dir_flg)
    #nlp_process.generate_training_data_sets()
    nlp_process.pre_queries(password)
    #nlp_process.post_queries()
    #nlp_process.calculate_performance()
    #nlp_process.download_queries()
    
#
sys.path.remove(software_path)