from pyAudioPlayer import AudioPlayer
from random import random
from Queue import Queue, Empty
from threading import Thread
from math import sin, pi
import pyaudio

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
                nums = []
                for j in range(CHUNK_SIZE):
                    # play a tone of <freq> Hertz
                    n = 0.5*(1 + sin(m*freq/float(RATE)))
                    nums.append(n)
                    m += 1
                chans.append(nums)
            self.queueOut.put( chans )

if __name__ == "__main__":

    info = { "CHUNK_SIZE" : 1024,
             "FORMAT"     : pyaudio.paInt16,
             "RATE"       : 44100,
             "CHANNELS"   : 2 }

    # link objects and run
    ctrl = Controller (1)
    dc   = DataCollector (ctrl, info, 1)
    ap   = AudioPlayer (dc, info)

    ap.start()