# -*- coding: utf-8 -*-
"""
Created on Mon Oct 01 14:35:28 2018

@author: haglers
"""

filename = 'anatomical_location.ansi'

term_set_0 = [ 'central', 'deep', 'distal', 'peripheral', 'proximal', 
               'superficial' ]
term_set_1 = [ 'anterior', 'dorsal', 'inferior', 'lateral', 'medial', 
               'posterial', 'superior' ]
term_set_2 = [ 'antero', 'dorso', 'infero', 'latero', 'medio', 'postero',
               'supero']

text = 'SID ohsu_anatomical_location\n\n'
text = text + 'anatomical_location\n'
text = text + '\tPT Anatomical Location\n'

for term in term_set_0:
    text = text + '\tSYN ' + term +'\n'
    
for term in term_set_1:
    text = text + '\tSYN ' + term +'\n'
    
for term1 in term_set_1:
    for term2 in term_set_1:
        if term1 != term2:
            text = text + '\tSYN ' + term1 + ' ' + term2 + '\n'
            text = text + '\tSYN ' + term1 + '/' + term2 + '\n'cd
            text = text + '\tSYN ' + term1 + '-' + term2 + '\n'
            
for term1 in term_set_2:
    for term2 in term_set_1:
        if term1[:-2] != term2[:len(term1)-2]:
            text = text + '\tSYN ' + term1 + term2 + '\n'
            text = text + '\tSYN ' + term1 + '-' + term2 + '\n'
    
f = open(filename, 'w+')
f.write(text)
f.close()