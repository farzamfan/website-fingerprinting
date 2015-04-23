# -*- coding: utf-8 -*-
from Trace import Trace
from Packet import Packet


class CounterMeasure(object):
    def __init__(self, trace):
        self.trace = trace
        self.new_trace = Trace(self.trace.getId())

    def apply(self):
        """ Create a new trace by applying the countermeasure to the original trace

            The original trace is available in self.trace
            The modified trace should be saved in self.new_trace
        """
        pass

    def get_new_trace(self):
        return self.new_trace
