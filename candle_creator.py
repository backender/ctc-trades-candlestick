from candle_manager import *

class CandleCreator(object):
    def __init__(self, manager, exchangeTrade, exchange):
        self.manager = manager
        self.exchangeTrade = exchangeTrade
        self.exchange = exchange # remove

    def run(self):
        myDB.connect()
        self.manager.candleClass.create_table(True)
        batch = 1000*int(self.manager.frequency)/60 # make configurable

        while True:
            try:
                lastCandle = self.manager.candleClass.select().order_by(self.manager.candleClass.id.desc()).get()
                idfrom = lastCandle.idto + 1 # last idto from existing candles + 1
            except pw.DoesNotExist:
                idfrom = 0

            print "Starting from " + self.exchange + " (" + self.exchangeTrade._meta.db_table + ") " + "trade: " + str(idfrom)
            trades = self.exchangeTrade.select().where(self.exchangeTrade.id >= idfrom).limit(batch)
            print "Found " + str(len(trades)) + " new trades"
            (candles, candle) = self.manager.insertCandles(myDB, trades)
            print str(len(candles)) + " Candles written to: " + self.manager.candleClass._meta.db_table
            if len(candles) == 0:
                time.sleep(10)
