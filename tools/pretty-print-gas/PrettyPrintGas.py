####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

import os
import subprocess

from pygments.lexers import GasLexer # , CObjdumpLexer, CppObjdumpLexer
from pygments.token import Token

####################################################################################################

from FiniteStateAutomata import FiniteStateAutomata, Transition

####################################################################################################

class GasFiniteStateAutomata(FiniteStateAutomata):

    __states__ = ('0',
                  'in_type', 'in_type_constant', 'in_type_function', 'out_type_function',
                  'in_opcode',
                  )

    __transitions__ = (
        # Function
        Transition(from_='0',
                   token='Name.Attribute', value='.type',
                   to='in_type',
                   ),
        Transition(from_='in_type',
                   token='Name.Constant',
                   to='in_type_constant',
                   do='store_constant',
                   ),
        Transition(from_='in_type_constant',
                   token='Name.Attribute', value='@function',
                   to='in_type_function',
                   ),
        Transition(from_='in_type_function',
                   token='Text', value='\n',
                   to='0',
                   do='print_function',
                   ),

        # Opcode
        Transition(from_='0',
                   token='Name.Function',
                   to='in_opcode',
                   do='store_opcode',
                   ),
        Transition(from_='in_opcode',
                   token='Text', value='\n',
                   to='0',
                   do='print_opcode',
                   ),
        )

    ##############################################

    def __init__(self, callback):

        super(GasFiniteStateAutomata, self).__init__(callback)

        self._constant = None
        self._opcode = None

    ##############################################

    def store_constant(self, token, value):

        self._constant = value

    ##############################################

    def print_function(self, token, value):

        self._callback.print_function(self._constant)
        self._constant = None

    ##############################################

    def store_opcode(self, token, value):

        self._opcode = value

    ##############################################

    def print_opcode(self, token, value):

        self._callback.print_opcode(self._opcode)
        self._opcode = None

####################################################################################################

class PrettyPrintGas(object):

    ##############################################

    def __init__(self, input_file_name, output_file):

        self._input_file_name = input_file_name
        self._output_file = output_file

        with open(self._input_file_name, 'r') as f:
            self._source_code = f.read()
        self._lexer = GasLexer()

        self._get_intel_instructions()
        self._get_constants()

    ##############################################

    def _token_source(self):

        return self._lexer.get_tokens(self._source_code)

    ##############################################

    def _get_intel_instructions(self):

        self._intel_instructions = {}
        with open(os.path.join(os.path.dirname(__file__), 'intel-instructions.txt'), 'r') as f:
            for line in f:
                if not line.startswith('#'):
                    opcodes, description = line.split(' | ')
                    description = description.rstrip()
                    for opcode in opcodes.split('/'):
                        opcode = opcode.lower().rstrip()
                        self._intel_instructions[opcode] =  description

    ##############################################

    def _get_constants(self):

        self._constant_dict = {}
        for token_type, value in self._token_source():
            if token_type == Token.Name.Constant:
                if value not in self._constant_dict:
                    demangled_value = subprocess.check_output(['c++filt', value]).rstrip()
                    self._constant_dict[value] = demangled_value

    ##############################################

    def lex(self):

        for token_type, value in self._token_source():
            print(token_type, '=', value)

    ##############################################

    def pretty_print(self):

        automata = GasFiniteStateAutomata(self)
        for token_type, value in self._token_source():
            self._output_file.write(value)
            token = str(token_type).replace('Token.', '')
            automata.step(token, value)

    ##############################################

    def print_function(self, mangled_function):

        self._output_file.write('### Function: ' + self._constant_dict[mangled_function] + '\n')

    ##############################################

    def print_opcode(self, opcode):
        
        try:
            description = self._intel_instructions[opcode]
        except KeyError:
            try:
                opcode_base = opcode[:-1]
                description = self._intel_instructions[opcode_base] + ' / With Prefix ' + opcode[-1]
            except KeyError:
                description = 'Unknown instruction %s' % opcode
        self._output_file.write('# ' + ' '*8 + description + '\n')

####################################################################################################
#
# End
#
####################################################################################################
