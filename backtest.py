from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from backtesting.test import SMA, GOOG


class SmaCross(Strategy):
    fast_sma = 10
    slow_sma = 20

    def init(self):
        close = self.data.Close
        self.sma1 = self.I(SMA, close, self.fast_sma)
        self.sma2 = self.I(SMA, close, self.slow_sma)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()


bt = Backtest(GOOG, SmaCross,
              cash=100000, commission=0.00,
              exclusive_orders=True)

output = bt.run()
bt.plot()
