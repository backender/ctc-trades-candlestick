from candle_creator import *
from models import *

manager = CandleManager(GdaxCandle, 60)
creator = CandleCreator(manager, GdaxTrade, "GDAX")
creator.run()
