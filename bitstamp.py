from candle_creator import *
from models import *

manager = CandleManager(BitstampCandle, 60)
creator = CandleCreator(manager, BitstampTrade, "Bitstamp")
creator.run()
