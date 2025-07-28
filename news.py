from alpaca_trade_api import REST

API_KEY = "PKSMWXDJFYEZKBFLSKE7"
API_SECRET = "1bbjhNjtjmLiYfUhbdLnJhNiQ7pYMUG6ndXhyqoA"
BASE_URL = "https://paper-api.alpaca.markets/v2"

api = REST(base_url=BASE_URL, key_id=API_KEY, secret_key=API_SECRET)

def get_news(symbol, start_date, end_date):
    news = api.get_news(symbol=symbol, start=start_date, end=end_date)
    headlines = [ev.__dict__["_raw"]["headline"] for ev in news]
    return headlines

# Example usage:
symbol = "SPY"
start_date = "2024-01-01"
end_date = "2024-04-11"
headlines = get_news(symbol, start_date, end_date)

for headline in headlines:
    print(headline)