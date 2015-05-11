# -*- coding: utf-8 -*-
from Packet import Packet
from config import website_clusters, cluster_distances, load_website_clusters
from countermeasure import CounterMeasure


class SmartMorphing(CounterMeasure):
    DEFAULT_PARAMS = {
        'CLUSTER_COUNT': 10,       # Total number of clusters
        'SECTION_COUNT': 10,       # Number of sections to divide traces into
        'D': 7,                    # For selecting target cluster
        'BANDWIDTH_D_FACTOR': 25,  # For converting D to bandwidth overhead threshold
        'DISTANCE_D_FACTOR': 0.5,  # For converting D to minimum acceptable morphing distance (from s to t)
        'MIN_JACCARD_SIMILARITY': 0.7,  # Copying extra dst packets (even in case of size overhead) until output reaches
                                        #   this similarity of dst
        'CLUSTERING_ALGORITHM': 'PAM10',  # MBC9, PAM10, SOM10
        'TIMING_METHOD': 'DST',    # MIN or DST
        'DEFAULT_PAUSE': 1,        # if timing method is not decisive
    }

    def __init__(self, *args, **kwargs):
        super(SmartMorphing, self).__init__(*args, **kwargs)
        self.D = self.D2 = 0
        self.update_params()
        self.dst_trace = None

    def update_params(self):
        self.D = self.params['D']
        self.D2 = 100 + self.D * self.params['BANDWIDTH_D_FACTOR']

    def apply(self):
        if self.dst_trace is None:
            pass  # TODO: select from clustering and database information
        self.morph_trace(self.trace, self.dst_trace)

    def morph_trace(self, src_trace, dst_trace):
        self.build_new_trace()
        dst_n = len(dst_trace.packets)
        src_n = len(src_trace.packets)
        head = {
            'src': 0,
            'dst': 0,
            'src-ended': src_n == 0,
            'dst-ended': dst_n == 0,
            'dst-timing': self.params['DEFAULT_PAUSE'],
            'src-timing': self.params['DEFAULT_PAUSE'],
            'dst-prev': None,
            'src-prev': None,
            'src-size': 0,
        }

        def pop_src_packet():
            # print 'SRC'
            pst = head['src-prev'][1] if head['src-prev'] else None
            ssd, sst, ssl = src_trace.packets[head['src']].get_details()
            head['src-size'] += ssl
            head['src-timing'] = (sst - pst) if pst else self.params['DEFAULT_PAUSE']
            head['src-prev'] = ssd, sst, ssl

            head['src'] += 1
            if head['src'] >= src_n:
                head['src-ended'] = True
            return ssd, sst, ssl

        def pop_dst_packet():
            # print 'DST'
            pdt = head['dst-prev'][1] if head['dst-prev'] else None
            ddd, ddt, ddl = dst_trace.packets[head['dst']].get_details()
            head['dst-timing'] = (ddt - pdt) if pdt else self.params['DEFAULT_PAUSE']
            head['dst-prev'] = ddd, ddt, ddl

            head['dst'] += 1
            if head['dst'] >= dst_n:
                head['dst-ended'] = True
                head['dst'] %= dst_n
                sh = dst_trace.packets[dst_n - 1].time + self.params['DEFAULT_PAUSE'] - dst_trace.packets[0].time
                for p in dst_trace.packets:
                    p.time += sh
            return ddd, ddt, ddl

        def size_overhead_reached():
            ovp = self.get_new_trace_size() * 100.0 / (head['src-size'] or 1)
            return ovp > self.D2

        def get_jaccard_similarity():
            return self.jaccard_similarity(map(Packet.getLength, self.new_trace.packets), map(Packet.getLength, dst_trace.packets))

        def print_overhead_report():
            jc = get_jaccard_similarity()
            ovp = self.get_new_trace_size() * 100.0 / (head['src-size'] or 1)
            ovps = '{0:.0f}%'.format(ovp)
            jcs = '{0:.2f}'.format(jc)
            if ovp > self.D2:
                ovps += ' +++'
            print head['src-size'], self.get_new_trace_size(), jcs, ovps

        while not head['src-ended']:
            print_overhead_report()
            sd, st, sl = pop_src_packet()
            dd, dt, dl = pop_dst_packet()
            if self.params['TIMING_METHOD'] == 'DST':
                send_time = dt if self.params['TIMING_METHOD'] == 'DST' else st
                send_time = max(st, send_time)  # can not send a packet before it is produced
            elif self.params['TIMING_METHOD'] == 'MIN':
                if st > self.get_new_trace_time():
                    send_time = st
                else:
                    send_time = st + min(head['src-timing'], head['dst-timing'])
            self.add_packet(Packet(sd, send_time, dl))
            if sl > dl:
                remaining = sl - dl
                while remaining > 0:
                    dd, dt, dl = pop_dst_packet()
                    if self.params['TIMING_METHOD'] == 'DST':
                        if dt > st:
                            send_time = dt
                        else:
                            send_time = st + head['dst-timing']
                    elif self.params['TIMING_METHOD'] == 'MIN':
                        send_time = st + min(head['src-timing'], head['dst-timing'])

                    self.add_packet(Packet(sd, send_time, dl))
                    remaining -= dl

        while not head['dst-ended']:
            print_overhead_report()
            if size_overhead_reached():  # we only break if we have *passed* the overhead threshold
                if get_jaccard_similarity() >= self.params['MIN_JACCARD_SIMILARITY']:
                    break
            dd, dt, dl = pop_dst_packet()
            self.add_packet(Packet(dd, dt, dl))

    def get_target_cluster(self):
        website_id = 1  # self.trace.getId().?
        return self.get_website_cluster(website_id)

    @classmethod
    def calc_manhattan_distance(cls, a, b):
        d = 0
        i = 0
        na = len(a)
        nb = len(b)
        while i < min(na, nb):
            d += abs(a[i] - b[i])
            i += 1
        while i < na:
            d += abs(a[i])
            i += 1
        while i < nb:
            d += abs(b[i])
            i += 1
        return d

    @classmethod
    def jaccard_similarity(cls, a, b):
        """ Calculate Jaccard Similarity Index for given lists (lists are interpreted as sets)

            :type a: list
            :type b: list
            :return: float
        """
        a = set(a)
        b = set(b)
        return len(a & b) * 1.0 / (len(a | b) or 1)

    @classmethod
    def get_website_cluster(cls, website_id):
        return website_clusters.get(website_id, 1)

    @classmethod
    def initialize(cls):
        load_website_clusters()
