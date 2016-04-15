import easyquotation

import easyquant
import easytrader
from easyquant import DefaultQuotationEngine, DefaultLogHandler, PushBaseEngine

class JSLQuotationEngine(PushBaseEngine):
    PushInterval = 1000
    EventType = 'jslquotation'

    def init(self):
        self.source = easyquotation.use('jsl')
        self.source.login('audoe', 'wh13chen')

    def fetch_quotation(self):
        return self.source.fundarb()


log_type = 'stdout'

log_handler = DefaultLogHandler(name='robot', log_type=log_type, filepath='')

user = easytrader.use('ht', remove_zero=False)
user.prepare('ht.json')

m = easyquant.MainEngine(user, quotation_engines=[DefaultQuotationEngine, JSLQuotationEngine], log_handler=log_handler)
m.load_strategy()
m.start()
