# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 13:46:12 2024

@author: haglers
"""

#
import datetime
#from names_dataset import NameDataset
#from pydeidentify import Deidentifier, DeidentifiedText
import random
import re
import string

#
class Deidentifier_object(object):
    pass
    
    '''
    #
    def __init__(self):
        nd = NameDataset()
        names_dict = nd.get_top_names(n=200, use_first_names=True,
                                      country_alpha2='US', )
        first_names_list = []
        first_names_list.extend(names_dict['US']['M'])
        first_names_list.extend(names_dict['US']['F'])
        names_dict = nd.get_top_names(n=200, use_first_names=False,
                                      country_alpha2='US', )
        last_names_list = []
        last_names_list.extend(names_dict['US'])
        self.first_names_list = first_names_list
        self.last_names_list = last_names_list
        
    #
    def _random_age(self, text):
        matches = re.findall('[0-9]+ Y/O', text)
        for match_str in matches:
            match_list = match_str.split(' ')
            digit_list = []
            digit_list.append(str(random.randint(1,9)))
            digit_list.append(str(random.randint(0,9)))
            sub_age = ''.join(digit_list)
            sub_list = match_list
            sub_list[0] = sub_age
            sub_str = ' '.join(sub_list)
            text = re.sub(match_str, sub_str, text)
        return text
    
    #
    def _random_date(self, actual_date_str):
        actual_date_list = actual_date_str.split(' / ')
        now_year = datetime.datetime.now().year
        month = random.randint(1,12)
        if month in [4, 6, 9, 11]:
            day = str(random.randint(1,30))
        elif month == 2:
            day = str(random.randint(1,28))
        else:
            day = str(random.randint(1,31))
        year = str(now_year - random.randint(1,10))
        if len(actual_date_list[-1]) == 2:
            year = year[2:]
        if len(actual_date_list) >= 3:
            if actual_date_list[0].isnumeric and actual_date_list[1].isnumeric and actual_date_list[2].isnumeric:
                date_str = str(month) + ' / ' + day + ' / ' + year
            else:
                print(actual_date_str)
        elif len(actual_date_list) == 2:
            if actual_date_list[0].isnumeric and actual_date_list[1].isnumeric:
                date_str = str(month) + ' / ' + year
            else:
                print(actual_date_str)
        elif len(actual_date_list) == 1:
            if actual_date_list[0].isnumeric:
                date_str = year
            else:
                print(actual_date_str)
        else:
            print(actual_date_str)
        return date_str
    
    #
    def _random_initials(self, text):
        matches = re.findall('\( initials [A-Za-z]+ \)', text)
        for match_str in matches:
            match_list = match_str.split(' ')
            sub_initials = ''.join(random.choice(string.ascii_uppercase) for _ in range(len(match_list[2])))
            sub_list = match_list
            sub_list[2] = sub_initials
            sub_str = ' '.join(sub_list)
            text = re.sub(match_str, sub_str, text)
        return text
    
    #
    def _random_mrn(self, text):
        matches = re.findall('MRN [0-9]+', text)
        for match_str in matches:
            match_list = match_str.split(' ')
            match_mrn = match_list[1]
            digit_list = []
            for _ in range(len(match_mrn)):
                digit_list.append(str(random.randint(0,9)))
            sub_mrn = ''.join(digit_list)
            sub_list = match_list
            sub_list[1] = sub_mrn
            sub_str = ' '.join(sub_list)
            text = re.sub(match_str, sub_str, text)
        return text
        
    #
    def _random_person(self, actual_person_str):
        actual_person_list = actual_person_str.split(' ')
        if actual_person_str.isnumeric():
            person_str = actual_person_str
        elif len(actual_person_list) == 1:
            idx = random.randint(0,len(self.first_names_list)-1)
            person_str = self.first_names_list[idx]
        else:
            if ',' in actual_person_list:
                person_list = []
                idx = random.randint(0, len(self.last_names_list)-1)
                person_list.append(self.last_names_list[idx])
                person_list.append(',')
                idx = random.randint(0, len(self.first_names_list)-1)
                person_list.append(self.first_names_list[idx])
                person_str = ' '.join(person_list)
            else:
                person_list = []
                idx = random.randint(0, len(self.first_names_list)-1)
                person_list.append(self.first_names_list[idx])
                idx = random.randint(0, len(self.last_names_list)-1)
                person_list.append(self.last_names_list[idx])
                person_str = ' '.join(person_list)
        return person_str
    
    #
    def _replace_institution(self, text):
        institution = 'INSTITUTION'
        text = re.sub('KDL', institution, text)
        text = re.sub('OHSU', institution, text)
        return text
    
    #
    def deidentify(self, text):
        d = Deidentifier()
        text = self._random_mrn(text)
        text = self._random_initials(text)
        text = self._random_age(text)
        text = self._replace_institution(text)
        d_text: DeidentifiedText = d.deidentify(text)
        text = d_text.text
        person_ctr = d_text.counts['PERSON']
        date_ctr = d_text.counts['DATE']
        for i in range(date_ctr):
            date_key = 'DATE' + str(i)
            date_str = d_text.decode_mapping[date_key]
            date_str = self._random_date(date_str)
            text = re.sub(date_key, date_str, text)
        fac_ctr = d_text.counts['FAC']
        for i in range(fac_ctr):
            fac_key = 'FAC' + str(i)
            fac_str = d_text.decode_mapping[fac_key]
            text = re.sub(fac_key, fac_str, text)
        loc_ctr = d_text.counts['LOC']
        for i in range(loc_ctr):
            loc_key = 'LOC' + str(i)
            loc_str = d_text.decode_mapping[loc_key]
            text = re.sub(loc_key, loc_str, text)
        org_ctr = d_text.counts['ORG']
        for i in range(org_ctr):
            org_key = 'ORG' + str(i)
            org_str = d_text.decode_mapping[org_key]
            text = re.sub(org_key, org_str, text)
        for i in range(person_ctr):
            person_key = 'PERSON' + str(i)
            person_str = d_text.decode_mapping[person_key]
            person_str = self._random_person(person_str)
            text = re.sub(person_key, person_str, text)
        return text    
    '''
    
    #
    def deidentify(self, text):
        return text