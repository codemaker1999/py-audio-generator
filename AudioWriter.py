from Queue import Queue

class AudioWriter:
    def __init__(dataProcessor, queueSize=1000):
        # connect FIFO queues
        self.queueOut = Queue(queueSize)
        self.dp       = dataProcessor
        self.queueIn  = dataProcessor.queueOut
        # start data processor
        dp.start()

    def start():
        while True:
            chunk = self.queueIn.get()
            result = self.process( chunk )
            self.queueOut.put( result )

    def process(chunk):
        pass
