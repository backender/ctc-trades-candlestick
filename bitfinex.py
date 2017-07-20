from candle_creator import *
from models import *

manager = CandleManager(BitfinexCandle, 60)
creator = CandleCreator(manager, BitfinexTrade, "Bitfinex")
creator.run()
