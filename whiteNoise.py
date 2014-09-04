from Queue import Queue
from random import random
from pyaudio import paInt16
from pyAudioPlayer import AudioPlayer

class DataCollector:
    '''
    Generate white noise
    '''

    def __init__(self, info, queueSize=5):
        # connect FIFO queues
        self.queueOut = Queue(queueSize)
        self.CS = info["CHUNK_SIZE"]

    def start(self):
        # read/write from queue
        while True:
            channels = []
            for i in range(2):
                nums = []
                for j in range(self.CS):
                    n = random()
                    nums.append(n)
                channels.append(nums)
            self.queueOut.put( channels )

if __name__ == "__main__":

    info = { "CHUNK_SIZE" : 1024,
             "FORMAT"     : paInt16,
             "RATE"       : 44100,
             "CHANNELS"   : 2 }

    dc = DataCollector (info, 1)
    ap = AudioPlayer (dc, info)

    raw_input("Please turn your speaker volume down.\nPress enter to continue...")
    ap.start()