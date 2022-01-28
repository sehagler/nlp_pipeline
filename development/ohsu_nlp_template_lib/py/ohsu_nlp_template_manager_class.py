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
class Ohsu_nlp_template_manager(object):
    
    #
    def _apply_template(self, document_id, template, text_dict):
        for key0 in text_dict.keys():
            for key1 in text_dict[key0].keys():
                offset_base = text_dict[key0][key1]['OFFSET_BASE']
                section = text_dict[key0][key1]['TEXT']
                template = re.compile(template)
                now = datetime.datetime.now()
                timestamp = now.strftime("%m/%d/%Y %H:%M:%S")
                matches = template.finditer(section)
                if bool(matches):
                    for match in matches:
                        query_output = match.group(0)
                        start = match.start() + offset_base
                        end = match.end() + offset_base - 1
                        offset = [ (start, end) ]
                        snippet = section
                        template_output = \
                            [ document_id, timestamp, key0, key1, query_output, snippet, offset ]
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
    def _create_text_dict(self, keywords_regexp, text):
        keyword = None
        offset_base = 0
        text_dict = {}
        for line in text.splitlines():
            if keywords_regexp.search(line):
                if keyword is not None:
                    text_dict[keyword] = {}
                    text_dict[keyword][''] = {}
                    text_dict[keyword]['']['OFFSET_BASE'] = offset_base
                    text_dict[keyword]['']['TEXT'] = section
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
    def run_template(self, data_dir, keywords_file, template):
        with open(keywords_file) as f:
            keywords = f.read()
        keywords_regexp = self._create_keywords_regexp(keywords)
        for filename in os.listdir(data_dir):
            filename_base, extension = os.path.splitext(filename)
            if extension in [ '.xml' ]:
                parser = ET.iterparse(os.path.join(data_dir, filename))
            for event, elem in parser:
                if elem.tag == 'DOCUMENT_ID':
                    document_id = elem.text
                elif elem.tag == 'rpt_text':
                    text = elem.text
            text_dict = self._create_text_dict(keywords_regexp, text)
            self._apply_template(document_id, template, text_dict)
        
    #
    def write_template_output(self, data_dir, filename, header):
        with open(os.path.join(data_dir, filename), 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(self.template_output)