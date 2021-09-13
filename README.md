# stock-trading
<b>Author: Dana Yi</b>

(Paper-testing) different trading strategies and backtesting for fun

## Setup
`pip3 install backtesting # not needed`

`pip3 install backtrader`

`pip3 install matplotlib # charting`

## Plan
- ⌛ Backtesting various strategies (using downloaded historical data)
- ❌ Connect to WeBull API to be able to place paper trades
- ❌ Use strategies/AI/ML to trade

## Files
- btmain.py - has everything cerebro related
- data/ - contains sample data
- backtest.py - uses backtesting and sample GOOG data with a simple 10/20SMA crossover strategy
- strategies.py - strategies to backtest

### Notes
- backtesting doesn't seem as useful as backtrader, but will leave for now
- h2o -> simple task ML platform