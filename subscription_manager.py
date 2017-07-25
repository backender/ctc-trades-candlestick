from instrument import Instrument
try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

class SubscriptionManager:
    def __init__(self, config_path):
        """
        Constructor
        """
        self.config = ConfigParser.ConfigParser()
        self.config.read(config_path)

    def get_instmt_ids(self):
        """
        Return all the instrument ids
        """
        return self.config.sections()

    def get_instrument(self, instmt_id):
        """
        Return the instrument object by instrument id
        :param instmt_id: Instrument ID
        :return Instrument object
        """
        exchange_name = self.config.get(instmt_id, 'exchange')
        candle_table = self.config.get(instmt_id, 'candle_table')
        frequency = self.config.get(instmt_id, 'frequency')
        enabled = int(self.config.get(instmt_id, 'enabled'))
        base = self.config.get(instmt_id, 'base')
        base_table = self.config.get(instmt_id, 'base_table')
        params = dict(self.config.items(instmt_id))
        del params['exchange']
        del params['candle_table']
        del params['frequency']
        del params['enabled']
        del params['base']
        del params['base_table']

        if enabled == 1:
            return Instrument(exchange_name, candle_table, int(frequency), base, base_table, **params)
        else:
            return None

    def get_subscriptions(self):
        """
        Get all the subscriptions from the configuration file
        :return List of instrument objects
        """
        instmts = [self.get_instrument(inst) for inst in self.get_instmt_ids()]
        return [instmt for instmt in instmts if instmt is not None]
