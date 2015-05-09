# -*- coding: utf-8 -*-
import unittest

from smartmorphing import SmartMorphing
from Trace import Trace
from tests.traffic_test import TrafficTest


class SmartMorphingTest(TrafficTest):
    TRACE_2_SRC = [
        [0, 10, 60],
        [0, 20, 90],
        [0, 30, 90],
        [0, 40, 170],
        [0, 50, 300],
    ]
    TRACE_2_DST = [
        [0, 10, 30],
        [0, 20, 80],
        [0, 30, 90],
        [0, 40, 160],
        [0, 50, 330],
        [0, 60, 380],
        [0, 70, 150],
        [0, 80, 20],
        [0, 90, 100],
        [0, 100, 130],
    ]

    def run_trace_morph_test(self, src, dst, exp, **kwargs):
        t1_src = Trace.create_from_array(1, src)
        t1_dst = Trace.create_from_array(1, dst)
        cm = SmartMorphing()
        for k, v in kwargs.items():
            cm.set_param(k, v)
        cm.dst_trace = t1_dst
        t2 = cm.apply_to_trace(t1_src)
        self.assertTraceEqual(t2, exp)

    def test_sm_simple_morphing(self):
        src = [
            [0, 70, 300],
            [0, 71, 100],
        ]
        dst = [
            [0, 68, 200],
            [0, 71, 250],
            [0, 73, 300],
        ]
        expected_trace = [
            (0, 70, 200),
            (0, 71, 250),
            (0, 73, 300),
        ]
        self.run_trace_morph_test(src, dst, expected_trace, D=4)

    def test_sm_small_dst(self):
        src = [
            [0, 70, 300],
            [0, 71, 100],
            [0, 72, 10],
            [0, 73, 20],
            [0, 74, 30],
        ]
        dst = [
            [0, 68, 200],
            [0, 71, 250],
            [0, 73, 300],
        ]
        exp = [
            (0, 70, 200),
            (0, 71, 250),
            (0, 73, 300),
            (0, 0, 10),
            (0, 0, 20),
            (0, 0, 30),
        ]
        self.run_trace_morph_test(src, dst, exp, D=4)


if __name__ == '__main__':
    unittest.main()
