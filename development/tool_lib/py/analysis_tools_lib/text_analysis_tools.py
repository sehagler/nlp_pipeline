# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 15:33:03 2020

@author: haglers
"""

#
def levenshtein_distance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

#
def prune_surface_antigens(antigens):
    if len(antigens) > 1:
        text_list = list(set(antigens))
        if len(text_list) > 1:
            drop_list = []
            for i in range(len(text_list)-1):
                for j in range(len(text_list)-i-1):
                    text0 = text_list[i]
                    text1 = text_list[j+i+1]
                    text_score = compare_texts(text0, text1, True)
                    if text_score[2] == 0:
                        drop_list.append(text1)
                    elif text_score[0] == 0 and text_score[1] == 0:
                        tokens0 = text0.split(' ')
                        tokens1 = text1.split(' ')
                        if len(tokens0) < len(tokens1):
                            drop_list.append(text0)
                        elif len(tokens0) > len(tokens1):
                            drop_list.append(text1)
            text_list = list(set(text_list) - set(drop_list)) 
        if len(text_list) > 1:
            drop_list = []
            for i in range(len(text_list)-1):
                for j in range(len(text_list)-i-1):
                    text0 = text_list[i]
                    text1 = text_list[j+i+1]
                    text_score = compare_texts(text0, text1, True)
                    if text_score[0] > 0 and text_score[1] == 0:
                        drop_list.append(text1)
                    elif text_score[0] == 0 and text_score[1] > 0:
                        drop_list.append(text0)
            text_list = list(set(text_list) - set(drop_list))
        antigens = text_list
    return antigens