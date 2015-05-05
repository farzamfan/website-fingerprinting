from Packet import Packet
from countermeasure import CounterMeasure


class Buffer:
    def __init__(self):
        self.__array = []

    def queue(self):
        return self.__array

    def add(self, p):
        self.__array.append(p)

    def top(self):
        return self.__array[0]

    def remove(self):
        if self.has_packets():
            p = self.__array[0]
            del self.__array[0]
            return p
        else:
            return None

    def has_packets(self):
        return len(self.__array) > 0

    def pack_from(self, cell_capacity):
        packets = 0
        while cell_capacity > 0:
            p = self.remove()
            if p:
                packets += 1
            if p and (p.getLength() - Packet.HEADER_LENGTH) > cell_capacity:
                new_p = Packet(p.getDirection(), p.getTime(),
                              p.getLength() - Packet.HEADER_LENGTH - cell_capacity)
                self.add(new_p)
                break
            elif p and p.getLength() <= cell_capacity:
                cell_capacity -= (p.getLength() - Packet.HEADER_LENGTH)
            else:
                break
        return packets


class Tamaraw(CounterMeasure):
    DEFAULT_PARAMS = {
        'CELL_SIZE': 750,     # d
        'SEND_INTERVAL': 20,  # R_out
        'RECV_INTERVAL': 6,   # R_in
        'RUN_PADDING': 100,   # L
    }

    def apply(self):
        timer_up = 0
        timer_down = 0
        buffer_up = Buffer()
        buffer_down = Buffer()
        packet_cur_up = 0
        packet_cur_down = 0
        n_packets = self.trace.getPacketCount()
        n_packets_up = sum(1 for p in self.trace.packets if p.getDirection() == Packet.UP)
        n_packets_down = sum(1 for p in self.trace.packets if p.getDirection() == Packet.DOWN)
        n_sent_up = 0
        n_sent_down = 0
        L = self.params['RUN_PADDING']
        cell_size = self.params['CELL_SIZE']
        t_down = self.params['RECV_INTERVAL']
        t_up = self.params['SEND_INTERVAL']

        while n_sent_up + n_sent_down < n_packets \
                or buffer_up.has_packets() or buffer_down.has_packets():

            # add to buffer: all packets that appeared since last clock
            while packet_cur_down < n_packets \
                    and self.trace.packets[packet_cur_down].getTime() <= timer_down:
                packet = self.trace.packets[packet_cur_down]
                if packet.getDirection() == Packet.DOWN:
                    buffer_down.add(packet)
                    n_sent_down += 1
                packet_cur_down += 1
            while packet_cur_up < n_packets \
                    and self.trace.packets[packet_cur_up].getTime() <= timer_up:
                packet = self.trace.packets[packet_cur_up]
                if packet.getDirection() == Packet.UP:
                    buffer_up.add(packet)
                    n_sent_up += 1
                packet_cur_up += 1

            # check buffer: purge at most Packet.MTU bytes
            pcu = buffer_up.pack_from(cell_size - Packet.HEADER_LENGTH)
            pcd = buffer_down.pack_from(cell_size - Packet.HEADER_LENGTH)

            if n_sent_down < n_packets_down:
                self.add_packet(Packet(Packet.DOWN, timer_down, cell_size))
                timer_down += t_down
                n_sent_down += pcd

            if n_sent_up < n_packets_up:
                self.add_packet(Packet(Packet.UP, timer_up, cell_size))
                timer_up += t_up
                n_sent_up += pcu

        while (timer_up // t_up) % L:
            # print 'PAD UP'
            self.add_packet(Packet(Packet.UP, timer_up, cell_size))
            timer_up += t_up
        while (timer_down // t_down) % L:
            # print 'PAD DOWN'
            self.add_packet(Packet(Packet.DOWN, timer_down, cell_size))
            timer_down += t_down
