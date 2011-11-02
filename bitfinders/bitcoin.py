"""
helper to parse bitcoin values
"""

from BeautifulSoup import BeautifulSoup
import urllib
try:
    import simplejson as json
except ImportError:
    import json
import md5

class BitCoinError(Exception):
    """ handles bitcoin error """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class BitCoinApi(object):
    """
    parent class for the differents api
    """
    def __init__(self, **kwargs):
        self.md5_offers = None
        self.md5_trades = None
        self.md5_ticker = None

    def _get_json(self, action=None, *args, **kwargs):
        f = urllib.urlopen("%s%s" % (self.URI, action))
        if f:
            return f.read()
        return None

    def get_ticker(self):
        """ represents market volumes """
        bit_json = self._get_json(action=self.VERBS[0])
        self.ticker = json.loads(bit_json)
        self.md5_ticker = md5.new(bit_json).hexdigest()
        return self.ticker

    def get_offers(self):
        bit_json = self._get_json(action=self.VERBS[1])
        self.offers = json.loads(bit_json)
        self.md5_offers = md5.new(bit_json).hexdigest()
        return self.offers

    def get_transactions(self):
        """ gets latest transactions """
        bit_json = self._get_json(action=self.VERBS[2])
        self.transactions = json.loads(bit_json)
        self.md5_trades = md5.new(bit_json).hexdigest()
        return self.transactions

class BritCoinApi(BitCoinApi):
    """
    parse and get data from britcoin.co.uk

    verbs (or action) are:
      - ticker: Market volume
      - getDepth: Active offers
      - getTrades: Latest transaction

    * ticker example:
    {"ticker": {"vol": 1798.44951852, "buy": 11, "sell": 11.9048, "last": 0.5}} 
    * getDepth example:
    {"asks": [[24.0000, 5], [23.0000, 10], [49.1400, 50],..]}
    * getTrades example:
    [{"date": 1307794561, "price": 13.6054, "amount": 0.735},..]
    """
    URI = "http://britcoin.co.uk/api/"
    VERBS = ["ticker", "getDepth", "getTrades"]

    def __init__(self, **kwargs):
        super(BritCoinApi, self).__init__(**kwargs)


class BitMarketEuApi(BitCoinApi):
    """
    parse and get data from bitmarket.eu

    verbs (or action) are:
      - ticker: Market volume and min/max prices for all currencies
      - get_offers: Active offers for all currencies as: [price, amount, "currency"]
      - get_transactions: Latest completed transactions (trades)

    PARAMS for action:
      - ticker
        - no param
      - get_offers: 
        - currency - display offers for this currency
      - get_trades: 
        - currency - display trades for this currency
        - days - display trades from n days (default: 2)

    * ticker example:
    {"vol":"1047.37","currencies":{"EUR":{"sell":"14.75","buy":"14.75","last":"14"}..}
    * get_offers example:
    {"asks":[[100,2,"EUR"],[200,2,"EUR"]..}
    * get_trades example:
    [{"date":"1307878498","currency":"EUR","amount":"3","price":"14"}..]
    """
    URI = "http://bitmarket.eu/api/"
    VERBS = ["ticker", "get_offers", "get_transactions"]

    def __init__(self, **kwargs):
        super(BitMarketEuApi, self).__init__(**kwargs)
