from Queue import Queue
from threading import Thread
from random import random

class DataCollector:


    def __init__(queueSize=1000):
        # connect FIFO queues
        self.queueOut    = Queue(queueSize)

    def start():
        # read/write from queue
        while True:
            n = random()
            self.queueOut.put( n )

'''
dc = DataProcessor(stuff,344)
dc.start()
dc.queueOut
'''