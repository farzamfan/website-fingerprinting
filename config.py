# This is a Python framework to compliment "Peek-a-Boo, I Still See You: Why Efficient Traffic Analysis Countermeasures Fail".
# Copyright (C) 2012  Kevin P. Dyer (kpdyer.com)
# See LICENSE for more details.

import os
import sys
from Packet import Packet

# Set the following to a directory that contains
# * weka-X-Y-Z (see WEKA_ROOT to change the weka version)
# * pcap-logs (a diretory that contains all of the LL pcap files)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Enviromental settings
JVM_MEMORY_SIZE = '4192m'

WEKA_ROOT          = os.path.join(BASE_DIR, 'weka')
WEKA_JAR           = os.path.join(WEKA_ROOT  ,'weka.jar')
PCAP_ROOT          = os.path.join(BASE_DIR   ,'pcap-logs')
CACHE_DIR          = './cache'
COUNTERMEASURE_DIR = './countermeasures'
CLASSIFIERS_DIR    = './classifiers'
OUTPUT_DIR         = './output'

#Specify options for Herrmann MySQL database
MYSQL_HOST = 'localhost'
MYSQL_DB = 'fingerprints'
MYSQL_USER = 'fingerprints'
MYSQL_PASSWD = 'fingerprints'

sys.path.append(COUNTERMEASURE_DIR)
sys.path.append(CLASSIFIERS_DIR)

COUNTERMEASURE      = 0
CLASSIFIER          = 0
BUCKET_SIZE         = 2
DATA_SOURCE         = 1
NUM_TRAINING_TRACES = 16
NUM_TESTING_TRACES  = 4
NUM_TRIALS          = 1
TOP_N               = 775
PACKET_PENALTY      = 68
IGNORE_ACK          = True

