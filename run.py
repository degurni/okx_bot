import time

import conf
import classes



def search():
    for symbol in conf.symbols:
        data = classes.candles(symbol)
        df = classes.frame(data=data)
        df = classes.add_indicator(df=df)
        if df.SIG.iloc[-1] != 0:
            print(f'Получен сигнал --> {symbol}: {df.SIG.iloc[-1]}')













if __name__ == '__main__':
    classes.chek_files()
    while True:
        search()
        time.sleep(conf.sleep_1)


