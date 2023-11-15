from classes import OKXex, Bot


order_inf = OKXex().order_details(symbol='MATIC-USDT', ord_id='645113822290153484')

print(order_inf['state'])
