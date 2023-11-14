import json
import time

import conf
from classes import OKXex, Bot




def start():
    Bot().chek_files()  # Проверяем существование файла <trades.json>
    Bot().fill_trades_file()

def trades_bot():
    with open('trades.json', 'r') as f:
        infa = json.loads(f.read())
    for symbol in conf.symbols:
        for inf in infa:
            if symbol == inf['symbol']:
                if len(inf['orders']) == 0:
                    Bot().zero_orders(inf=inf)

        time.sleep(conf.sleep_4)



















if __name__ == '__main__':

    start()
    while True:
        trades_bot()
        time.sleep(conf.sleep_1)



    # try:
    #     start()
    #     while True:
    #         trades_bot()
    #         time.sleep(conf.sleep_1)
    #
    # except Exception as e:
    #     print(e)
    # except KeyboardInterrupt:
    #     Bot().debug('debug', 'Бот остановлен вручную')



