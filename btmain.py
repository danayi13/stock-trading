import backtrader as bt

from datetime import datetime
from strategies import MACrossOver, PrintClose

#----- Dummy Strategy for Printing -------------#
# # instantiate cerebro engine + add data and strategies
# cerebro = bt.Cerebro()
# data = bt.feeds.YahooFinanceCSVData(dataname='data/TSLA.csv')
# cerebro.adddata(data)
# cerebro.addstrategy(PrintClose)

# # run cerebro engine
# cerebro.run()
#----------------------------------------------#

# instantiate cerebro engine
cerebro = bt.Cerebro()

# set data params and add to cerebro
data = bt.feeds.YahooFinanceCSVData(
    dataname='data/TSLA.csv',
    fromdate=datetime(2016, 1, 1),
    todate=datetime(2017, 12, 25)
)
cerebro.adddata(data)

# add strategy to cerebro
cerebro.addstrategy(MACrossOver)

# default position size
cerebro.addsizer(bt.sizers.SizerFix, stake=100)

if __name__ == '__main__':
    # run cerebro engine
    start_portfolio_value = cerebro.broker.getvalue()

    cerebro.run()

    end_portfolio_value = cerebro.broker.getvalue()
    pnl = end_portfolio_value - start_portfolio_value

    print(f'Starting Portfolio Value: {start_portfolio_value:.2f}')
    print(f'Final Portfolio Value: {end_portfolio_value:.2f}')
    print(f'PnL: {pnl:.2f}')
