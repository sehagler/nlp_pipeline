# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 09:40:02 2022

@author: haglers
"""

#
import csv
import datetime
import os
import re
import xml.etree.ElementTree as ET

#
from tool_lib.py.processing_tools_lib.file_processing_tools import read_xlsx_file

#
class Ohsu_nlp_template_manager(object):
    
    #
    def _apply_template(self, template, template_sections_list, text_dict):
        for document_id in text_dict.keys():
            for key in text_dict[document_id].keys():
                offset_base = text_dict[document_id][key]['OFFSET_BASE']
                section = text_dict[document_id][key]['TEXT']
                if template is not None:
                    template = re.compile(template)
                now = datetime.datetime.now()
                timestamp = now.strftime("%m/%d/%Y %H:%M:%S")
                if template is not None:
                    create_output_flg = True
                    if template_sections_list is not None:
                        create_output_flg = False
                        for section_name in template_sections_list:
                            if section_name in key[0]:
                                create_output_flg = True
                    if create_output_flg:
                        matches = template.finditer(section)
                        if bool(matches):
                            for match in matches:
                                query_output = match.group(0)
                                start = match.start() + offset_base
                                end = match.end() + offset_base - 1
                                offset = [ (start, end) ]
                                snippet = section
                                template_output = \
                                    [ document_id, timestamp, key[0], key[1],
                                      query_output, snippet, offset ]
                                self.template_output.append(template_output)
                else:
                    if template_sections_list is not None:
                        create_output_flg = False
                        for section_name in template_sections_list:
                            if section_name in key[0]:
                                create_output_flg = True
                    if create_output_flg:
                        query_output = section
                        snippet = section
                        offset = []
                        template_output = \
                            [ document_id, timestamp, key[0], key[1],
                              query_output, snippet, offset ]
                        self.template_output.append(template_output)
    
    #
    def _create_keywords_regexp(self, keywords):
        keywords_list = keywords.split('\n')
        keywords_list.remove('')
        keywords_regexp_str = '('
        for i in range(len(keywords_list)-1):
            keywords_regexp_str += keywords_list[i] + '|'
        keywords_regexp_str += keywords_list[-1] + ')'
        keywords_regexp = re.compile(keywords_regexp_str)
        return keywords_regexp
    
    #
    def _create_text_dict_preprocessing_data_out(self, data_dir,
                                                 keywords_regexp):
        text_dict = {}
        filenames = os.listdir(data_dir)
        filenames = sorted(filenames)
        for filename in filenames:
            filename_base, extension = os.path.splitext(filename)
            if extension in [ '.xml' ]:
                parser = ET.iterparse(os.path.join(data_dir, filename))
            for event, elem in parser:
                if elem.tag == 'DOCUMENT_ID':
                    document_id = elem.text
                elif elem.tag == 'rpt_text':
                    text = elem.text
            text_dict[document_id] = \
                self._parse_document(keywords_regexp, text)
        return text_dict
    
    #
    def _create_text_dict_postprocessing_data_in(self, sections):
        document_ids = []
        for i in range(1, len(sections)):
            row = sections[i]
            document_ids.append(row[0])
        document_ids = list(set(document_ids))
        document_ids = sorted(document_ids)
        text_dict = {}
        for document_id in document_ids:
            text_dict[document_id] = {}
            for i in range(1, len(sections)):
                row = sections[i]
                if row[0] == document_id:
                    key = (row[2], row[3])
                    section = row[4]
                    offset_base = 0
                    if section != '.*':
                        text_dict[document_id][key] = {}
                        text_dict[document_id][key]['OFFSET_BASE'] = offset_base
                        text_dict[document_id][key]['TEXT'] = section
        return text_dict
    
    #
    def _parse_document(self, keywords_regexp, text):
        keyword = None
        offset_base = 0
        text_dict = {}
        for line in text.splitlines():
            if keywords_regexp.search(line):
                if keyword is not None:
                    key = (keyword, '')
                    text_dict[key] = {}
                    text_dict[key]['OFFSET_BASE'] = offset_base
                    text_dict[key]['TEXT'] = section
                offset_base += len(line)
                keyword = line
                section = ''
            else:
                offset_base += len(line)
                section += line + '\n'
        return text_dict
    
    #
    def clear_template_output(self):
        self.template_output = []
    
    #
    def run_template_preprocessing_data_out(self, data_dir, keywords_file,
                                            template, template_sections_list):
        with open(keywords_file) as f:
            keywords = f.read()
        keywords_regexp = self._create_keywords_regexp(keywords)
        text_dict = \
            self._create_text_dict_preprocessing_data_out(data_dir,
                                                          keywords_regexp)
        self._apply_template(template, template_sections_list, text_dict)
                             
    #
    def run_template_postprocessing_data_in(self, data_dir, template,
                                            template_sections_list):
        sections = []
        with open(os.path.join(data_dir, 'sections.csv')) as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                sections.append(row)
        text_dict = self._create_text_dict_postprocessing_data_in(sections)
        self._apply_template(template, template_sections_list, text_dict)
        
    #
    def write_template_output(self, data_dir, filename, header):
        with open(os.path.join(data_dir, filename), 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(self.template_output)