# Liberatore and Levine Training and Testing configuration
DATA_SET = [
#{'month':2,'day':10,'hour':13},
#{'month':2,'day':11,'hour':11},
#{'month':2,'day':13,'hour':8},
#{'month':2,'day':13,'hour':19},
#{'month':2,'day':14,'hour':9},
#{'month':2,'day':14,'hour':23},
#{'month':2,'day':15,'hour':8},
#{'month':2,'day':16,'hour':12},
#{'month':2,'day':20,'hour':10},
#{'month':2,'day':20,'hour':16},
#{'month':2,'day':20,'hour':22},
#{'month':2,'day':21,'hour':4},
#{'month':2,'day':21,'hour':10},
#{'month':2,'day':21,'hour':16},
#{'month':2,'day':21,'hour':22},
#{'month':2,'day':22,'hour':4},
#{'month':2,'day':22,'hour':10},
#{'month':2,'day':22,'hour':16},
#{'month':2,'day':22,'hour':22},
#{'month':2,'day':23,'hour':4},
#{'month':2,'day':23,'hour':10},
#{'month':2,'day':20,'hour':10},
#{'month':2,'day':20,'hour':16},
#{'month':2,'day':20,'hour':22},
#{'month':2,'day':21,'hour':4},
#{'month':2,'day':21,'hour':10},
#{'month':2,'day':21,'hour':16},
#{'month':2,'day':21,'hour':22},
#{'month':2,'day':22,'hour':4},
#{'month':2,'day':22,'hour':10},
#{'month':2,'day':22,'hour':16},
#{'month':2,'day':22,'hour':22},
#{'month':2,'day':23,'hour':4},
#{'month':2,'day':23,'hour':10},
{'month':3,'day':6,'hour':16},
{'month':3,'day':6,'hour':22},
{'month':3,'day':7,'hour':4},
{'month':3,'day':7,'hour':10},
{'month':3,'day':7,'hour':16},
{'month':3,'day':7,'hour':22},
{'month':3,'day':8,'hour':4},
{'month':3,'day':8,'hour':10},
{'month':3,'day':8,'hour':16},
{'month':3,'day':8,'hour':22},
{'month':3,'day':9,'hour':4},
{'month':3,'day':9,'hour':16},
{'month':3,'day':9,'hour':22},
{'month':3,'day':10,'hour':4},
{'month':3,'day':10,'hour':10},
{'month':3,'day':10,'hour':16},
{'month':3,'day':10,'hour':22},
{'month':3,'day':11,'hour':4},
{'month':3,'day':11,'hour':10},
{'month':3,'day':11,'hour':16},
{'month':3,'day':11,'hour':22},
{'month':3,'day':12,'hour':4},
{'month':3,'day':12,'hour':10},
{'month':3,'day':12,'hour':16},
{'month':3,'day':12,'hour':22},
{'month':3,'day':13,'hour':16},
{'month':3,'day':13,'hour':22},
{'month':3,'day':14,'hour':4},
{'month':3,'day':14,'hour':10},
{'month':3,'day':14,'hour':16},
{'month':3,'day':14,'hour':22},
{'month':3,'day':15,'hour':4},
{'month':3,'day':15,'hour':10},
{'month':3,'day':15,'hour':16},
{'month':3,'day':15,'hour':22},
{'month':3,'day':16,'hour':4},
{'month':3,'day':16,'hour':10},
{'month':3,'day':16,'hour':16},
{'month':3,'day':16,'hour':22},
{'month':3,'day':17,'hour':4},
{'month':3,'day':17,'hour':10},
{'month':3,'day':17,'hour':16},
{'month':3,'day':17,'hour':22},
{'month':3,'day':20,'hour':10},
{'month':3,'day':20,'hour':16},
{'month':3,'day':20,'hour':22},
{'month':3,'day':21,'hour':4},
{'month':3,'day':21,'hour':10},
{'month':3,'day':21,'hour':16},
{'month':3,'day':21,'hour':22},
{'month':3,'day':22,'hour':4},
{'month':3,'day':22,'hour':10},
{'month':3,'day':22,'hour':16},
{'month':3,'day':22,'hour':22},
{'month':3,'day':23,'hour':4},
{'month':3,'day':23,'hour':10},
{'month':3,'day':23,'hour':16},
{'month':3,'day':23,'hour':22},
{'month':3,'day':24,'hour':10},
{'month':3,'day':24,'hour':16},
{'month':3,'day':24,'hour':22},
{'month':3,'day':25,'hour':4},
{'month':3,'day':25,'hour':10},
{'month':3,'day':25,'hour':16},
{'month':3,'day':25,'hour':22},
{'month':3,'day':26,'hour':4},
{'month':3,'day':26,'hour':10},
{'month':3,'day':26,'hour':16},
{'month':3,'day':26,'hour':22},
{'month':3,'day':27,'hour':4},
{'month':3,'day':27,'hour':10},
{'month':3,'day':27,'hour':16},
{'month':3,'day':28,'hour':16},
{'month':3,'day':28,'hour':22},
{'month':3,'day':29,'hour':4},
{'month':3,'day':29,'hour':10},
{'month':3,'day':29,'hour':16},
{'month':3,'day':29,'hour':22},
{'month':3,'day':30,'hour':4},
{'month':3,'day':30,'hour':10},
{'month':3,'day':30,'hour':16},
{'month':3,'day':30,'hour':22},
{'month':3,'day':31,'hour':4},
{'month':3,'day':31,'hour':10},
{'month':3,'day':31,'hour':16},
{'month':3,'day':31,'hour':22},
{'month':4,'day':1,'hour':4},
{'month':4,'day':1,'hour':10},
{'month':4,'day':1,'hour':16},
{'month':4,'day':1,'hour':22},
{'month':4,'day':2,'hour':4},
{'month':4,'day':2,'hour':10},
{'month':4,'day':2,'hour':16},
{'month':4,'day':2,'hour':22},
{'month':4,'day':3,'hour':4},
{'month':4,'day':3,'hour':10},
{'month':4,'day':3,'hour':16},
{'month':4,'day':3,'hour':22},
{'month':4,'day':4,'hour':4},
{'month':4,'day':4,'hour':10},
{'month':4,'day':4,'hour':16},
{'month':4,'day':4,'hour':22},
{'month':4,'day':5,'hour':4},
{'month':4,'day':5,'hour':10},
{'month':4,'day':5,'hour':16},
{'month':4,'day':5,'hour':22},
{'month':4,'day':6,'hour':4},
{'month':4,'day':6,'hour':10},
{'month':4,'day':6,'hour':16},
{'month':4,'day':6,'hour':22},
{'month':4,'day':7,'hour':4},
{'month':4,'day':7,'hour':10},
{'month':4,'day':7,'hour':16},
{'month':4,'day':7,'hour':22},
{'month':4,'day':8,'hour':4},
{'month':4,'day':8,'hour':10},
{'month':4,'day':8,'hour':16},
#{'month':4,'day':13,'hour':22},
#{'month':4,'day':14,'hour':4},
#{'month':4,'day':14,'hour':10},
#{'month':4,'day':14,'hour':16},
#{'month':4,'day':14,'hour':22},
#{'month':4,'day':15,'hour':4},
#{'month':4,'day':15,'hour':10},
#{'month':4,'day':15,'hour':16},
#{'month':4,'day':15,'hour':22},
#{'month':4,'day':16,'hour':4},
#{'month':4,'day':16,'hour':16},
#{'month':4,'day':16,'hour':22},
#{'month':4,'day':18,'hour':16},
#{'month':4,'day':18,'hour':22},
#{'month':4,'day':19,'hour':4},
#{'month':4,'day':19,'hour':10},
#{'month':4,'day':19,'hour':16},
#{'month':4,'day':19,'hour':22},
#{'month':4,'day':20,'hour':4},
#{'month':4,'day':20,'hour':10},
#{'month':4,'day':20,'hour':16},
#{'month':4,'day':20,'hour':22},
#{'month':4,'day':21,'hour':4},
#{'month':4,'day':21,'hour':10},
#{'month':4,'day':21,'hour':16},
#{'month':4,'day':21,'hour':22},
#{'month':4,'day':22,'hour':4},
#{'month':4,'day':22,'hour':16},
#{'month':4,'day':22,'hour':22},
#{'month':4,'day':23,'hour':4},
#{'month':4,'day':23,'hour':10},
#{'month':4,'day':23,'hour':16},
#{'month':4,'day':23,'hour':22},
#{'month':4,'day':24,'hour':4},
#{'month':4,'day':24,'hour':16},
#{'month':4,'day':24,'hour':22},
]

