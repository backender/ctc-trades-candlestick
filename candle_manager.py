import peewee as pw
from datetime import datetime, timedelta
import os
import time
from models import *

class CandleManager(object):

    def __init__(self, candleClass, frequency):
        self.candleClass = candleClass
        self.frequency = frequency

    def withinCandle(self, trade, firstTrade, frequency = 60):
        return (trade.tradeDate() - firstTrade.tradeDate()).total_seconds() > frequency

    def addTrade(self, trade, candles, candle):
        if not candle.lastTrade or self.withinCandle(trade, candle.firstTrade, self.frequency):
            if candle.lastTrade:
                candle.idto = candle.lastTrade.id
                candle.close = candle.lastTrade.trade_px
                candle.candle_date_time = candle.lastTrade.trades_date_time
                candles.append(candle) # append / insert
                #print candle.__dict__

            candle = self.candleClass()
            candle.firstTrade = trade
            candle.trades = 1
            candle.idfrom = trade.id
            candle.open = trade.trade_px
            candle.volume = trade.trade_volume
            candle.low = trade.trade_px
            candle.high = trade.trade_px
        else:
            candle.trades = candle.trades + 1
            candle.volume = candle.volume + trade.trade_volume
            if candle.low > trade.trade_px:
                candle.low = trade.trade_px
            if candle.high < trade.trade_px:
                candle.high = trade.trade_px

        candle.lastTrade = trade
        return (candles, candle)

    def createCandles(self, trades):
        candle = self.candleClass()
        candles = []
        for trade in trades:
            candles, candle = self.addTrade(trade, candles, candle)
        return (candles, candle)

    def insert(self, db, candles):
        with db.atomic():
            cs = map(lambda c: (c.__dict__)['_data'], candles)
            self.candleClass.insert_many(cs).execute()

    def insertCandlesBulk(self, db, trades, bulk):
        candle = self.candleClass()
        candles = []
        candlesTmp = []
        for trade in trades:
            candlesTmp, candle = self.addTrade(trade, candlesTmp, candle)
            if len(candlesTmp) >= bulk:
                self.insert(db, candlesTmp)
                candles = candles + candlesTmp
                candlesTmp = []
        # Bulk leftover which are still valid candles
        if candlesTmp:
            self.insert(db, candlesTmp)
            candles.append(candlesTmp)
        return (candles, candle)

    def insertCandles(self, db, trades):
        return self.insertCandlesBulk(db, trades, 1)
