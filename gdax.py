from candleManager import *
from models import *

creator = CandleCreator(GdaxCandle, 60)
manager = CandleManager(creator, GdaxTrade, "GDAX")
manager.run()
