# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 13:05:05 2022

@author: haglers
"""

#
import re

#
class Lambda_object(object):
    
    #
    def lambda_conversion(self, abstraction_operator, expression, argument):
        return re.sub('(?i)' + abstraction_operator, argument, expression)
    
    #
    def contextual_lambda_conversion(self, context_abstraction_operator,
                                     abstraction_operator, expression,
                                     argument):
        stop_flg = False
        ctr = 0
        while not stop_flg:
            ctr += 1
            stop_flg = True
            for match in re.finditer('(?i)' + context_abstraction_operator, expression):
                if match is not None:
                    stop_flg = False
                    search_str = match.group(0)
                    match_argument = \
                        self.lambda_conversion(abstraction_operator,
                                               search_str, argument)
                    expression = expression.replace(search_str, match_argument)
            if ctr == 100:
                stop_flg = True
        return expression
    
    #
    def deletion_lambda_conversion(self, abstraction_operator, expression):
        return self.lambda_conversion(abstraction_operator, expression, '')
    
    #
    def erasure_lambda_conversion(self, abstraction_operator, expression):
        return self.lambda_conversion(abstraction_operator, expression, ' ')
    
    #
    def initialism_lambda_conversion(self, abstraction_operator, expression, argument):
        expression = self.lambda_conversion(abstraction_operator + '( \( ?' + argument + ' ?\))?',
                                            expression, argument)
        return self.lambda_conversion(argument + ' \( ?' + argument + ' ?\)',
                                      expression, argument)
    
        #
    def space_correction_lambda_conversion(self, abstraction_operator, expression, argument):
        return self.lambda_conversion(abstraction_operator, expression, ' ' + argument + ' ')