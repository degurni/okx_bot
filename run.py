import time

import conf
import classes
from classes import Bot

bot = Bot()

def start():
    bot.debug('debug', 'Бот запущен на бирже OKX ')
    bot.debug('debug', f'Отслеживаем {len(conf.symbols)} торговых пар')
    for symbol in conf.symbols:
        print(symbol.center(30, '_'))
    bot.chek_files()
    bot.checking_open_positions()

def search():
    for symbol in conf.symbols:
        s = bot.checking_open_positions(symbol=symbol)
        if s == True:
            print(f'позиция {symbol} уже открыта')



        else:
            data = classes.candles(symbol)
            df = classes.frame(data=data)
            df = classes.add_indicator(df=df)
            if df.SIG.iloc[-1] != 0:  # 'LONG', 'SHORT'
                bot.debug('debug', f'Получен сигнал --> {symbol}: {df.SIG.iloc[-1]}')
















if __name__ == '__main__':
    try:
        start()

        while True:
            search()
            time.sleep(conf.sleep_1)
    except KeyboardInterrupt:
        bot.debug('debug', 'Бот остановлен вручную')


