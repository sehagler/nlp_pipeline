# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 09:57:58 2018

@author: haglers
"""

#
from fnmatch import fnmatch
import numpy as np
import os
import shutil
from xml.dom import minidom
import xml.etree.ElementTree as ET

#
from nlp_lib.py.manager_lib.server_manager_class import Server_manager
from nlp_lib.py.tool_lib.processing_tools_lib.file_processing_tools import remove_file, write_general_file, write_zip_file
from nlp_lib.py.tool_lib.processing_tools_lib.text_processing_tools import make_ascii, make_xml_compatible

#
class Linguamatics_i2e_writer(object):
    
    #
    def __init__(self, project_data, linguamatics_i2e_file_manager, password):
        self.clear_keywords_text()
        self.metadata_keys = []
        self.linguamatics_i2e_file_manager = linguamatics_i2e_file_manager
        self.project_data = project_data
        self.server_manager = Server_manager(self.project_data, password)
        
    #
    def _append_keywords_text(self, keyword, index_flg):
        if index_flg == 0:
            self.keywords_list.append(keyword)
        elif index_flg == 1: 
            self.keywords_list.append(keyword + ' \d+')
        self.keywords_list = list(set(self.keywords_list))
        
    #
    def _generate_query_bundle_file_component(self, filename, queries_dir, dest_path_base):
        max_files_per_zip = self.project_data['max_files_per_zip']
        for path, subdirs, files in os.walk(queries_dir):
            rel_path = os.path.relpath(path, queries_dir)
            dest_path = os.path.join (dest_path_base, rel_path)
            data_files = []
            for file in files:
                if fnmatch(file, '*.i2qy'):
                    data_files.append(os.path.join(path, file))
            write_zip_file(filename, data_files, dest_path, max_files_per_zip, remove_file_flg=False)
        
    #
    def _generate_xml_file(self, ctr, metadata, raw_text, rpt_text):
        self._set_metadata(metadata)
        raw_text = make_ascii(raw_text)
        raw_text = make_xml_compatible(raw_text)
        keys = metadata.keys()
        for key in keys:
            key_value = metadata[key]
            if key_value is not None:
                key_value = key_value.replace('\'','\\\'')
            metadata[key] = key_value
        report = ET.Element('REPORT')
        for key in keys:
            subelement = ET.SubElement(report, key)
            subelement.text = metadata[key]
        subelement = ET.SubElement(report, 'RAW_TEXT')
        subelement.text = raw_text
        subelement = ET.SubElement(report, 'rpt_text')
        subelement.text = rpt_text
        xml_str = minidom.parseString(ET.tostring(report)).toprettyxml(indent = "   ")
        outdir = self.linguamatics_i2e_file_manager.preprocessing_data_directory()
        filename = str(ctr) + '.xml'
        write_general_file(os.path.join(outdir, filename), xml_str)
        
    #
    def _read_file_metadata(self):
        data_dir = self.linguamatics_i2e_file_manager.preprocessing_data_directory()
        files = os.listdir(data_dir)
        xml = ET.parse(os.path.join(data_dir, files[0]))
        root_element = xml.getroot()
        self.metadata_keys = []
        for child in root_element:
            self.metadata_keys.append(child.tag)
        
    #
    def _set_metadata(self, metadata):
        self.metadata_keys += tuple(metadata.keys())
        self.metadata_keys = tuple(np.unique(self.metadata_keys))
        
    #
    def clear_keywords_text(self):
        self.keywords_list = []
        
    #
    def append_keywords_text(self, keyword):
        self._append_keywords_text(keyword, 0)
        
    #
    def generate_keywords_file(self):
        text = ''
        self.keywords_list.sort()
        for keyword in self.keywords_list:
            text += keyword + '\n'
        write_general_file(self.linguamatics_i2e_file_manager.keywords_file(), text)
        
    #
    def generate_query_bundle_file(self, project_name):
        dest_path_base = self.linguamatics_i2e_file_manager.query_bundle_path_base()
        filename = self.linguamatics_i2e_file_manager.bundle('query_bundle_file')
        remove_file(filename)
        general_dest_path_base = dest_path_base + 'General'
        general_queries_dir = \
            self.linguamatics_i2e_file_manager.general_queries_source_directory()
        self._generate_query_bundle_file_component(filename, general_queries_dir, general_dest_path_base)
        project_dest_path_base = dest_path_base + project_name
        project_queries_dir = \
            self.linguamatics_i2e_file_manager.project_queries_source_directory()
        self._generate_query_bundle_file_component(filename, project_queries_dir, project_dest_path_base)
    
    #
    def generate_regions_file(self):
        self._read_file_metadata()
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
        write_general_file(self.linguamatics_i2e_file_manager.resource_file('region_list'), text)
        
    #
    def generate_source_data_file(self, project_name):
        max_files_per_zip = self.project_data['max_files_per_zip']
        data_dir = self.linguamatics_i2e_file_manager.preprocessing_data_directory()
        data_files = [os.path.join(data_dir, file) for file in os.listdir(data_dir) if os.path.splitext(file)[1] == '.xml']
        write_zip_file(self.linguamatics_i2e_file_manager.resource_file('source_data'), data_files, None, max_files_per_zip)
        
    #
    def generate_xml_configuation_file(self):
        self._read_file_metadata()
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
        write_general_file(self.linguamatics_i2e_file_manager.resource_file('xml_and_html_config_file'), text)
        
    #
    def generate_xml_file(self, ctr, metadata, raw_text, rpt_text):
        self._generate_xml_file(ctr, metadata, raw_text, rpt_text)
        ret_val = True
        return ret_val
    
    #
    def get_keywords_list(self):
        return self.keywords_list
    
    #
    def merge_copy(self, linguamatics_i2e_writer_copy):
        self.keywords_list.extend(linguamatics_i2e_writer_copy.get_keywords_list())
        self.keywords_list = list(set(self.keywords_list))
    
    #
    def prepare_keywords_file(self, keywords_tmp_file):
        self.server_manager.open_ssh_client()
        self.server_manager.exec_sudo_command('chmod 664 ' + self.linguamatics_i2e_file_manager.server_file('keywords'))
        self.server_manager.close_ssh_client()
        shutil.copyfile(self.linguamatics_i2e_file_manager.keywords_file(), self.linguamatics_i2e_file_manager.server_file('keywords'))
        self.server_manager.open_ssh_client()
        self.server_manager.exec_sudo_command('chmod 644 ' + self.linguamatics_i2e_file_manager.server_file('keywords'))
        self.server_manager.close_ssh_client()
        
    #
    def prepare_keywords_file_ssh(self, keywords_tmp_file):
        self.server_manager.open_ssh_client()
        self.server_manager.push_file(self.linguamatics_i2e_file_manager.keywords_file(), keywords_tmp_file)
        self.server_manager.exec_sudo_command('mv ' + keywords_tmp_file + ' ' + self.linguamatics_i2e_file_manager.server_file('keywords'))
        self.server_manager.exec_sudo_command('chmod 664 ' + self.linguamatics_i2e_file_manager.server_file('keywords'))
        self.server_manager.exec_sudo_command('chown i2e:i2e ' + self.linguamatics_i2e_file_manager.server_file('keywords'))
        self.server_manager.close_ssh_client()