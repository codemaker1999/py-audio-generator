from Queue import Queue
from threading import Thread

class DataProcessor:
    '''
    Consumption and Production are controlled through Queues.
    
    Consumes a 2D array in which each row is a list of floats between 0 and 1.
    Each row represents one channel of audio data, and each float represents
    an amplitude.

    Produces a 2D array in which each float in the input is mapped to an integer
    between -32767 and 32767.
    '''

    def __init__(dataCollector, queueSize=1000):
        # connect FIFO queues
        self.queueOut    = Queue(queueSize)
        self.dc          = dataCollector
        self.queueIn     = dataCollector.queueOut
        self.childThread = Thread(target=self.dc.start)

    def start():
        # start data collection
        self.childThread.start()
        # read/write from queue
        while True:
            buf = self.queueIn.get()
            result = self.process( buf )
            self.queueOut.put( result )

    def process(buf):
        pass
