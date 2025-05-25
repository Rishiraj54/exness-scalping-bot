from keep_alive import keep_alive
import requests
import time
import os
from telegram import Bot

# Start keep-alive server
keep_alive()

# Set environment variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
API_KEY = os.getenv("TWELVE_DATA_API_KEY")

bot = Bot(token=TOKEN)

def send_signal(pair, entry, exit, stoploss, pips):
    message = f"""📊 Signal Alert
Pair: {pair}
Entry: {entry}
Exit: {exit}
Stoploss: {stoploss}
Profit/Loss: {pips} pips"""
    bot.send_message(chat_id=CHAT_ID, text=message)

def check_market(pair):
    url = f"https://api.twelvedata.com/time_series?symbol={pair}&interval=1min&apikey={API_KEY}&outputsize=5"
    r = requests.get(url)
    data = r.json()

    # Example logic: trigger when candle closes higher than open
    candles = data['values']
    latest = candles[0]

    open_price = float(latest['open'])
    close_price = float(latest['close'])

    if close_price > open_price:
        send_signal(pair, entry=close_price, exit=close_price+0.0010, stoploss=close_price-0.0010, pips=10)

def main():
    pairs = ["EUR/USD", "XAU/USD", "GBP/USD"]
    symbol_map = {"EUR/USD": "EUR/USD", "XAU/USD": "XAU/USD", "GBP/USD": "GBP/USD"}

    while True:
        for pair in pairs:
            check_market(symbol_map[pair])
        time.sleep(60)

main()
