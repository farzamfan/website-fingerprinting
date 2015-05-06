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
   }

    def __init__(self, *args, **kwargs):
        super(SmartMorphing, self).__init__(*args, **kwargs)
        self.D = self.params['D']
        self.D2 = 100 + self.D * self.params['BANDWIDTH_D_FACTOR']

    def apply(self):
        pass

    def morph_trace(self, src_trace, dst_trace):
        dst_sizes = map(Packet.getLength, dst_trace.packets)
        dst_n = len(dst_sizes)
        dst_i = 0
        src_sizes = map(Packet.getLength, src_trace.packets)
        src_n = len(src_sizes)
        src_i = 0

        while src_i < src_n:
            orig_packet = src_trace.packets[src_i]
            self.add_packet(Packet(orig_packet.getDirection(), orig_packet.getTime(), dst_sizes[dst_i]))
            if src_sizes[src_i] > dst_sizes[dst_i]:
                remaining = dst_sizes[dst_i] - src_sizes[src_i]
                src_i += 1
                while remaining > 0:
                    dst_i += 1
                    orig_packet = src_trace.packets[src_i]
                    self.add_packet(Packet(orig_packet.getDirection(), orig_packet.getTime(), dst_sizes[dst_i]))
                    src_i += 1
                    remaining -= dst_sizes[dst_i]

    def get_target_cluster(self):
        website_id = 1  # self.trace.getId().?
        return self.get_website_cluster(website_id)

    @classmethod
    def get_website_cluster(cls, website_id):
        return website_clusters.get(website_id, 1)

    @classmethod
    def initialize(cls):
        load_website_clusters()
