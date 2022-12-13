# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 09:56:24 2022

@author: haglers
"""

#
import os
import subprocess
from subprocess import STDOUT, PIPE
import sys

#
from base_lib.manager_base_class import Manager_base
from tools_lib.processing_tools_lib.file_processing_tools \
    import write_file

#
class Melax_clamp_manager(Manager_base):
    
    #
    def __init__(self, static_data_object):
        Manager_base.__init__(self, static_data_object)
    
    #
    def create_source_data_file(self, ctr, rpt_text):
        static_data = self.static_data_object.get_static_data()
        directory_manager = static_data['directory_manager']
        outdir = directory_manager.pull_directory('melax_clamp_preprocessing_data_out')
        filename = str(ctr) + '.txt'
        write_file(os.path.join(outdir, filename), rpt_text, False, False)
        ret_val = True
        return ret_val
    
    #
    def run_pipeline(self):
        umlsAPI = 'dde8473e-6f90-4de5-9733-b199ff4c0f78'

        clampcmd_dir = 'C:\\Users\\haglers\\Desktop\\ClampCmd_1.6.6\\ClampCmd_1.6.6'
        clampwin_dir = 'C:\\Users\\haglers\\Desktop\\ClampWin_1.6.6\\ClampWin_1.6.6'
        
        #input_dir = clampcmd_dir + '\\' + 'input'
        input_dir = clampwin_dir + '\\' + 'workspace\\MyPipeline\\disease-attribute\\Data\\Input'
        #output_dir = clampcmd_dir + '\\' + 'output'
        output_dir = clampwin_dir + '\\' + 'workspace\\MyPipeline\\disease-attribute\\Data\\Output'
        clampbin_dir = clampcmd_dir + '\\' +'bin/clamp-nlp-1.6.6-jar-with-dependencies.jar'
        #pipeline = clampcmd_dir + '\\' +'pipeline/clinical_pipeline.pipeline.jar'
        pipeline = clampwin_dir + '\\' + 'workspace\\MyPipeline\\disease-attribute\\Components\\disease-attribute.pipeline.jar'
        umlsIndex = clampcmd_dir + '\\' + 'resource/umls_index/'
        
        cmd = [ 'java', '-DCLAMPLicenceFile=' + clampcmd_dir + '\CLAMP.LICENSE', 
                '-Xmx3g',  '-cp', clampbin_dir, 'edu.uth.clamp.nlp.main.PipelineMain',
                '-i', input_dir, '-o', output_dir, '-p', pipeline, '-A', umlsAPI,
                '-I', umlsIndex ]
        
        process = \
            subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT, universal_newlines=True)
        
        while True:
            out = process.stdout.read(1)
            if out == '' and process.poll() != None:
                break
            if out != '':
                sys.stdout.write(out)
                sys.stdout.flush()