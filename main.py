from candle_creator import *
from subscription_manager import SubscriptionManager

instmts = SubscriptionManager("subscriptions.ini").get_subscriptions()
myDB.connect()
for instmt in instmts:
    manager = CandleManager(instmt.get_candle(), instmt.get_frequency())
    if instmt.get_base() == 'candle':
        print "Based on candle"
        print "----------------"
        creator = CandleCreator(myDB, manager, instmt.get_base_candle())
        creator.runOnCandle()
    else:
        print "Based on trade"
        print "----------------"
        creator = CandleCreator(myDB, manager, instmt.get_trade())
        creator.run()
