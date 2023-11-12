from classes import OKXex



f = OKXex().get_instrument()
for i in f:
    if i['quoteCcy'] == 'BTC':
        ...
    elif i['quoteCcy'] == 'USDC':
        ...
    elif i['quoteCcy'] == 'USDT':
        ...
    elif i['quoteCcy'] == 'TRY':
        ...
    elif i['quoteCcy'] == 'DAI':
        ...
    elif i['quoteCcy'] == 'ETH':
        ...
    else:
        print(i['instId'])
        print(i)

