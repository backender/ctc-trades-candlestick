from candleManager import *
from models import *

creator = CandleCreator(BitfinexCandle, 60)
manager = CandleManager(creator, BitfinexTrade, "Bitfinex")
manager.run()
