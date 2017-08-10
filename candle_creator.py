from candle_manager import *

class CandleCreator(object):
    def __init__(self, db, manager, baseObject):
        self.manager = manager
        self.baseObject = baseObject
        self.db = db

    def run(self):
        self.manager.candleClass.create_table(True)
        batch = 10000*int(self.manager.frequency)/60 # make configurable

        while True:
            try:
                lastCandle = self.manager.candleClass.select().order_by(self.manager.candleClass.id.desc()).get()
                idfrom = lastCandle.idto + 1 # last idto from existing candles + 1
            except pw.DoesNotExist:
                idfrom = 0

            print "Starting from (" + self.baseObject._meta.db_table + ") " + "trade: " + str(idfrom)
            trades = self.baseObject.select().where(self.baseObject.id >= idfrom).limit(batch)
            print "Found " + str(len(trades)) + " new trades"
            (candles, candle) = self.manager.insertCandles(self.db, trades)
            print str(len(candles)) + " Candles written to: " + self.manager.candleClass._meta.db_table
            if len(candles) == 0:
                time.sleep(10)

    def runOnCandle(self):
        self.manager.candleClass.create_table(True)

        while True:
            try:
                lastCandle = self.manager.candleClass.select().order_by(self.manager.candleClass.id.desc()).get()
                idfrom = lastCandle.id + 1 # last idto from existing candles + 1
            except pw.DoesNotExist:
                idfrom = 0

            print "Starting from (" + self.baseObject()._meta.db_table + ") " + "candle with id >= " + str(idfrom)
            candlesBatch = self.baseObject.select().where(self.baseObject.id >= idfrom)#.limit(batch)
            baseCandles = []
            for c in candlesBatch:
                baseCandles.append(c)
            print "Found " + str(len(candlesBatch)) + " new candles"
            candles = []
            candlesInserted = []

            freqMinute = self.manager.frequency / 60
            while len(baseCandles) >= freqMinute:
                for i in range(freqMinute):
                    baseCandle = baseCandles[i]
                    if i == 0:
                        candle = self.manager.candleClass()
                        candle.trades = baseCandle.trades
                        candle.idfrom = baseCandle.idfrom
                        candle.open = baseCandle.open
                        candle.volume = baseCandle.volume
                        candle.low = baseCandle.low
                        candle.high = baseCandle.high

                    else:
                        candle.trades = candle.trades + baseCandle.trades
                        candle.volume = candle.volume + baseCandle.volume
                        if candle.low > baseCandle.low:
                            candle.low = baseCandle.low
                        if candle.high < baseCandle.high:
                            candle.high = baseCandle.high

                candle.idto = baseCandle.idto
                candle.close = baseCandle.close
                candle.candle_date_time = baseCandle.candle_date_time
                candles.append(candle) # append / insert
                del baseCandles[0]

            print "Total inserted in ("+self.manager.candleClass._meta.db_table+"): " + str(len(candles))
            if len(candles) == 0:
                time.sleep(10)
            else:
                self.manager.insert(self.db, candles)
