
import classes


if __name__ == '__main__':
    data = classes.candles('ATOM-USDT-SWAP')
    df = classes.frame(data=data)
    df = classes.add_indicator(df=df)
    print(df)
