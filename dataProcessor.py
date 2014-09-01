class DataProcessor:
    def __init__(outputQueue, dataCollector):
        # connect FIFO queues
        self.queueOut = outputQueue
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
