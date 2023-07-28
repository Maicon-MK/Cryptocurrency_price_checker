import requests
import datetime
import tkinter as tk
from tkinter import messagebox

def get_binance_price(symbol, quote_currency):
    base_url = "https://api.binance.com/api/v3/ticker/price"
    params = {
        "symbol": symbol.upper() + quote_currency.upper()
    }

    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            return float(data["price"])
        else:
            print(f"Falha na solicitação. Código de status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão: {e}")
    
    return None

def get_recent_trades(symbol, quote_currency):
    base_url = "https://api.binance.com/api/v3/trades"
    params = {
        "symbol": symbol.upper() + quote_currency.upper(),
        "limit": 5  
    }

    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            crypto_data = response.json()
            price_changes = crypto_data
            print(f"Últimas cinco alterações do {symbol.capitalize()}:")
            for change in price_changes[-5:]:
                timestamp, price = change["time"], float(change["price"])
                date_time = datetime.datetime.fromtimestamp(timestamp // 1000)  
                date_time_str = date_time.strftime("%Y-%m-%d %H:%M:%S")
                print(f"{date_time_str} - Preço: ${price:.2f}")
    
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão: {e}")
    
    return price_changes

def get_user_input():
    symbol = input("Digite o símbolo da criptomoeda (exemplo: btc): ").lower()
    quote_currency = input("Digite a moeda desejada (usdt, eur, brl, etc.): ").lower()
    return symbol, quote_currency

def validate_symbol_and_currency(symbol, quote_currency):
    valid_symbols = ["btc", "eth", "ltc", "xrp", "bch"]  
    valid_currencies = ["usdt", "eur", "brl", "usd", "eur"]  

    while symbol not in valid_symbols or quote_currency not in valid_currencies:
        print("Criptomoeda ou moeda corrente inválida. Por favor, tente novamente.")
        symbol, quote_currency = get_user_input()
    
    return symbol, quote_currency

def show_crypto_price():
    symbol = crypto_symbol_input.get().lower()
    quote_currency = quote_currency_input.get().lower()
    symbol, quote_currency = validate_symbol_and_currency(symbol, quote_currency)
    crypto_price = get_binance_price(symbol, quote_currency)

    if crypto_price is not None:
        crypto_price_label.config(text=f"Preço atual do {symbol.upper()} em {quote_currency.upper()}: {crypto_price:.2f}")

        recent_trades = get_recent_trades(symbol, quote_currency)
        if recent_trades is None:
            recent_trades_label.config(text="Últimas 5 alterações de valores:")
        else:
            recent_trades_str = "Últimas cinco alterações do {symbol.capitalize()}:\n"
            for change in recent_trades[-5:]:
                timestamp, price = change["time"], float(change["price"])
                date_time = datetime.datetime.fromtimestamp(timestamp // 1000)
                date_time_str = date_time.strftime("%Y-%m-%d %H:%M:%S")
                recent_trades_str += f"{date_time_str} - Preço: ${price:.2f}\n"
            recent_trades_label.config(text=recent_trades_str)

def on_exit():
    if messagebox.askokcancel("Exit", "Deseja sair da aplicação?"):
        root.destroy()

root = tk.Tk()
root.title("Cryptocurrency Price Checker")
root.geometry("400x300")
root.protocol("WM_DELETE_WINDOW", on_exit)

instruction_label = tk.Label(root, text="Choose a cryptocoin and a quote")
instruction_label.pack(pady=10)

crypto_symbol_label = tk.Label(root, text="Type a cryptocoin symbol (example: eth)")
crypto_symbol_label.pack(pady=5)

crypto_symbol_input = tk.Entry(root)
crypto_symbol_input.pack()

quote_currency_label = tk.Label(root, text="Choose a quote (example: usdt, eur, brl, etc)")
quote_currency_label.pack(pady=5)

quote_currency_input = tk.Entry(root)
quote_currency_input.pack()

crypto_price_label = tk.Label(root, text="")
crypto_price_label.pack(pady=10)

recent_trades_label = tk.Label(root, text="")
recent_trades_label.pack(pady=10)

check_button = tk.Button(root, text="Check Price", command=show_crypto_price)
check_button.pack(pady=10)

def reset_inputs():
    crypto_symbol_input.delete(0, tk.END)
    quote_currency_input.delete(0, tk.END)
    crypto_price_label.config(text="")
    recent_trades_label.config(text="")

def on_enter(event):
    show_crypto_price()

root.bind('<Return>', on_enter)

root.mainloop()
