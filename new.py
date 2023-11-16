from classes import OKXex, Bot


symbol = 'DYDX-USDT'

df = Bot().frame(symbol)
df = Bot().indicator(df)

print(df)



