from models import *

class Instrument(object):
    def __init__(self,
                 exchange_name,
                 frequency,
                 **param):
        """
        Constructor
        :param exchange: Exchange name
        :param instmt_code: Instrument code
        :param param: Options parameters, e.g. restful_order_book_link
        :return:
        """
        self.exchange_name = exchange_name
        self.frequency = int(frequency) #important!

    def copy(self, obj):
        """
        Copy constructor
        """
        self.exchange_name = obj.exchange_name
        self.frequency = frequency

    def get_exchange_name(self):
        return self.exchange_name

    def get_frequency(self):
        return self.frequency

    def get_candle(self):
        candles = {
            'Bitfinex': BitfinexCandle,
            'Bitstamp': BitstampCandle,
            'Gdax': GdaxCandle
        }
        return candles.get(self.exchange_name)

    def get_trade(self):
        trades = {
            'Bitfinex': BitfinexTrade,
            'Bitstamp': BitstampTrade,
            'Gdax': GdaxTrade
        }
        return trades.get(self.exchange_name)
