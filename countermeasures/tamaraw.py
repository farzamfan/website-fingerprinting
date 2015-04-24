# -*- coding: utf-8 -*-
from Packet import Packet
from countermeasure import CounterMeasure


class TamarawCounterMeasure(CounterMeasure):
    PACKET_DELAY_OUT = 20
    PACKET_DELAY_IN = 6
    CELL_SIZE = 750
    L = 100

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
                t_last_sent += self.PACKET_DELAY_OUT

        # Ensure total transfer packets is a multiple of L
        for _ in range(-self.new_trace.get_packet_count() % self.L):
            self.add_packet(Packet(Packet.UP, t_last_sent, self.CELL_SIZE))
            t_last_sent += self.PACKET_DELAY_OUT
