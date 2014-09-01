from Queue import Queue
from threading import Thread
from random import random
from array import array
from struct import pack
import pyaudio

#########################################################

class DataCollector:

    def __init__(self, queueSize=1000):
        # connect FIFO queues
        self.queueOut = Queue(queueSize)

    def start(self):
        # read/write from queue
        while True:
            chan = []
            for i in range(2):
                nums = []
                for j in range(100):
                    n = random()
                    nums.append(n)
                chan.append(nums)
            self.queueOut.put( chan )

#########################################################

class DataProcessor:
    '''
    Consumption and Production are controlled through Queues.
    
    Consumes a 2D array in which each row is a list of floats between 0 and 1.
    Each row represents one channel of audio data, and each float represents
    an amplitude.

    Produces a 2D array in which each float in the input is mapped to an integer
    between -32767 and 32767.
    '''

    def __init__(self, dataCollector, queueSize=1000):
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
            buf = self.queueIn.get()
            result = self.process( buf )
            self.queueOut.put( result )


    def process(self, data):
        result = []
        for row in data:
            newrow = []
            for num in row:
                # convert to amp between 0 and 10000 hz
                a = int(num*10000)
                newrow.append(a)    
            result.append(newrow)
        return result

#########################################################

class AudioWriter:
    '''
    Consumption and Production are controlled through Queues.

    Consumes a 2D array in which each row represents one channel of audio data.
    Each channel is composed of a list of amplitudes (intergers between
    -32767 and 32767).

    Produces an array of writable audio chunks.
    '''

    CHUNK_SIZE = 1024
    FORMAT = pyaudio.paInt16
    RATE = 41000
    CHANNELS = 1

    def __init__(self, dataProcessor, queueSize=1000):
        # connect FIFO queues
        self.queueOut    = Queue(queueSize)
        self.dp          = dataProcessor
        self.queueIn     = dataProcessor.queueOut
        self.childThread = Thread(target=self.dp.start)

    def start(self):
        # start data processor
        self.childThread.start()
        # read/write from queue
        while True:
            buf = self.queueIn.get()
            result = self.process( buf )
            self.queueOut.put( result )

    def process(self, buf):
        output = []

        for channel in buf:
            chunk = array('h')

            for amp in channel:
                # Check for Clips
                if int(amp) < -32767:
                    amp = -32767
                    print("clip at "+str(i))

                elif int(amp) > 32767:
                    amp = 32767
                    print("clip at "+str(i))

                # write to chunk
                chunk.append(amp)

            # Converts to bitstream for chunk
            chunk = pack('<' + ('h'*len(chunk)), *chunk)
            output.append(chunk)

        return output

#########################################################

class AudioPlayer:
    '''
    Consumption is controlled through Queues.

    Consumes a list of audio channels, where each channel is ready
    to be directly written to the pyaudio engine and played back
    through the default audio device.
    '''

    def __init__(self, audioWriter):
        # connect FIFO queues
        self.aw          = audioWriter
        self.queueIn     = audioWriter.queueOut
        self.childThread = Thread(target=self.aw.start)
        # start audio devices
        self.audioDevice = pyaudio.PyAudio()
        self.stream = self.audioDevice.open( \
            format=self.aw.FORMAT,
            channels=self.aw.CHANNELS,
            rate=self.aw.RATE,
            output=True,
            frames_per_buffer=self.aw.CHUNK_SIZE)

    def start(self):
        # start audio writer
        self.childThread.start()
        # read from queue and play
        while True:
            channels = self.queueIn.get()
            for chunk in channels:
                self.stream.write(chunk)

#########################################################

def autostart():
    dc = DataCollector()
    dp = DataProcessor(dc)
    aw = AudioWriter(dp)
    ap = AudioPlayer(aw)

    ap.start()