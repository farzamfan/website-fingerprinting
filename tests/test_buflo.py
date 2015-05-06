# -*- coding: utf-8 -*-
import unittest

from Folklore import Folklore
from Trace import Trace
from tamaraw import Tamaraw
from tests.traffic_test import TrafficTest


class BufloTest(TrafficTest):
    TRACE_1 = [
        [0, 10, 100],   # u1
        [1, 20, 70],    # d1
        [0, 25, 200],   # u2
        [1, 37, 1500],  # d2
        [1, 40, 520],   # d3
        [0, 41, 70],    # u3
        [1, 57, 1500],  # d4
        [1, 60, 1500],  # d5
        [1, 70, 200],   # d6
        [0, 100, 70],   # u4
    ]

    TRACE_2 = [
        [0, 8, 100],    # u1
        [1, 20, 70],    # d1
        [0, 25, 200],   # u2
        [1, 30, 1500],  # d2
    ]

    def test_send_1(self):
        t1 = Trace.create_from_array(1, self.TRACE_1)
        Folklore.FIXED_PACKET_LEN = 1000
        Folklore.TIMER_CLOCK_SPEED = 10
        Folklore.MILLISECONDS_TO_RUN = 200
        t2 = Folklore.applyCountermeasure(t1)
        expected_trace = [
            (1, 0, 1000), (0, 0, 1000),        # -  u1
            (1, 10, 1000), (0, 10, 1000),      # -  -
            (1, 20, 1000), (0, 20, 1000),      # d1 -
            (1, 30, 1000), (0, 30, 1000),      # -  u2
            (1, 40, 1000), (0, 40, 1000),      # d2 -
            (1, 50, 1000), (0, 50, 1000),      # d2 u3
            (1, 60, 1000), (0, 60, 1000),      # d3 -
            (1, 70, 1000), (0, 70, 1000),      # d4 u4
            (1, 80, 1000), (0, 80, 1000),      # d4 -
            (1, 90, 1000), (0, 90, 1000),      # d5 -
            (1, 100, 1000), (0, 100, 1000),    # d5 -
            (1, 110, 1000), (0, 110, 1000),    # d6 -
            (1, 120, 1000), (0, 120, 1000),    # -  -
            (1, 130, 1000), (0, 130, 1000),    # -  -
            (1, 140, 1000), (0, 140, 1000),    # -  -
            (1, 150, 1000), (0, 150, 1000),    # -  -
            (1, 160, 1000), (0, 160, 1000),    # -  -
            (1, 170, 1000), (0, 170, 1000),    # -  -
            (1, 180, 1000), (0, 180, 1000),    # -  -
            (1, 190, 1000), (0, 190, 1000),    # -  -
            (1, 200, 1000), (0, 200, 1000),    # -  -
        ]
        self.assertTraceEqual(t2, expected_trace)

    def test_tamaraw_1(self):
        t1 = Trace.create_from_array(1, self.TRACE_2)
        cm = Tamaraw()
        cm.set_param('RUN_PADDING', 4)
        t2 = cm.apply_to_trace(t1)
        expected_trace = [
            (1, 0, 750),
            (0, 0, 750),
            (1, 6, 750),
            (1, 12, 750),
            (1, 18, 750),
            (0, 20, 750),   # u1
            (1, 24, 750),   # d1
            (1, 30, 750),   # d2-1
            (1, 36, 750),   # d2-2
            (0, 40, 750),   # u2
            (1, 42, 750),
            (0, 60, 750),
        ]
        self.assertTraceEqual(t2, expected_trace)


if __name__ == '__main__':
    unittest.main()
