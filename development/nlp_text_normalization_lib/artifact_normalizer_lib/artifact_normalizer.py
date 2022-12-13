# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 08:56:52 2021

@author: haglers
"""

#
from lambda_lib.object_lib.lambda_object_class import Lambda_object
        
#
def artifact_normalizer(text):
    lambda_object = Lambda_object()
    text = \
        lambda_object.deletion_lambda_conversion('(?<= )\(A\)(?= )', text)
    text = \
        lambda_object.deletion_lambda_conversion('(?<= )\(H\)(?= )', text)
    text = \
        lambda_object.deletion_lambda_conversion('(?<= )\(HCC\)(?= )', text)
    text = \
        lambda_object.deletion_lambda_conversion('(?<= )\(L\)(?= )', text)
    text = \
        lambda_object.deletion_lambda_conversion('(?<= )\(LAB\)(?= )', text)
    text = \
        lambda_object.deletion_lambda_conversion('(?<= )\[[A-Z]{2}\](?= )', text)
    return text