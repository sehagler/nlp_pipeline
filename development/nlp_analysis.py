# -*- coding: utf-8 -*-
"""
Created on Wed Aug 1 9:05:23 2018

@author: haglers
"""

#
import getpass
import sys

#
sys.dont_write_bytecode = True

#
server_base = '/home/groups/hopper2/RDW_NLP_WORKSPACE/NLP'
x_root_base = 'X:/OHSU Shared/Restricted/OCTRI/Informatics/NLP'
z_root_base = 'Z:/NLP'

#
project_names = [ 'AdverseEvents', 'BeatAML_Waves_1_And_2',
                  'BeatAML_Waves_3_And_4', 'BreastCancerPathology', 'CCC19' ]
project_subdirs = [ 'production', 'test' ]
root_dirs = [ 'X', 'Z', 'server' ]
servers = [ 'development', 'production' ]

#
pipeline_mode_flgs = [ 'check_queries', 'training_sets', 'prequeries', 'postqueries' ]

#
mode_flgs = [ 'update', 'run' ]

#
project_name = project_names[3]
project_subdir = project_subdirs[1]
root_dir = root_dirs[2]
server = servers[0]

#
pipeline_mode_flg = pipeline_mode_flgs[0]

#
mode_flg = mode_flgs[1]

#
if root_dir == 'server':
    root_base = server_base + '/NLP_Sandbox/' + getpass.getuser()
elif root_dir == 'X':
    root_base = x_root_base + '/NLP_Sandbox/' + getpass.getuser()
elif root_dir == 'Z':
    root_base = z_root_base + '/NLP_Sandbox/' + getpass.getuser()
else:
    print('unknown root_base')
    
#
software_base = root_base + '/NLP_Software/'

#
if mode_flg == 'update':
                
    #
    software_path = software_base + 'development'
    sys.path.insert(0, software_path)
    from nlp_lib.py.nlp_processor_lib.nlp_processor import Nlp_processor
    password = getpass.getpass()
    nlp_process = Nlp_processor()
    nlp_process.software_manager(password, root_dir)
    nlp_process.move_software()
    
elif mode_flg == 'run':

    #
    software_path = software_base + server
    sys.path.insert(0, software_path)
    from nlp_lib.py.nlp_processor_lib.nlp_processor import Nlp_processor
    password = getpass.getpass()
    nlp_process = Nlp_processor()
    nlp_process.pipeline_manager(server, root_dir, project_subdir,
                                 project_name, password)
    if pipeline_mode_flg == 'check_queries':
        nlp_process.fix_linguamatics_i2e_queries()
    elif pipeline_mode_flg == 'training_sets':
        nlp_process.generate_training_data_sets(password)
    elif pipeline_mode_flg == 'prequeries':
        nlp_process.prequeries(password)
    elif pipeline_mode_flg == 'postqueries':
        nlp_process.postqueries_preperformance()
        if project_subdir == 'test':
            nlp_process.calculate_performance()
        nlp_process.postqueries_postperformance()
    #nlp_process.download_queries()
    
#
sys.path.remove(software_path)