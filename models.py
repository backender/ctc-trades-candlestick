import peewee as pw
import os
from dateutil import parser

myDB = (pw.MySQLDatabase(
            os.environ['CTC_CANDLES_DB'],
            host=os.environ['CTC_CANDLES_HOST'],
            port=int(os.environ['CTC_CANDLES_PORT']),
            user=os.environ['CTC_CANDLES_USER'],
            passwd=os.environ['CTC_CANDLES_PASSWORD']))

# myDB = (pw.MySQLDatabase(
#             "bcex",
#             host="localhost",
#             port=3306,
#             user="root",
#             passwd="password"))

class MySQLModel(pw.Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = myDB

class Candle(MySQLModel):
    firstTrade = None
    lastTrade = None
    close = pw.DecimalField(null=True)
    high = pw.DecimalField(null=True)
    low = pw.DecimalField(null=True)
    open = pw.DecimalField(null=True)
    trades = pw.IntegerField(null=True)
    volume = pw.DecimalField(null=True, max_digits=20, decimal_places=8)
    idfrom = pw.IntegerField(null=True)
    idto = pw.IntegerField(null=True)
    candle_date_time = pw.CharField(null=True)

class BitfinexCandle(Candle):
    class Meta:
        db_table = 'exch_bitfinex_btcusd_candles_'

class BitstampCandle(Candle):
    class Meta:
        db_table = 'exch_bitstamp_btcusd_candles_'

class GdaxCandle(Candle):
    class Meta:
        db_table = 'exch_gdax_btcusd_candles_'

class Trade(MySQLModel):
    a1 = pw.DecimalField(null=True)
    a2 = pw.DecimalField(null=True)
    a3 = pw.DecimalField(null=True)
    a4 = pw.DecimalField(null=True)
    a5 = pw.DecimalField(null=True)
    aq1 = pw.DecimalField(null=True)
    aq2 = pw.DecimalField(null=True)
    aq3 = pw.DecimalField(null=True)
    aq4 = pw.DecimalField(null=True)
    aq5 = pw.DecimalField(null=True)
    b1 = pw.DecimalField(null=True)
    b2 = pw.DecimalField(null=True)
    b3 = pw.DecimalField(null=True)
    b4 = pw.DecimalField(null=True)
    b5 = pw.DecimalField(null=True)
    bq1 = pw.DecimalField(null=True)
    bq2 = pw.DecimalField(null=True)
    bq3 = pw.DecimalField(null=True)
    bq4 = pw.DecimalField(null=True)
    bq5 = pw.DecimalField(null=True)
    #exchange = pw.CharField()
    instmt = "BTCUSD"
    order_date_time = pw.CharField(null=True)
    trade_px = pw.DecimalField(null=True)
    trade_volume = pw.DecimalField(null=True, max_digits=20, decimal_places=8)
    trades_date_time = pw.CharField(null=True)
    update_type = pw.IntegerField(null=True)

    def tradeDate(self):
        return parser.parse(self.trades_date_time)

class GdaxTrade(Trade):
    exchange = "GDAX"
    class Meta:
        db_table = 'exch_gdax_btcusd_snapshot_20170718'

class BitfinexTrade(Trade):
    exchange = "Bitfinex"
    class Meta:
        db_table = 'exch_bitfinex_btcusd_snapshot_20170718'

class BitstampTrade(Trade):
    exchange = "Bitstamp"
    class Meta:
        db_table = 'exch_bitstamp_btcusd_snapshot_20170718'
