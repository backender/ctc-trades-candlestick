from candleManager import *
from models import *

creator = CandleCreator(BitstampCandle, 60)
manager = CandleManager(creator, BitstampTrade, "Bitstamp")
manager.run()
