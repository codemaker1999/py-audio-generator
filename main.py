from DefaultComponents import DataProcessor, AudioWriter, AudioPlayer
from random import random
from Queue import Queue
from threading import Thread
from math import sin, pi
import pyaudio

info = { "CHUNK_SIZE" : 1024,
         "FORMAT"     : pyaudio.paInt16,
         "RATE"       : 44100,
         "CHANNELS"   : 2 }

# custom data collector

class DataCollector:
    def __init__(self, info, queueSize=1000):
        # connect FIFO queues
        self.queueOut = Queue(queueSize)

    def start(self):
        # unpack
        CHUNK_SIZE = info["CHUNK_SIZE"]
        RATE       = info["RATE"]
        CHANNELS   = info["CHANNELS"]
        m = 0
        freq = 400 # Hz
        # read/write from queues
        while True:
            chans = []
            for i in range(CHANNELS):
                nums = []
                # r = random()
                for j in range(CHUNK_SIZE):
                    # play a tone of <freq> Hertz
                    n = 0.5*(1 + sin(m*freq/float(RATE)))
                    nums.append(n)
                    m += 1
                chans.append(nums)
            self.queueOut.put( chans )

# custom data processor

class DataProcessor:
    '''
    Consumption and Production are controlled through Queues.
    
    Consumes a 2D array in which each row is a list of floats between 0 and 1.
    Each row represents one channel of audio data, and each float represents
    an amplitude.

    Produces a 2D array in which each float in the input is mapped to an integer
    between -32767 and 32767.
    '''

    def __init__(self, dataCollector, info, queueSize=1000):
        # connect FIFO queues
        self.queueOut    = Queue(queueSize)
        self.dc          = dataCollector
        self.queueIn     = dataCollector.queueOut
        self.childThread = Thread(target=self.dc.start)

    def start(self):
        # start data collection
        self.childThread.start()
        # read/write from queue
        while True:
            channels = self.queueIn.get()
            output = self.process( channels )
            self.queueOut.put( output )


    def process(self, channels):
        output = []
        for chan in channels:
            newchan = []
            for num in chan:
                a = int(2*(num-0.5)*32760)
                newchan.append(a)    
            output.append(newchan)
        return output

# link objects and run

dc = DataCollector (info)
dp = DataProcessor (dc, info)
aw = AudioWriter   (dp, info)
ap = AudioPlayer   (aw, info)
print 'starting...'
ap.start()