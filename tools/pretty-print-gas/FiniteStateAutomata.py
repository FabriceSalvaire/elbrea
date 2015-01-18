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
