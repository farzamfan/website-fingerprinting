# This is a Python framework to compliment "Peek-a-Boo, I Still See You: Why Efficient Traffic Analysis Countermeasures Fail".
# Copyright (C) 2012  Kevin P. Dyer (kpdyer.com)
# See LICENSE for more details.
from __future__ import print_function

import sys
import time
import os
import random
import getopt
import string
import itertools

import config


# custom
from Datastore import Datastore

from DirectTargetSampling import DirectTargetSampling
from WrightStyleMorphing import WrightStyleMorphing

# classifiers
from LiberatoreClassifier import LiberatoreClassifier
from WrightClassifier import WrightClassifier
from BandwidthClassifier import BandwidthClassifier
from HerrmannClassifier import HerrmannClassifier
from TimeClassifier import TimeClassifier
from PanchenkoClassifier import PanchenkoClassifier
from VNGPlusPlusClassifier import VNGPlusPlusClassifier
from VNGClassifier import VNGClassifier
from JaccardClassifier import JaccardClassifier
from ESORICSClassifier import ESORICSClassifier
from countermeasure import CounterMeasure


def intToCountermeasure(n):
    try:
        return config.get_available_countermeasures()[n]
    except KeyError:
        print('[Error] Invalid countermeasure id: {}'.format(n))
        sys.exit(3)


def intToClassifier(n):
    classifier = None
    if n == config.LIBERATORE_CLASSIFIER:
        classifier = LiberatoreClassifier
    elif n == config.WRIGHT_CLASSIFIER:
        classifier = WrightClassifier
    elif n == config.BANDWIDTH_CLASSIFIER:
        classifier = BandwidthClassifier
    elif n == config.HERRMANN_CLASSIFIER:
        classifier = HerrmannClassifier
    elif n == config.TIME_CLASSIFIER:
        classifier = TimeClassifier
    elif n == config.PANCHENKO_CLASSIFIER:
        classifier = PanchenkoClassifier
    elif n == config.VNG_PLUS_PLUS_CLASSIFIER:
        classifier = VNGPlusPlusClassifier
    elif n == config.VNG_CLASSIFIER:
        classifier = VNGClassifier
    elif n == config.JACCARD_CLASSIFIER:
        classifier = JaccardClassifier
    elif n == config.ESORICS_CLASSIFIER:
        classifier = ESORICSClassifier

    return classifier

def usage():
    print("""
    -N [int] : use [int] websites from the dataset
               from which we will use to sample a privacy
               set k in each experiment (default 775)

    -k [int] : the size of the privacy set (default 2)

    -d [int]: dataset to use
        0: Liberatore and Levine Dataset (OpenSSH)
        1: Herrmann et al. Dataset (OpenSSH)
        2: Herrmann et al. Dataset (Tor)
        (default 1)

    -C [int] : classifier to run
        0: Liberatore Classifer
        1: Wright et al. Classifier
        2: Jaccard Classifier
        3: Panchenko et al. Classifier
        5: Lu et al. Edit Distance Classifier
        6: Herrmann et al. Classifier
        4: Dyer et al. Bandwidth (BW) Classifier
        10: Dyer et al. Time Classifier
        14: Dyer et al. Variable n-gram (VNG) Classifier
        15: Dyer et al. VNG++ Classifier
        (default 0)

    -c [int]: countermeasure to use
        0: None (default)
        1: Pad to MTU
        2: Session Random 255
        3: Packet Random 255
        4: Pad Random MTU
        5: Exponential Pad
        6: Linear Pad
        7: Mice-Elephants Pad
        8: Direct Target Sampling
        9: Traffic Morphing
        10: BuFLO
        11: Tamaraw

    -n [int]: number of trials to run per experiment (default 1)

    -t [int]: number of training traces to use per experiment (default 16)

    -T [int]: number of testing traces to use per experiment (default 4)
    """)


def info(*args):
    print('[INFO]', *args)


def error(*args, **kwargs):
    ex = kwargs.pop('exit', None)
    print('[ERROR]', *args)
    if ex is not None:
        sys.exit(ex)


