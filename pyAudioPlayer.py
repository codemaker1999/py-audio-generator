from threading import Thread
from array import array
from struct import pack
import pyaudio

class AudioPlayer:
    '''
    Consumes a 2D array in which each row is a list of floats between 0 and 1.
    Each row represents one channel of audio data, and each float represents
    an amplitude.

    Map this data to a 2D array in which each float in the input is mapped to
    an integer between -32767 and 32767.

    Pack this data into an optimized array.

    Play data using the PyAudio API
    '''

    def __init__(self, dataCollector, info):
        # connect FIFO queues
        self.dc          = dataCollector
        self.queueIn     = dataCollector.queueOut
        # start audio devices
        self.audioDevice = pyaudio.PyAudio()
        self.stream = self.audioDevice.open( \
            format=info["FORMAT"],
            channels=info["CHANNELS"],
            rate=info["RATE"],
            output=True,
            frames_per_buffer=info["CHUNK_SIZE"])

    def start(self):
        # start data collection
        collectionThread = Thread(target=self.dc.start)
        collectionThread.start()
        # read from queue
        while True:
            channels = self.queueIn.get()
            output = self.process( channels )
            self.play( output )


    def process(self, channels):
        output = []
        for chan in channels:
            newchan = []
            for num in chan:
                # convert to amp between -32766 and 32766
                a = int(((2*num)-1)*32766)
                newchan.append(a)    
            output.append(newchan)
        return self.packChannels( output )

    def packChannels(self, channels):
        output = []

        for chan in channels:
            chunk = array('h') # efficient array

            for amp in chan:
                # Check for clipping
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

    def play(self, channels):
        for chunk in channels:
            self.stream.write(chunk)
