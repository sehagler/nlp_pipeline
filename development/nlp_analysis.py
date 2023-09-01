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
user = getpass.getuser()
password = getpass.getpass()
    
#
class Nlp_analysis_main_object(object):
    
    #
    def pipeline(self, server, project_subdir, pipeline_mode, project_name):
        root_dir = 'server'
        if root_dir == 'server':
            root_base = server_base + '/NLP_Sandbox/' + getpass.getuser()
        elif root_dir == 'X':
            root_base = x_root_base + '/NLP_Sandbox/' + getpass.getuser()
        elif root_dir == 'Z':
            root_base = z_root_base + '/NLP_Sandbox/' + getpass.getuser()
        else:
            print('unknown root_base')
        software_base = root_base + '/NLP_Software/'
        software_path = software_base + server
        sys.path.insert(0, software_path)
        from nlp_pipeline_lib.object_lib.pipeline_lib.pipeline_object_class \
            import Pipeline_object
        pipeline_object = Pipeline_object()
        pipeline_object.process_manager(server, root_dir, project_subdir,
                                        project_name, user, password)
        if pipeline_mode == 'training_sets':
            pipeline_object.generate_training_data_sets(password)
        elif pipeline_mode == 'linguamatics_i2e_prequeries':
            if True:
                pipeline_object.cleanup_directory('linguamatics_i2e_preprocessing_data_out')
                pipeline_object.initialize_metadata()
            pipeline_object.linguamatics_i2e_prequeries(password)
            pipeline_object.cleanup_directory('source_data')
            pipeline_object.linguamatics_i2e_indexer()
            pipeline_object.linguamatics_i2e_push_queries()
        elif pipeline_mode == 'linguamatics_i2e_indexer':
            pipeline_object.cleanup_directory('source_data')
            pipeline_object.linguamatics_i2e_indexer()
            pipeline_object.linguamatics_i2e_push_queries()
        elif pipeline_mode == 'linguamatics_i2e_postqueries':
            pipeline_object.cleanup_directory('postprocessing_data_out')
            pipeline_object.linguamatics_i2e_postqueries(project_subdir)
        elif pipeline_mode == 'linguamatics_i2e_push_queries':
            pipeline_object.linguamatics_i2e_push_queries()
        sys.path.remove(software_path)
    
    #
    def update(self):
        root_dirs = [ 'X', 'Z' ]
        for i in range(len(root_dirs)):
            root_dir = root_dirs[i]
            if root_dir == 'server':
                root_base = server_base + '/NLP_Sandbox/' + getpass.getuser()
            elif root_dir == 'X':
                root_base = x_root_base + '/NLP_Sandbox/' + getpass.getuser()
            elif root_dir == 'Z':
                root_base = z_root_base + '/NLP_Sandbox/' + getpass.getuser()
            else:
                print('unknown root_base')
            software_base = root_base + '/NLP_Software/'
            software_path = software_base + 'development'
            sys.path.insert(0, software_path)
            from nlp_pipeline_lib.object_lib.pipeline_lib.pipeline_object_class \
                import Pipeline_object
            pipeline_object = Pipeline_object()
            pipeline_object.software_manager(root_dir, user, password)
            pipeline_object.move_software()
            sys.path.remove(software_path)
    
#
def main():
    args = sys.argv[1:]
    print(args)
    mode = args[1]
    nlp_analysis_main_object = Nlp_analysis_main_object()
    if mode == 'pipeline':
        server = args[3]
        project_subdir = args[5]
        pipeline_mode = args[7]
        project_name = args[9]
        nlp_analysis_main_object.pipeline(server, project_subdir,
                                          pipeline_mode, project_name)
    elif mode == 'update':
        nlp_analysis_main_object.update()
    
#
if __name__ == "__main__":
    main()