from DefaultComponents import DataProcessor, AudioWriter, AudioPlayer
from random import random
from Queue import Queue
from math import sin, pi

# custom data collector

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
                r = random()
                for j in range(10000):
                    n = r*0.5*(1 + sin(2*pi*j/1000.0))
                    # TICK TOCK NOISE # n = random() if j%1000==0 else 0
                    nums.append(n)
                chan.append(nums)
            self.queueOut.put( chan )

# link objects and run

dc = DataCollector()
dp = DataProcessor(dc)
aw = AudioWriter(dp)
ap = AudioPlayer(aw)

ap.start()