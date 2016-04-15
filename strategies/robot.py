from easyquant import DefaultLogHandler
from easyquant import StrategyTemplate
import requests
import re
import datetime


class Strategy(StrategyTemplate):
    name = 'joinquant'
    last_order = None
    allow_types = ['jslquotation']
    def init(self):
        self.engine = JoinQuant('17701971032', 'weihong', 'eef65c3d35e886f7592f0dc3963f8fcc')

    def strategy(self, event):
        print(event.data)
        pass


    def clock(self, event):
        """在交易时间会定时推送 clock 事件
        :param event: event.data.clock_event 为 [0.5, 1, 3, 5, 15, 30, 60] 单位为分钟,  ['open', 'close'] 为开市、收市
            event.data.trading_state  bool 是否处于交易时间
        """
        if event.data.clock_event == 'open':
            # 开市了
            self.log.info('open')
            self.keep_alive()
        elif event.data.clock_event == 'close':
            # 收市了
            self.log.info('close')
        elif event.data.clock_event == 5:
            # 5 分钟的 clock
            orders = self.engine.get_order()
            for order in orders:
                buy, stock, amount, price, t = [int(order[1]) > 0] + order
                t = datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
                if self.last_order is None or t > self.last_order:
                    if buy:
                        result = self.user.buy(order[0], order[2], int(order[1]))
                    else:
                        result = self.user.sell(order[0], order[2],  int(order[1]))
                    self.log.info(result)
                    self.last_order = t
            self.log.info("5分钟")


    def log_handler(self):
        """自定义 log 记录方式"""
        return DefaultLogHandler(self.name, log_type='file', filepath='joinquant.log')


class JoinQuant(object):
    """聚宽交易指令获取引擎"""

    def __init__(self, username, password, backtestId):
        self.username = username
        self.password = password
        self.client = None
        self.backtestId = backtestId
        self.login()

    def login(self):
        self.client = requests.Session()
        response = self.client.post('https://www.joinquant.com/user/login/doLogin', {"CyLoginForm[username]":self.username,
                                                                          "CyLoginForm[pwd]":self.password,
                                                                          "ajax":1})
        if "error" in response.json():
            raise ValueError("login error")

    def get_order(self):
        response = self.client.get("https://www.joinquant.com/algorithm/live/transactionDetail?backtestId={backtestId}&date={date}".format(backtestId=self.backtestId, date=(datetime.datetime.now()).strftime('%Y-%m-%d')))
        order = response.json()
        results = []
        for _order in order["data"]["transaction"]:
            results.append([re.search("\d{6}",_order['stock']).group(), re.search(r"<span.*>(.+?)</span>", _order['share']).groups()[0], _order['price'], _order['date']])
        return results


