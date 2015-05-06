# -*- coding: utf-8 -*-
import unittest

from smartmorphing import SmartMorphing
from Trace import Trace
from tests.traffic_test import TrafficTest


class SmartMorphingTest(TrafficTest):
    TRACE_1_SRC = [
        [0, 10, 60],
        [0, 20, 90],
        [0, 30, 90],
        [0, 40, 170],
        [0, 50, 300],
    ]
    TRACE_1_DST = [
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

    def test_sm_1(self):
        t1_src = Trace.create_from_array(1, self.TRACE_1_SRC)
        t1_dst = Trace.create_from_array(1, self.TRACE_1_DST)
        cm = SmartMorphing()
        cm.set_param('D', 4)
        t2 = cm.morph_trace(t1_src, t1_dst)
        expected_trace = [
        ]
        self.assertTraceEqual(t2, expected_trace)


if __name__ == '__main__':
    unittest.main()
