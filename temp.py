from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime 
from alpaca_trade_api import REST 
from datetime import timedelta
from finbert_utils import estimate_sentiment
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pickle
import pandas as pd
import yfinance as yf
msg = MIMEMultipart()

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

API_KEY = "PKSMWXDJFYEZKBFLSKE7"
API_SECRET = "1bbjhNjtjmLiYfUhbdLnJhNiQ7pYMUG6ndXhyqoA"
BASE_URL = "https://paper-api.alpaca.markets/v2"

ALPACA_CREDS = {
    "API_KEY":API_KEY, 
    "API_SECRET": API_SECRET, 
    "PAPER": True
}

#3 occurences of the symbol variable

class PaisaFy(Strategy): 
    def initialize(self, symbol:str="SPY", cash_at_risk:float=.60): 
        self.symbol = symbol
        self.sleeptime = "24H" 
        self.last_trade = None 
        self.cash_at_risk = cash_at_risk
        self.api = REST(base_url=BASE_URL, key_id=API_KEY, secret_key=API_SECRET)
        try:
                with open('bot_state.pkl', 'rb') as f:
                    state = pickle.load(f)
                    self.last_trade = state['last_trade']
        except FileNotFoundError:
                self.last_trade = None

    def position_sizing(self): 
        cash = self.get_cash() 
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash * self.cash_at_risk / last_price,0)
        return cash, last_price, quantity
    
    def get_dates(self): 
        today = self.get_datetime()
        three_days_prior = today - timedelta(days=3)
        return today.strftime('%Y-%m-%d'), three_days_prior.strftime('%Y-%m-%d')
    
    def get_dates_SMA(self): 
        today = self.get_datetime()
        twoHundred_days_prior = today - timedelta(days=200)
        return today.strftime('%Y-%m-%d'), twoHundred_days_prior.strftime('%Y-%m-%d')

    def get_sentiment(self): 
        today, three_days_prior = self.get_dates()
        news = self.api.get_news(symbol=self.symbol, 
                                 start=three_days_prior, 
                                 end=today) 
        news = [ev.__dict__["_raw"]["headline"] for ev in news]
        probability, sentiment = estimate_sentiment(news)
        return probability, sentiment 
    
    def get_data(self, ticker, start_date, end_date):
        data = yf.download(ticker, start=start_date, end=end_date)
        return data

    def calculate_indicators(self, data):
        data['SMA_50'] = data['Close'].rolling(window=50).mean()
        data['SMA_200'] = data['Close'].rolling(window=200).mean()
        return data

    def on_trading_iteration(self):
        try:  
            cash, last_price, quantity = self.position_sizing() 
            probability, sentiment = self.get_sentiment()
            ticker = 'SPY'
            end_date, start_date = self.get_dates_SMA()
            try:
                stock_data = self.get_data(ticker, start_date, end_date)
            except Exception as e:
                print(f"Error: {e}")
                return

            # Calculate indicators
            stock_data = self.calculate_indicators(stock_data)

            # Display SMA values
            last_row = stock_data.iloc[-1]
            sma_50 = last_row['SMA_50']
            sma_200 = last_row['SMA_200']

           # raise Exception('This is a test exception') 
            if cash > last_price: 
                if sentiment == "positive" and probability > .95 and sma_50 > sma_200:
                    if self.last_trade == "sell": 
                        self.sell_all() 
                    order = self.create_order(
                        self.symbol, 
                        quantity, 
                        "buy", 
                        type="bracket", 
                        take_profit_price=last_price*1.20, 
                        stop_loss_price=last_price*.95
                    )
                    self.submit_order(order) 
                    self.last_trade = "buy"
                    print(f"Placed a buy order for {quantity} shares of {self.symbol}")

                elif sentiment == "negative" and probability > .95 and sma_50 < sma_200:
                    if self.last_trade == "buy": 
                        self.sell_all() 
                    order = self.create_order(
                        self.symbol, 
                        quantity, 
                        "sell", 
                        type="bracket", 
                        take_profit_price=last_price*.8, 
                        stop_loss_price=last_price*1.05
                    )
                    self.submit_order(order) 
                    self.last_trade = "sell"
                    print(f"Placed a sell order for {quantity} shares of {self.symbol}")
                    with open('bot_state.pkl', 'wb') as f:
                        pickle.dump({'last_trade': self.last_trade}, f)
        except Exception as e:
                print('The trading bot has crashed and will not restart')
                msg['From'] = 'gtworks247@gmail.com'
                msg['To'] = 'gttrys247@gmail.com'
                msg['Subject'] = 'Trading Bot Error'
                msg.attach(MIMEText('The trading bot has crashed. It is advised to KEEP YOUR PORTFOLIO in check until the bot is up again.'))
                try:
                    mailserver = smtplib.SMTP('smtp.gmail.com', 587)
                    mailserver.ehlo()
                    mailserver.starttls()
                    mailserver.login('gtworks247@gmail.com', 'luczzbsakevaaejc')
                    mailserver.sendmail('gtworks247@gmail.com', 'gttrys247@gmail.com', msg.as_string())
                    print('Email notification sent')
                    mailserver.quit()
                except Exception as e:
                    print(f"Failed to send email: {e}")
start_date = datetime(2023,1,1)
end_date = datetime(2024,4,11) 
broker = Alpaca(ALPACA_CREDS) 
strategy = PaisaFy(name='mlstrat', broker=broker, 
                    parameters={"symbol":"SPY", 
                                "cash_at_risk":.5})

strategy.backtest(    
    YahooDataBacktesting,   
    start_date, 
    end_date, 
    parameters={"symbol":"SPY", "cash_at_risk":.5}
)

# trader = Trader()
# trader.add_strategy(strategy)
# trader.run_all()

#manual intervention when the bot crashes.

#==================================================================#