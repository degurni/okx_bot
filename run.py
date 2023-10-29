
import conf
import classes


if __name__ == '__main__':
    data = classes.candles(conf.symbols[2])
    df = classes.frame(data=data)
    df = classes.add_indicator(df=df)
    print(df)


