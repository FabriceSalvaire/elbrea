####################################################################################################
# 
# Elbrea - Electronic Board Reverse Engineering Assistant
# Copyright (C) 2014 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
####################################################################################################

####################################################################################################

class Transition(object):

    ##############################################

    def __init__(self, from_, to, token, value=None, do=None):

        self.from_ = from_
        self.to = to
        self.token = token
        self.value = value
        self.do = do

    ##############################################

    def match_from(self, from_):

        return self.from_ == from_

    ##############################################

    def match(self, token, value):

        if self.value is not None:
            return self.token == token and self.value == value
        else:
            return self.token == token

    ##############################################

    def as_do(self):

        return self.do is not None

####################################################################################################

class FiniteStateAutomata(object):

    __states__ = ()
    __transitions__ = ()

    ##############################################

    def __init__(self, callback):

        self._callback = callback
        self._state = '0'

    ##############################################

    def _transitions_for_state(self):

        return [transition for transition in self.__transitions__ 
                if transition.match_from(self._state)]

    ##############################################

    def step(self, token, value):

        for transition in self._transitions_for_state():
            if transition.match(token, value):
                self._state = transition.to
                if transition.as_do():
                    getattr(self, transition.do)(token, value)

####################################################################################################
# 
# End
# 
####################################################################################################
