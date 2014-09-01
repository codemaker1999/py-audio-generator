from WhiteNoise import DataCollector, DataProcessor, AudioWriter, AudioPlayer

dc = DataCollector()
dp = DataProcessor(dc)
aw = AudioWriter(dp)
ap = AudioPlayer(aw)

ap.start()