# packet range (LL)
PACKET_RANGE = range(Packet.HEADER_LENGTH,Packet.MTU+1,8)
PACKET_RANGE2 = range(Packet.HEADER_LENGTH,Packet.MTU+1,4)

# packet range (H)


# Countermeasures
from PadToMTU import PadToMTU
from PadRFCFixed import PadRFCFixed
from PadRFCRand import PadRFCRand
from PadRand import PadRand
from PadRoundExponential import PadRoundExponential
from PadRoundLinear import PadRoundLinear
from MiceElephants import MiceElephants
from DirectTargetSampling import DirectTargetSampling
from WrightStyleMorphing import WrightStyleMorphing


available_countermeasures = [
    None,
    PadToMTU,
    PadRFCFixed,
    PadRFCRand,
    PadRand,
    PadRoundExponential,
    PadRoundLinear,
    MiceElephants,
    DirectTargetSampling,
    WrightStyleMorphing,
]


# Classifier enum
LIBERATORE_CLASSIFIER    = 0
WRIGHT_CLASSIFIER        = 1
JACCARD_CLASSIFIER       = 2
PANCHENKO_CLASSIFIER     = 3
BANDWIDTH_CLASSIFIER     = 4
ESORICS_CLASSIFIER       = 5
HERRMANN_CLASSIFIER      = 6
TIME_CLASSIFIER          = 10
VNG_CLASSIFIER           = 14
VNG_PLUS_PLUS_CLASSIFIER = 15


def sanity():
    if not os.path.exists(WEKA_JAR):
        print 'Weka does not exist in path: '+str(WEKA_JAR)
        print 'Please install Weka properly.'
        sys.exit(1)

sanity()
