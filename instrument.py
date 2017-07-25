from models import *

class Instrument(object):
    def __init__(self,
                 exchange_name,
                 candle_table,
                 frequency,
                 base,
                 base_table,
                 **param):
        """
        Constructor
        :param exchange: Exchange name
        :param instmt_code: Instrument code
        :param param: Options parameters, e.g. restful_order_book_link
        :return:
        """
        self.exchange_name = exchange_name
        self.candle_table = candle_table
        self.frequency = int(frequency) #important!
        self.base = base
        self.base_table = base_table

    def copy(self, obj):
        """
        Copy constructor
        """
        self.exchange_name = obj.exchange_name
        self.candle_table = candle_table
        self.frequency = frequency
        self.base = base
        self.base_table = base_table

    def get_exchange_name(self):
        return self.exchange_name

    def get_candle_table(self):
        return self.candle_table

    def get_base_table(self):
        return self.base_table

    def get_frequency(self):
        return self.frequency

    def get_base(self):
        return self.base

    def get_candle(self):
        candles = {
            'Bitfinex': BitfinexCandle,
            'Bitstamp': BitstampCandle,
            'Gdax': GdaxCandle
        }
        candle = candles.get(self.exchange_name)
        candle._meta.db_table = self.candle_table # make configurable
        return candle

    def get_base_candle(self):
        if self.base != 'candle':
            return None
        candles = {
            'Bitfinex': BitfinexCandleBase,
            'Bitstamp': BitstampCandleBase,
            'Gdax': GdaxCandleBase
        }
        candle = candles.get(self.exchange_name)
        candle._meta.db_table = self.base_table # make configurable
        return candle


    def get_trade(self):
        trades = {
            'Bitfinex': BitfinexTrade,
            'Bitstamp': BitstampTrade,
            'Gdax': GdaxTrade
        }
        return trades.get(self.exchange_name)
