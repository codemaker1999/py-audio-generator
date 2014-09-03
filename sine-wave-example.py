from DefaultComponents import DataProcessor, AudioWriter, AudioPlayer
from random import random
from Queue import Queue, Empty
from threading import Thread
from math import sin, pi
import pyaudio

info = { "CHUNK_SIZE" : 1024,
         "FORMAT"     : pyaudio.paInt16,
         "RATE"       : 44100,
         "CHANNELS"   : 2 }

# controller class

class BassController:
    def __init__(self, queueSize=5):
        # connect FIFO queues
        self.queueOut = Queue(queueSize)

    def start(self):
        while True:
            f = raw_input("Enter frequency value in Hz\n")
            try:
                f = int(f)
                self.queueOut.put(f)
            except Exception as e:
                pass

# controller class

class Controller:
    def __init__(self, queueSize=5):
        # connect FIFO queues
        self.queueOut = Queue(queueSize)

    def start(self):
        while True:
            f = raw_input("Enter frequency value in Hz\n")
            try:
                f = int(f)
                self.queueOut.put(f)
            except Exception as e:
                pass

# custom data collector

class DataCollector:
    def __init__(self, controller, info, queueSize=5):
        # connect FIFO queues
        self.queueOut = Queue(queueSize)
        self.ctrl = controller
        self.queueIn = self.ctrl.queueOut
        self.childThread = Thread(target=self.ctrl.start)

    def start(self):
        # unpack
        CHUNK_SIZE = info["CHUNK_SIZE"]
        RATE       = info["RATE"]
        CHANNELS   = info["CHANNELS"]
        # sine wave parameter
        m = 0
        # start controller thread and wait for frequency
        self.childThread.start()
        freq = self.queueIn.get()
        # read/write from queues
        while True:
            chans = []
            # check queue, continue loop if queue empty
            try:
                freq = self.queueIn.get_nowait()
                m = 0
            except Empty as e:
                pass
            # build chunk
            for i in range(CHANNELS):
                # DEBUG: offset channels by 50Hz
                f = freq + 50*i
                nums = []
                # r = random()
                for j in range(CHUNK_SIZE):
                    # play a tone of <freq> Hertz
                    n = 0.5*(1 + sin(m*f/float(RATE)))
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

    def __init__(self, dataCollector, info, queueSize=5):
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
ctrl = Controller (1)
dc   = DataCollector (ctrl, info,1)
dp   = DataProcessor (dc, info,1)
aw   = AudioWriter (dp, info,1)
ap   = AudioPlayer (aw, info)

ap.start()