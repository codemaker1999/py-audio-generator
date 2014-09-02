### **Generate Audio using Python**

The purpose of this project is to create a modular interface for collecting data from any source, processing it into audio data, and playing it back through the default playback device.

##### **Data Flow**

The flow of data through the system is as follows:

* a DataCollector object reads or generates data from arbitrary sources and returns a chunk of data (a 2D array in which each row is a list of floating point values between 0 and 1, representing one channel of audio data)

* a DataProcessor object reads consumes this chunk of data, processes it, and returns a newly formatted chunk (a 2D array in which each row is a list of intergers between -32767 and 32767. Again, each row is one channel of audio data)

* an AudioWriter object consumes this new chunk and converts each row into an object that the AudioPlayer can directly consume and play

* an AudioPlayer object consumes this formatted chunk and plays it back through the default audio device on the system

##### **Implementation Details**

* each object is run in it's own thread and queues output data in FIFO pipes for the proceeding step

* current implementation uses PyAudio, the Python bindings for PortAudio, for audio playback