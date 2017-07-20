from candleCreator import *

class CandleManager(object):
    def __init__(self, creator, exchangeTrade, exchange):
        self.creator = creator
        self.exchangeTrade = exchangeTrade
        self.exchange = exchange # remove

    def run(self):
        myDB.connect()
        self.creator.candleClass.create_table(True)
        batch = 1000
        
        while True:
            try:
                lastCandle = self.creator.candleClass.select().order_by(self.creator.candleClass.id.desc()).get()
                idfrom = lastCandle.idto + 1 # last idto from existing candles + 1
            except pw.DoesNotExist:
                idfrom = 0

            print "Starting from " + self.exchange + " trade: " + str(idfrom)
            trades = self.exchangeTrade.select().where(self.exchangeTrade.id >= idfrom).limit(batch)
            (candles, candle) = self.creator.insertCandles(myDB, trades)
            print str(len(candles)) + " Candles written to DB."
            if len(candles) == 0:
                time.sleep(5)
