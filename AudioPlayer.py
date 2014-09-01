from Queue import Queue
from threading import Thread
import pyaudio

class AudioPlayer:
    '''
    Consumption is controlled through Queues.

    Consumes a list of audio channels, where each channel is ready
    to be directly written to the pyaudio engine and played back
    through the default audio device.
    '''

    def __init__(audioWriter):
        # connect FIFO queues
        self.aw          = audioWriter
        self.queueIn     = audioWriter.queueOut
        self.childThread = Thread(target=self.aw.start)
        # start audio devices
        self.audioDevice = pyaudio.PyAudio()
        self.stream = self.audioDevice.open( \
            format=self.aw.FORMAT,
            channels=self.aw.CHANNELS,
            rate=self.aw.RATE,
            output=True,
            frames_per_buffer=self.aw.CHUNK_SIZE)

    def start():
        # start audio writer
        self.childThread.start()
        # read from queue and play
        while True:
            channels = self.queueIn.get()
            for chunk in channels
                self.stream.write(chunk)
