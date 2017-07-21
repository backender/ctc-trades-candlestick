from candle_creator import *
from subscription_manager import SubscriptionManager

instmts = SubscriptionManager("subscriptions.ini").get_subscriptions()
for instmt in instmts:
    manager = CandleManager(instmt.get_candle(), instmt.get_frequency())
    creator = CandleCreator(manager, instmt.get_trade(), instmt.get_exchange_name())
    creator.run()
