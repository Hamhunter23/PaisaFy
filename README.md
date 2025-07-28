# PaisaFy Trading Bot 🤖📈

An intelligent algorithmic trading bot that combines sentiment analysis, technical indicators, and automated trading execution using the Alpaca API. The bot analyzes news sentiment using FinBERT and incorporates Simple Moving Average (SMA) crossover strategies for enhanced trading decisions.

## 🌟 Features

### Core Trading Features
- **Sentiment Analysis**: Uses FinBERT (Financial BERT) to analyze news sentiment for trading decisions
- **Technical Analysis**: Implements SMA (Simple Moving Average) crossover strategies (50-day vs 200-day)
- **Automated Trading**: Executes buy/sell orders automatically based on combined sentiment and technical signals
- **Risk Management**: Implements bracket orders with take-profit and stop-loss levels
- **Position Sizing**: Intelligent cash allocation based on configurable risk parameters

### Monitoring & Reliability
- **Email Notifications**: Automated email alerts for bot status, errors, and crashes
- **Auto-Recovery**: Automatic restart functionality with configurable retry attempts
- **State Persistence**: Saves trading state to prevent conflicts during restarts
- **Comprehensive Logging**: Detailed logs, statistics, and HTML tearsheets for performance analysis
- **Backtesting**: Historical strategy testing with Yahoo Finance data

### Data Sources
- **News Data**: Real-time financial news via Alpaca API
- **Price Data**: Historical and real-time stock data via Yahoo Finance and Alpaca
- **Market Data**: Supports various stocks and ETFs (default: TSLA, SPY)

## 🏗️ Architecture

```
├── tradingbot.py          # Main trading strategy implementation
├── runner.py              # Bot supervisor with auto-restart functionality
├── finbert_utils.py       # FinBERT sentiment analysis utilities
├── news.py                # News data retrieval functions
├── SMA Calc.py           # Simple Moving Average calculation utilities
├── temp.py               # Enhanced strategy with SMA integration
├── mailtest.py           # Email notification testing
├── requirements.txt      # Python dependencies
├── bot_state.pkl         # Trading state persistence file
└── logs/                 # Trading logs, statistics, and tearsheets
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Alpaca Trading Account (paper trading supported)
- Gmail account for notifications (optional)
- CUDA-compatible GPU (optional, for faster sentiment analysis)

### Dependencies Installation
```bash
pip install -r requirements.txt
```

### Key Dependencies
- **lumibot**: Trading framework and backtesting engine
- **alpaca-trade-api**: Alpaca brokerage integration
- **transformers**: Hugging Face transformers for FinBERT
- **torch**: PyTorch for machine learning
- **yfinance**: Yahoo Finance data
- **pandas**: Data manipulation
- **matplotlib/plotly**: Data visualization

## ⚙️ Configuration

### 1. Alpaca API Setup
Edit the API credentials in `tradingbot.py`, `news.py`, and `temp.py`:
```python
API_KEY = "your_alpaca_api_key"
API_SECRET = "your_alpaca_secret_key"
BASE_URL = "https://paper-api.alpaca.markets/v2"  # Paper trading
```

### 2. Email Notifications Setup
Configure email settings in `runner.py` and `mailtest.py`:
```python
msg['From'] = 'your_email@gmail.com'
msg['To'] = 'recipient@gmail.com'
# Add your Gmail app password in login()
mailserver.login('your_email@gmail.com', 'your_app_password')
```

### 3. Trading Parameters
Customize trading parameters in the strategy initialization:
```python
strategy = PaisaFy(name='mlstrat', broker=broker, 
                   parameters={"symbol":"TSLA",      # Stock symbol
                              "cash_at_risk":.5})   # Risk percentage
```

## 🚀 Usage

### Running the Bot
```bash
# Direct execution
python tradingbot.py

# With auto-restart functionality
python runner.py
```

### Backtesting
The bot includes backtesting capabilities. Modify the date range in `tradingbot.py`:
```python
start_date = datetime(2023,1,1)
end_date = datetime(2024,4,11)
```

### Testing Individual Components
```bash
# Test sentiment analysis
python finbert_utils.py

# Test SMA calculations
python "SMA Calc.py"

# Test news retrieval
python news.py

# Test email notifications
python mailtest.py
```

## 📊 Trading Strategy

### Buy Signals
- **Sentiment**: Positive news sentiment with >97% confidence
- **Technical**: 50-day SMA above 200-day SMA (bullish trend)
- **Execution**: Market buy with 20% take-profit and 5% stop-loss

### Sell Signals
- **Sentiment**: Negative news sentiment with >97% confidence
- **Technical**: 50-day SMA below 200-day SMA (bearish trend)
- **Execution**: Market sell with 20% take-profit and 5% stop-loss

### Risk Management
- Configurable cash-at-risk percentage (default: 50%)
- Bracket orders with automatic take-profit and stop-loss
- Position conflict prevention through state tracking

## 📈 Performance Monitoring

### Log Files
The `logs/` directory contains:
- **CSV files**: Detailed trading logs and statistics
- **HTML files**: Visual tearsheets and trade summaries
- **JSON files**: Strategy settings and parameters

### Log File Naming Convention
```
[BotName]_YYYY-MM-DD_HH-MM-SS_[type].[extension]
```

### Key Metrics Tracked
- Total returns and Sharpe ratio
- Win/loss ratios and maximum drawdown
- Trade frequency and position sizes
- Strategy parameters and market conditions

## 🔧 File Descriptions

| File | Purpose |
|------|---------|
| `tradingbot.py` | Main trading strategy (TSLA focused) |
| `temp.py` | Enhanced strategy with SMA integration (SPY focused) |
| `runner.py` | Supervisor script with crash recovery |
| `finbert_utils.py` | FinBERT sentiment analysis implementation |
| `news.py` | News data retrieval and processing |
| `SMA Calc.py` | Technical analysis utilities |
| `mailtest.py` | Email notification testing |
| `bot_state.pkl` | Persistent state storage |

## ⚠️ Important Notes

### Security
- **Never commit API keys** to version control
- Use environment variables for sensitive credentials
- Enable 2FA on your Alpaca account

### Trading Risks
- This bot trades with real money when live trading is enabled
- Always test thoroughly with paper trading first
- Monitor positions regularly, especially during high volatility
- Understand that past performance doesn't guarantee future results

### Technical Considerations
- FinBERT requires significant computational resources
- GPU acceleration recommended for faster sentiment analysis
- Ensure stable internet connection for real-time trading
- Monitor API rate limits to avoid service interruptions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Test thoroughly with paper trading
4. Submit a pull request with detailed descriptions

## 📄 License

This project is for educational purposes. Use at your own risk when trading with real money.

## 🔗 Resources

- [Alpaca API Documentation](https://alpaca.markets/docs/)
- [Lumibot Documentation](https://lumibot.lumiwealth.com/)
- [FinBERT Model](https://huggingface.co/ProsusAI/finbert)
- [Yahoo Finance API](https://pypi.org/project/yfinance/)

---

**Disclaimer**: This software is for educational and research purposes only. Trading involves significant financial risk, and you should never trade with money you cannot afford to lose. The authors are not responsible for any financial losses incurred through the use of this software. 