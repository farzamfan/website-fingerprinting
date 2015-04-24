# -*- coding: utf-8 -*-
from Trace import Trace


class CounterMeasure(object):
    def __init__(self):
        self.trace = None
        self.new_trace = None
        self.metadata = None
        self.model = None

    def train(self, src_page=None, target_page=None):
        pass

    def apply(self):
        """ Create a new trace by applying the countermeasure to the original trace

            The original trace is available in self.trace
            The modified trace should be saved in self.new_trace or returned
        """
        raise NotImplementedError

    def build_new_trace(self):
        self.new_trace = Trace(self.trace.getId())

    def add_packet(self, packet):
        self.new_trace.add_packet(packet)

    def apply_to_trace(self, trace):
        self.trace = trace
        self.build_new_trace()
        t2 = self.apply()
        if t2 is None:
            t2 = self.new_trace
        return t2
