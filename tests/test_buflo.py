# -*- coding: utf-8 -*-
import unittest

from Packet import Packet
from Trace import Trace
from buflo import BufloCounterMeasure


class BufloTest(unittest.TestCase):
    def test_send_1(self):
        t1 = Trace.create_from_array(1, [
            [0, 10, 100],
            [1, 20, 70],
            [0, 25, 200],
            [1, 37, 1500],
            [1, 40, 520],
            [0, 41, 70],
            [1, 57, 1500],
            [1, 60, 1500],
            [1, 70, 200],
            [0, 100, 70],
        ])
        t2 = BufloCounterMeasure().apply_to_trace(t1)
        new_trace = [
            (0, 10, 1000),   # 10
            (1, 20, 1000),   # 20
            (0, 30, 1000),   # 25
            (1, 40, 1000),   # 37
            (1, 50, 1000),
            (1, 60, 1000),   # 40
            (0, 70, 1000),   # 41
            (1, 80, 1000),   # 57
            (1, 90, 1000),
            (1, 100, 1000),  # 60
            (1, 110, 1000),
            (1, 120, 1000),  # 70
            (0, 130, 1000),  # 100
            (0, 140, 1000),  # Transmit Pad
            (0, 150, 1000),
            (0, 160, 1000),
            (0, 170, 1000),
            (0, 180, 1000),
            (0, 190, 1000),
            (0, 200, 1000),
        ]
        self.assertListEqual(map(Packet.get_details, t2.getPackets()), new_trace)


if __name__ == '__main__':
    unittest.main()
