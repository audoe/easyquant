# coding: utf-8
import aiohttp
from base_engine import BaseEngine
import time
from easyquant.event_engine import Event
from ..easydealutils import time as etime

class BaseEngine:
class JSLQuotationEngine(BaseEngine):
    """集思录行情推送"""
    PushInterval = 100
    EventType = 'jslquotation'

    def init(self):
        self.source = easyquotation.use('jsl')
        self.source.login('audoe', 'wh13chen')

    def fetch_quotation(self):
        return self.source.fundarb()

    def push_quotation(self):
        while self.is_active:
            now_time = datetime.datetime.now()
            time_delta = now_time - self.start_time
            
            if etime.is_holiday_today():
                sleep_time = etime.calc_next_trade_time_delta_seconds() + 1
                time.sleep(sleep_time)

            elif etime.is_tradetime_now():  # 工作日，干活了
                try:
                    response_data = self.fetch_quotation()
                except aiohttp.errors.ServerDisconnectedError:
                    time.sleep(self.PushInterval)
                    continue
                event = Event(event_type=self.EventType, data=response_data)
                self.event_engine.put(event)
                time.sleep(self.PushInterval)
            else:
                sleep_time = etime.calc_next_trade_time_delta_seconds() + 1
                time.sleep(sleep_time)