def run():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:T:N:k:c:C:d:n:r:h")
    except getopt.GetoptError, err:
        print(str(err))  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    char_set = string.ascii_lowercase + string.digits
    runID = ''.join(random.sample(char_set,8))

    for o, a in opts:
        if o in ("-k"):
            config.BUCKET_SIZE = int(a)
        elif o in ("-C"):
            config.CLASSIFIER = int(a)
        elif o in ("-d"):
            config.DATA_SOURCE = int(a)
        elif o in ("-c"):
            config.COUNTERMEASURE = int(a)
        elif o in ("-N"):
            config.TOP_N = int(a)
        elif o in ("-t"):
            config.NUM_TRAINING_TRACES = int(a)
        elif o in ("-T"):
            config.NUM_TESTING_TRACES = int(a)
        elif o in ("-n"):
            config.NUM_TRIALS = int(a)
        elif o in ("-r"):
            runID = str(a)
        else:
            usage()
            sys.exit(2)

    outputFilenameArray = ['results',
                           'k'+str(config.BUCKET_SIZE),
                           'c'+str(config.COUNTERMEASURE),
                           'd'+str(config.DATA_SOURCE),
                           'C'+str(config.CLASSIFIER),
                           'N'+str(config.TOP_N),
                           't'+str(config.NUM_TRAINING_TRACES),
                           'T'+str(config.NUM_TESTING_TRACES),
                          ]
    outputFilename = os.path.join(config.OUTPUT_DIR,'.'.join(outputFilenameArray))

    if not os.path.exists(config.CACHE_DIR):
        os.mkdir(config.CACHE_DIR)

    if not os.path.exists(outputFilename+'.output'):
        banner = ['accuracy','overhead','timeElapsedTotal','timeElapsedClassifier']
        f = open( outputFilename+'.output', 'w' )
        f.write(','.join(banner))
        f.close()
    if not os.path.exists(outputFilename+'.debug'):
        f = open( outputFilename+'.debug', 'w' )
        f.close()

    # Dataset Selection
    dataset_size = 0
    training_set_size = config.NUM_TRAINING_TRACES
    testing_set_size = config.NUM_TESTING_TRACES
    if config.DATA_SOURCE == 0:
        dataset_size = len(config.DATA_SET)
        startIndex = config.NUM_TRAINING_TRACES
        endIndex   = len(config.DATA_SET)-config.NUM_TESTING_TRACES
    elif config.DATA_SOURCE == 1:
        dataset_size = 160
        maxTracesPerWebsiteH = 160
        startIndex = config.NUM_TRAINING_TRACES
        endIndex   = maxTracesPerWebsiteH-config.NUM_TESTING_TRACES
    elif config.DATA_SOURCE == 2:
        dataset_size = 18
        maxTracesPerWebsiteH = 18
        startIndex = config.NUM_TRAINING_TRACES
        endIndex   = maxTracesPerWebsiteH-config.NUM_TESTING_TRACES
    else:
        error('Invalid data-source id:', config.DATA_SOURCE)
        return 3

    # Checking Training-set and Test-set Sizes
    info('|dataset|={}\t|training-set|={}, |testing-set|={}'.format(dataset_size, training_set_size, testing_set_size))
    if training_set_size + testing_set_size > dataset_size:
        print('[ERROR] t+T is larger than dataset size!')
        print('\tThe dataset is devided into two parts: Training set (t) and Testing set (T), so t+T must be ')
        print('\tless than or equal to the total number of data in dataset.')
        sys.exit(4)

    # Run
    for run_index in range(config.NUM_TRIALS):
        run_start_time = time.time()
        print('Run #{}'.format(run_index))

        # Select a sample of size k from websites 1..N
        webpageIds = range(0, config.TOP_N - 1)
        random.shuffle(webpageIds)
        webpageIds = webpageIds[0:config.BUCKET_SIZE]
        seed = random.randint(startIndex, endIndex)

        trainingSet = []
        testingSet = []
        targetWebpage = None

        classifier = intToClassifier(config.CLASSIFIER)
        countermeasure = intToCountermeasure(config.COUNTERMEASURE)
        if issubclass(countermeasure, CounterMeasure):
            countermeasure = countermeasure()   # also instantiating
            new_style_cm = True
        else:
            new_style_cm = False
        preCountermeasureOverhead = 0
        postCountermeasureOverhead = 0

        for webpageId in webpageIds:
            print('.', end='')
            sys.stdout.flush()

            # Sampling From Data-source
            if config.DATA_SOURCE == 0:
                webpageTrain = Datastore.getWebpagesLL( [webpageId], seed-config.NUM_TRAINING_TRACES, seed )
                webpageTest = Datastore.getWebpagesLL( [webpageId], seed, seed+config.NUM_TESTING_TRACES )
            elif config.DATA_SOURCE in [1, 2]:
                webpageTrain = Datastore.getWebpagesHerrmann( [webpageId], seed-config.NUM_TRAINING_TRACES, seed )
                webpageTest = Datastore.getWebpagesHerrmann( [webpageId], seed, seed+config.NUM_TESTING_TRACES )
            else:
                error('Invalid datasource id:', config.DATA_SOURCE)
                return 3

            # Selecting Targets
            webpageTrain = webpageTrain[0]
            webpageTest = webpageTest[0]
            if targetWebpage is None:
                targetWebpage = webpageTrain

            # Accounting
            preCountermeasureOverhead += webpageTrain.getBandwidth()
            preCountermeasureOverhead += webpageTest.getBandwidth()

            # Train Countermeasure
            metadata = None
            if new_style_cm:
                countermeasure.train(src_page=webpageTrain, target_page=targetWebpage)
            else:
                if countermeasure in [DirectTargetSampling, WrightStyleMorphing]:
                    metadata = countermeasure.buildMetadata(webpageTrain, targetWebpage)

            # Applying Countermeasure (and feeding data to classifier)
            for i, w in enumerate([webpageTrain, webpageTest]):
                for trace in w.getTraces():
                    if countermeasure:
                        if new_style_cm:
                            traceWithCountermeasure = countermeasure.apply_to_trace(trace)
                        else:
                            if countermeasure in [DirectTargetSampling, WrightStyleMorphing]:
                                if w.getId() != targetWebpage.getId():
                                    traceWithCountermeasure = countermeasure.applyCountermeasure(trace,  metadata)
                                else:
                                    traceWithCountermeasure = trace
                            else:
                                traceWithCountermeasure = countermeasure.applyCountermeasure(trace)
                    else:
                        traceWithCountermeasure = trace

                    # Overhead Accounging
                    postCountermeasureOverhead += traceWithCountermeasure.getBandwidth()

                    instance = classifier.traceToInstance( traceWithCountermeasure )
                    if instance:
                        if i == 0:     # train-page
                            trainingSet.append(instance)
                        elif i == 1:   # test-page
                            testingSet.append(instance)

        # Classification
        print('')
        classification_start_time = time.time()
        [accuracy, debugInfo] = classifier.classify(runID, trainingSet, testingSet)
        run_end_time = time.time()

        # Write Output
        overhead = '{}/{}'.format(postCountermeasureOverhead, preCountermeasureOverhead)
        overhead_ratio = ((postCountermeasureOverhead * 1.0 / preCountermeasureOverhead) - 1) * 100
        run_total_time = run_end_time - run_start_time
        classification_total_time = run_end_time - classification_start_time
        output = [accuracy, overhead, '%.2f' % run_total_time, '%.2f' % classification_total_time]
        summary = ', '.join(itertools.imap(str, output))
        f = open(outputFilename + '.output', 'a')
        f.write('\n' + summary)
        f.close()

        # Processing Classification Results For Each Page
        sites_detected = []
        sites_not_detected = []
        f = open(outputFilename + '.debug', 'a')
        for entry in debugInfo:
            if entry[0] == entry[1]:
                sites_detected.append(entry[0])
            else:
                sites_not_detected.append(entry[0])
            f.write(entry[0] + ',' + entry[1] + '\n')
        f.close()

        # Show A Brief Report To User
        info('sites detected correctly:\t{}'.format(', '.join(sites_detected)))
        info('sites detected incorrectly:\t{}'.format(', '.join(sites_not_detected)))
        info('summary: {}%, {} bytes ({:.1f}%), {:.1f}s'.format(accuracy, overhead, overhead_ratio, run_total_time))

    return 0


if __name__ == '__main__':
    sys.exit(run() or 0)
