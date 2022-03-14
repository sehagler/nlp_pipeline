# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 09:57:58 2018

@author: haglers
"""

#
from fnmatch import fnmatch
import os
import shutil
import xml.etree.ElementTree as ET

#
from tool_lib.py.processing_tools_lib.file_processing_tools \
    import remove_file, write_file, write_zip_file

#
class Linguamatics_i2e_writer(object):
    
    #
    def __init__(self, linguamatics_i2e_file_manager, server_manager):
        self.linguamatics_i2e_file_manager = linguamatics_i2e_file_manager
        self.server_manager = server_manager
        
    #
    def _generate_query_bundle_file_component(self, filename, queries_dir,
                                              dest_path_base, max_files_per_zip):
        for path, subdirs, files in os.walk(queries_dir):
            rel_path = os.path.relpath(path, queries_dir)
            dest_path = os.path.join (dest_path_base, rel_path)
            data_files = []
            for file in files:
                if fnmatch(file, '*.i2qy'):
                    data_files.append(os.path.join(path, file))
            write_zip_file(filename, data_files, dest_path, max_files_per_zip, remove_file_flg=False)
        
    #
    def _read_file_metadata(self, preprocessing_data_out_dir):
        #data_dir = self.linguamatics_i2e_file_manager.preprocessing_data_directory()
        files = os.listdir(preprocessing_data_out_dir)
        xml = ET.parse(os.path.join(preprocessing_data_out_dir, files[0]))
        root_element = xml.getroot()
        self.metadata_keys = []
        for child in root_element:
            self.metadata_keys.append(child.tag)
        
    #
    def generate_query_bundle_file(self, project_name, 
                                   general_queries_source_dir,
                                   processing_data_dir,
                                   project_queries_source_dir,
                                   max_files_per_zip):
        dest_path_base = self.linguamatics_i2e_file_manager.query_bundle_path_base()
        filename = os.path.join(processing_data_dir,
                                self.linguamatics_i2e_file_manager.query_bundle_filename())
        remove_file(filename)
        general_dest_path_base = dest_path_base + 'General'
        self._generate_query_bundle_file_component(filename,
                                                   general_queries_source_dir,
                                                   general_dest_path_base,
                                                   max_files_per_zip)
        project_dest_path_base = dest_path_base + project_name
        self._generate_query_bundle_file_component(filename,
                                                   project_queries_source_dir,
                                                   project_dest_path_base,
                                                   max_files_per_zip)
    
    #
    def generate_regions_file(self, preprocessing_data_out_dir,
                              processing_data_dir):
        self._read_file_metadata(preprocessing_data_out_dir)
        text = []
        text.append('hc.metadata\t\"Record Metadata\"\t-\tnonleaf\n')
        for key in self.metadata_keys:
            text.append('\thc.' + key + '\t\"' + key + '\"\thc.metadata\tleaf\n')
        text.append('\n')
        text.append('hc.pathology_reports\t\"Healthcare Pathology Reports\"\t-\tnonleaf\n')
        text.append('\n')
        text.append('hc.section\t\"Section\"\thc.pathology_reports\tnonleaf\n')
        text.append('\thc.titled_section\t\"Titled Section\"\thc.section\tleaf\n')
        text.append('\thc.untitled_section\t\"Untitled Section\"\thc.section\tleaf\n')
        text.append('hc.subsection\t\"Subsection\"\thc.pathology_reports\tnonleaf\n')
        text.append('\thc.section_title\t\"Section Title\"\thc.subsection\tleaf\n')
        text.append('\thc.section_body\t\"Section Body\"\thc.subsection\tleaf\n')
        text.append('hc.shared_field\t\"Shared Field\"\thc.pathology_reports\tnonleaf\n')
        text.append('\thc.specimen\t\"Specimen Description\"\thc.shared_field\tleaf\n')
        text.append('\n')
        text.append('hc.shadow\t\"Healthcare Pathology Reports Shadow Regions\"\t-\tnonleaf,shadow\n')
        text.append('\thc.specimen_id\t\"Specimen Id\"\thc.shadow\tleaf,shadow\n')
        text.append('\n')
        text.append('linguamatics.metadata\t\"File Metadata\"\t-\tnonleaf,shadow\n')
        text.append('\tlinguamatics.filename\t"File Name"\tlinguamatics.metadata\tleaf,shadow\n')
        text.append('\tlinguamatics.indextype\t"Index Type"\tlinguamatics.metadata\tleaf,shadow\n')
        text.append('\tlinguamatics.lastmodified\t"Last Modified"\tlinguamatics.metadata\tleaf,shadow\n')
        text.append('\tlinguamatics.relativepath\t"Relative Path"\tlinguamatics.metadata\tleaf,shadow\n')
        text.append('\tlinguamatics.sourcetype\t"Source Type"\tlinguamatics.metadata\tleaf,shadow\n')
        text = ''.join(text)
        filename = os.path.join(processing_data_dir,
                                self.linguamatics_i2e_file_manager.regions_filename())
        write_file(filename, text, False, False)
        
    #
    def generate_source_data_file(self, project_name, preprocessing_data_out_dir,
                                  source_data_dir, max_files_per_zip):
        source_data_filename = self.linguamatics_i2e_file_manager.source_data_filename()
        data_files = [os.path.join(preprocessing_data_out_dir, file) \
                      for file in os.listdir(preprocessing_data_out_dir) \
                      if os.path.splitext(file)[1] == '.xml']
        write_zip_file(os.path.join(source_data_dir, source_data_filename),
                       data_files, None, max_files_per_zip)
        
    #
    def generate_xml_configuation_file(self, preprocessing_data_out_dir,
                                       processing_data_dir):
        self._read_file_metadata(preprocessing_data_out_dir)
        text = []
        text.append('split Report\n')
        text.append('\n')
        for key in self.metadata_keys:
            text.append('region\t' + key + '\t' + 'hc.' + key + '\t2\n')
        text.append('\n')
        text.append('region\tsection\thc.titled_section\t2\n')
        text.append('region\tuntitled_section\thc.untitled_section\t2\n')
        text.append('region\tsection_title\thc.section_title\t2\n')
        text.append('region\tsection_body\thc.section_body\t2\n')
        text.append('region\tspecimen\thc.specimen\t2\n')
        text.append('region\tspecimen/@id\thc.specimen_id\t2\n')
        text.append('\n')
        text.append('alias\ti2e_metadata_filename = file.name\n')
        text.append('token\ti2e_metadata_filename\t2\n')
        text.append('regionname\ti2e_metadata_filename\tlinguamatics.filename\t2\n')
        text.append('matchclass\ti2e_metadata_filename\texclude\t*\n')
        text.append('\n')
        text.append('alias\ti2e_metadata_relativepath = file.relativePath\n')
        text.append('token\ti2e_metadata_relativepath\t2\n')
        text.append('region\ti2e_metadata_relativepath\tlinguamatics.relativepath\t2\n')
        text.append('matchclass\ti2e_metadata_relativepath\texclude\t*\n')
        text.append('\n')
        text.append('alias\ti2e_metadata_indextype = \"XML\"\n')
        text.append('region\ti2e_metadata_indextype\tlinguamatics.indextype\t2\n')
        text.append('matchclass\ti2e_metadata_indextype\texclude\t*\n')
        text.append('\n')
        text.append('alias\ti2e_metadata_lastmodified = file.lastWriteTime\n')
        text.append('region\ti2e_metadata_lastmodified\tlinguamatics.lastmodified\t2\n')
        text.append('matchclass\ti2e_metadata_lastmodified\tinclude\tSEMANTIC_DATE_COMMON_FORMATS\texclude\t*\n')
        text.append('\n')
        text.append('createontology\tFirst\t1\t\"lineboundaries.Words per Line\"\t0\n')
        text.append('createontology\tLast\t1\t\"lineboundaries.Words per Line\"\t0\n')
        text.append('\n')
        text.append('regions\n')
        text.append('include\t*\t0\n')
        text = ''.join(text)
        filename = os.path.join(processing_data_dir,
                                self.linguamatics_i2e_file_manager.xmlconf_filename())
        write_file(filename, text, False, False)
    
    #
    def prepare_keywords_file(self, keywords_file, keywords_tmp_file):
        self.server_manager.open_ssh_client()
        self.server_manager.exec_sudo_command('chmod 664 ' + self.linguamatics_i2e_file_manager.server_file('keywords'))
        self.server_manager.close_ssh_client()
        shutil.copyfile(keywords_file, self.linguamatics_i2e_file_manager.server_file('keywords'))
        self.server_manager.open_ssh_client()
        self.server_manager.exec_sudo_command('chmod 644 ' + self.linguamatics_i2e_file_manager.server_file('keywords'))
        self.server_manager.close_ssh_client()
        
    #
    def prepare_keywords_file_ssh(self, keywords_file, keywords_tmp_file):
        self.server_manager.open_ssh_client()
        self.server_manager.push_file(keywords_file, keywords_tmp_file)
        self.server_manager.exec_sudo_command('mv ' + keywords_tmp_file + ' ' + self.linguamatics_i2e_file_manager.server_file('keywords'))
        self.server_manager.exec_sudo_command('chmod 664 ' + self.linguamatics_i2e_file_manager.server_file('keywords'))
        self.server_manager.exec_sudo_command('chown i2e:i2e ' + self.linguamatics_i2e_file_manager.server_file('keywords'))
        self.server_manager.close_ssh_client()