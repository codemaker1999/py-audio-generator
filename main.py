from dataProcessor import DataProcessor 
from dataCollector import DataCollector
from AudioWriter import AudioWriter
from AudioPlayer import AudioPlayer

dc=DataCollector()
dp=DataProcessor(dc)
aw=AudioWriter(dp)
ap=AudioPlayer(aw)

ap.start()