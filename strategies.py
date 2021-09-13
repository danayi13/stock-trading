import backtrader as bt


class PrintClose(bt.Strategy):
    """sample strategy class for printing closing prices"""

    def __init__(self):
        self.dataclose = self.datas[0].close

    def log(self):
        """print date and closing price"""
        date = self.datas[0].datetime.date(0)
        closing_price = self.dataclose[0]
        print(f'{date.isoformat()} Close: {closing_price:.2f}')

    # Runs for each data point
    def next(self):
        self.log()


class MACrossOver(bt.Strategy):
    # moving average parameters
    params = (('sma_fast', 20), ('sma_slow', 50))

    def __init__(self):
        self.dataclose = self.datas[0].close

        self.order = None  # ongoing order details/status

        # instantiate moving averages
        self.slow_sma = bt.indicators.MovingAverageSimple(self.datas[0],
                                                          period=self.params.sma_slow)
        self.fast_sma = bt.indicators.MovingAverageSimple(self.datas[0],
                                                          period=self.params.sma_fast)

    def log(self, txt, dt=None):
        """logs buy/sells/info"""
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} {txt}')

    def notify_order(self, order):
        """processes everything related to trade orders"""
        if order.status in [order.Submitted, order.Accepted]:
            return  # active buy/sell order submitted/accepted - do nothing

        # check if order has been completed (could reject if not enough cash)
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, {order.executed.price:.2f}')
            elif order.issell():
                self.log(f'SELL EXECUTED, {order.executed.price:.2f}')
            elif order.status in [order.Canceled, order.Margin, order.Rejected]:
                self.log('Order Canceled/Margin/Rejected')

            self.bar_executed = len(self)

            self.order = None  # reset orders

    def next(self):
        if self.order:
            return  # no open orders

        # not in market, look for signal to OPEN trades
        if not self.position:
            # 20 SMA above 50 SMA
            if self.fast_sma[0] > self.slow_sma[0] and self.fast_sma[-1] < self.slow_sma[-1]:
                self.log(f'BUY CREATE {self.dataclose[0]:.2f}')
                self.order = self.buy()  # keep track of order to avoid 2nd order

            # 20 SMA below 50 SMA
            elif self.fast_sma[0] < self.slow_sma[0] and self.fast_sma[-1] > self.slow_sma[-1]:
                self.log(f'SELL CREATE {self.dataclose[0]:.2f}')
                self.order = self.sell()  # keep track of order to avoid 2nd order

        # already in market, look for signal to CLOSE trades
        else:
            # dummy for now just exit after 5 days of entering
            if len(self) >= (self.bar_executed + 5):
                self.log(f'CLOSE CREATE {self.dataclose[0]:.2f}')
                self.order = self.close()
