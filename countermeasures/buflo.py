# -*- coding: utf-8 -*-
from Packet import Packet
from countermeasure import CounterMeasure


class BufloCounterMeasure(CounterMeasure):
    PACKET_DELAY = 10
    CELL_SIZE = 1000
    TRANSMIT_MIN_TIME = 200

    def apply(self):
        t_last_sent = 0
        for packet in self.trace.getPackets():
            d, t, l = packet.get_details()
            t_last_sent = max(t_last_sent, t)
            ps = packet.alter_size(self.CELL_SIZE)
            ps[-1].setLength(self.CELL_SIZE)
            for p in ps:
                p.setTime(t_last_sent)
                self.add_packet(p)
                t_last_sent += self.PACKET_DELAY

        # Ensure minimum total transfer time
        while t_last_sent <= self.TRANSMIT_MIN_TIME:
            self.add_packet(Packet(Packet.UP, t_last_sent, self.CELL_SIZE))
            t_last_sent += self.PACKET_DELAY
