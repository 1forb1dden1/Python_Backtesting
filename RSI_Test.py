from backtesting import Backtest, Strategy
import talib
import yfinance as yf

data = yf.download("TSLA", start="2023-11-07", end="2023-12-29", interval="15m")

data = data[['Open', 'High', 'Low', 'Close', 'Volume']]

class Rsi(Strategy):
    # RSI strategy parameters
    buy_threshold = 40
    rsi_window = 14
    take_profit = 1.05
    stop_loss = 0.97
    current_price = 0

    def init(self):
        # Initialize RSI indicator
        self.rsi = self.I(talib.RSI, self.data.Close, self.rsi_window)

    def next(self):
        # Execute trading logic based on RSI values
        current_rsi = self.rsi[-1]

        if current_rsi <= self.buy_threshold:
            # Buy at the current close price
            self.buy()
            self.current_price = self.data.Close[-1]
        
        #Take Profit & Stop Loss (BRACKET)
        #elif self.data.Close > self.take_profit * self.current_price or self.data.Close < self.stop_loss * self.current_price:
        #    self.position.close()
        
        elif current_rsi >= 70:
            self.position.close()

# Backtest with RSI strategy
bt = Backtest(data, Rsi, cash=10_000, commission=(0.00))

stats = bt.optimize(
    buy_threshold=35,
)

# Print optimization results
print(stats)

# Plot the backtest results
bt.plot(filename="plots/")