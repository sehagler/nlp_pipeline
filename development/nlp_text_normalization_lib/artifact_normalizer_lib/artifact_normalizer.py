# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 08:56:52 2021

@author: haglers
"""

#
import lambda_lib.object_lib.lambda_object_class as lambda_lib
        
#
def artifact_normalizer(text):
    text = \
        lambda_lib.deletion_lambda_conversion('(?<= )\(A\)(?= )', text)
    text = \
        lambda_lib.deletion_lambda_conversion('(?<= )\(H\)(?= )', text)
    text = \
        lambda_lib.deletion_lambda_conversion('(?<= )\(HCC\)(?= )', text)
    text = \
        lambda_lib.deletion_lambda_conversion('(?<= )\(L\)(?= )', text)
    text = \
        lambda_lib.deletion_lambda_conversion('(?<= )\(LAB\)(?= )', text)
    text = \
        lambda_lib.deletion_lambda_conversion('(?<= )\[[A-Z]{2}\](?= )', text)
    return text