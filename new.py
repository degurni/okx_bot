from classes import OKXex



f = OKXex().get_instrument(symbol='NEAR-BTC')
print(f[0])
