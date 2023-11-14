from classes import OKXex, Bot

inf = {
    "symbol": "LUNC-USDT",
    "base_cur": "LUNC",
    "quote_cur": "USDT",
    "min_size": "10000",
    "tick_size": "0.00000001",
    "orders": []
  }

# f = Bot().buy_order(inf=inf)
symbol = 'LUNC-USDT'

f = OKXex().get_instrument(symbol=symbol)[0]
print(f)

"""
{ 
'baseCcy': 'NEAR',              'baseCcy': 'LUNC',
'instId': 'NEAR-USDT',          'instId': 'LUNC-USDT',
'lever': '5',                   'lever': '5', 
'lotSz': '0.00000001',          'lotSz': '1',
'minSz': '5',                   'minSz': '10000',
'quoteCcy': 'USDT',             'quoteCcy': 'USDT',
'tickSz': '0.001',              'tickSz': '0.00000001',
}

"""