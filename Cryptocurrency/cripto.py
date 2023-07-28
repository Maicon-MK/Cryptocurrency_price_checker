import requests
import datetime 

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
                date_time = datetime.datetime.fromtimestamp(timestamp // 1000)  # Convertendo milissegundos para segundos
                date_time_str = date_time.strftime("%d-%m-%Y %H:%M:%S")
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

if __name__ == "__main__":
    while True:
        symbol, quote_currency = get_user_input()
        symbol, quote_currency = validate_symbol_and_currency(symbol, quote_currency)

        crypto_price = get_binance_price(symbol, quote_currency)

        if crypto_price is not None:
            print(f"Preço atual do {symbol.upper()} em {quote_currency.upper()}: {crypto_price:.2f}")

            recent_trades = get_recent_trades(symbol, quote_currency)
            if recent_trades is  None:
                print("\nÚltimas 5 alterações de valores:")

        continue_input = input("Deseja consultar outra criptomoeda e moeda corrente? (Digite 's' para sim ou qualquer outra coisa para sair): ")
        if continue_input.lower() != 's':
            break
