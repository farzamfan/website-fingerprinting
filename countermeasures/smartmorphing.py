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
        'CLUSTERING_ALGORITHM': 'PAM10',  # MBC9, PAM10, SOM10
        'TIMING_METHOD': 'MIN',    # MIN or DST
   }

    def __init__(self, *args, **kwargs):
        super(SmartMorphing, self).__init__(*args, **kwargs)
        self.D = self.params['D']
        self.D2 = 100 + self.D * self.params['BANDWIDTH_D_FACTOR']
        self.dst_trace = None

    def apply(self):
        if self.dst_trace is None:
            pass  # TODO: select from clustering and database information
        self.morph_trace(self.trace, self.dst_trace)

    def morph_trace(self, src_trace, dst_trace):
        self.build_new_trace()
        dst_n = len(dst_trace.packets)
        head = {
            'src': 0,
            'dst': 0,
        }
        src_n = len(src_trace.packets)

        def pop_src_packet():
            sd, st, sl = src_trace.packets[head['src']].get_details()
            head['src'] += 1
            return sd, st, sl

        def pop_dst_packet(rewind=True):
            if rewind:
                if head['dst'] >= dst_n:
                    head['dst'] %= dst_n
            dd, dt, dl = dst_trace.packets[head['dst']].get_details()
            head['dst'] += 1
            return dd, dt, dl

        while head['src'] < src_n:
            sd, st, sl = pop_src_packet()
            dd, dt, dl = pop_dst_packet()
            self.add_packet(Packet(sd, st, dl))
            if sl > dl:
                remaining = dl - sl
                while remaining > 0:
                    dd, dt, dl = pop_dst_packet()
                    self.add_packet(Packet(sd, st, dl))
                    remaining -= dl

        while head['dst'] < dst_n:
            dd, dt, dl = pop_dst_packet(rewind=False)
            self.add_packet(Packet(dd, dt, dl))

    def get_target_cluster(self):
        website_id = 1  # self.trace.getId().?
        return self.get_website_cluster(website_id)

    @classmethod
    def calc_L1_distance(cls, a, b):
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
    def get_website_cluster(cls, website_id):
        return website_clusters.get(website_id, 1)

    @classmethod
    def initialize(cls):
        load_website_clusters()
