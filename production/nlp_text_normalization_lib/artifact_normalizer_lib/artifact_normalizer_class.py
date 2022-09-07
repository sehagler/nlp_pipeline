# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 08:56:52 2021

@author: haglers
"""

#
from lambda_lib.lambda_manager_class import Lambda_manager

#
class Artifact_normalizer(object):
    
    #
    def __init__(self):
        self.lambda_manager = Lambda_manager()
        
    #
    def normalize_text(self, text):
        self.text = text
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?<= )\(A\)(?= )', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?<= )\(H\)(?= )', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?<= )\(HCC\)(?= )', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?<= )\(L\)(?= )', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?<= )\(LAB\)(?= )', self.text)
        self.text = \
            self.lambda_manager.deletion_lambda_conversion('(?<= )\[[A-Z]{2}\](?= )', self.text)
        return self.text