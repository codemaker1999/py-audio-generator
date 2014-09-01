from Queue import Queue
from threading import Thread
from random import random

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
