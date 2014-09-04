### **Generate Audio using Python**

The purpose of this project is to create a modular interface for collecting data from any source, processing it into audio data, and playing it back through the default playback device.

##### **How it works**

* A DataCollector object reads or generates data from arbitrary sources and returns a chunk of data (a 2D array in which each row is a list of floating point values between 0 and 1, representing one channel of audio data). This is the part you will likely override.

* The AudioPlayer object consumes this chunk and plays it back through the default audio device on the system

##### **Usage**

Create a DataCollector class and pass it to AudioPlayer on construction. A DataCollector must

* have an instance variable, `queueOut`, that provides a python `Queue.Queue` object from which audio chunks are read.

* a `start()` method that presumably loops indefinitely and adds audio chunks to the queue

An audio chunk is a 2D array, where each row is a channel of raw audio data represented as a list of floating point numbers (amplitudes) between 0 and 1.

##### **Examples**

Running the `DefaultComponents.py` file should produce white noise, and the `sine-wave-example.py` file shows an example of runtime audio control.

##### **Implementation Details**

* tested with python 2.8 and PyAudio 0.2.8 on Windows 8.1

* each object is run in it's own thread and queues output data in FIFO pipes for the proceeding step

* current implementation uses PyAudio, the Python bindings for PortAudio, for audio playback
