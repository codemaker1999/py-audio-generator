from DataCollector import DataCollector
from DataProcessor import DataProcessor 
from AudioWriter import AudioWriter
from AudioPlayer import AudioPlayer

dc = DataCollector()
dp = DataProcessor(dc)
aw = AudioWriter(dp)
ap = AudioPlayer(aw)

ap.start()