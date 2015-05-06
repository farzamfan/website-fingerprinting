# -*- coding: utf-8 -*-
import unittest

from Packet import Packet


class TrafficTest(unittest.TestCase):
    def assertTraceEqual(self, trace2, trace1):
        self.assertListEqual(map(Packet.get_details, trace2.getPackets()), trace1)
