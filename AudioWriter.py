from Queue import Queue
from threading import Thread
from array import array
from struct import pack
import audioWriter

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

    def __init__(dataProcessor, queueSize=1000):
        # connect FIFO queues
        self.queueOut    = Queue(queueSize)
        self.dp          = dataProcessor
        self.queueIn     = dataProcessor.queueOut
        self.childThread = Thread(target=self.dp.start)

    def start():
        # start data processor
        self.childThread.start()
        # read/write from queue
        while True:
            buf = self.queueIn.get()
            result = self.process( buf )
            self.queueOut.put( result )

    def process(buf):
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
