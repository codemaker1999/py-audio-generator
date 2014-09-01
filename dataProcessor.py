from Queue import Queue

class DataProcessor:
    def __init__(dataCollector, queueSize=1000):
        # connect FIFO queues
        self.queueOut = Queue(queueSize)
        self.dc       = dataCollector
        self.queueIn  = dataCollector.queueOut
        # start data collection
        dc.start()

    def start():
        while True:
            chunk = self.queueIn.get()
            result = self.process( chunk )
            self.queueOut.put( result )

    def process(chunk):
        pass