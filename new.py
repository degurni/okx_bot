from classes import OKXex, Bot


symbol = 'XRP-USDT'

df = Bot().frame(symbol)
df = Bot().indicator_TSI(df)

print(df)



