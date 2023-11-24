
import json
import okx.MarketData as Market
from okx import Account, MarketData, PublicData, Trade
import pandas as pd
import pandas_ta as ta
from decimal import Decimal, ROUND_FLOOR
import math
import datetime
import os

import conf
if os.path.isfile('keys.py'):
    import keys
    key = keys.key
    secret = keys.secret
    passw = keys.passw
else:
    key = conf.key
    secret = conf.secret
    passw = conf.passw

class OKXex:

    def __init__(self):
        flag = '0'  # 0 - живая торговля, 1 - тестовая торговля
        self.public = PublicData.PublicAPI(flag=flag, debug=False)
        self.market = Market.MarketAPI(flag=flag, debug=False)
        self.accaunt = Account.AccountAPI(api_key=key, api_secret_key=secret, passphrase=passw,
                                 flag=flag, debug=False)
        self.trade = Trade.TradeAPI(api_key=key, api_secret_key=secret, passphrase=passw,
                           flag=flag, debug=False)

    # MARKET
    def candles(self, pair: str = 'BTC-USDT', tf: str = '15m', limit: str = '300') -> list:
        """
        Получить сведения о 300 последних рыночных свечах
        :param instId:
        :param bar:
        :param limit:
        :return:['1697125500000',           -Время
                 '26668.4',                 -Открытие
                 '26697.9',                 -Максимум
                 '26605',                   -Минимум
                 '26677.2',                 -Закрытие
                 '6000603.65197306',
                 '159971120351.05124191',
                 '159971120351.05124191',
                 '0']                       -1 - завершена. 0 - не завершена
        """
        res = self.market.get_candlesticks(instId=pair, bar=tf, limit=limit)
        if res['code'] == '0' and res['msg'] == '':
            # print(res['data'])
            return res['data']
        else:
            print(f'code - {res["code"]} : msg - {res["msg"]}')
            return []

    # PUBLIC
    def get_instrument(self, symbol: str | None = None, inst_type: str = 'SPOT') -> list:
        """
        https://www.okx.com/docs-v5/en/#public-data-rest-api-get-instruments
        Получаем информацию о торговой паре, если не указывать название торговой пары
        то получим о всех торговых парах на рынке
        :param symbol:
        :param inst_type: SPOT, MARGIN, SWAP, FUTURES, OPTION
        :return:{'alias': '',
                 'baseCcy': 'NEAR',
                 'category': '1',
                 'ctMult': '',
                 'ctType': '',
                 'ctVal': '',
                 'ctValCcy': '',
                 'expTime': '',
                 'instFamily': '',
                 'instId': 'NEAR-BTC',
                 'instType': 'SPOT',
                 'lever': '3',
                 'listTime': '1606950015000',
                 'lotSz': '1',
                 'maxIcebergSz': '9999999999999999.0000000000000000',
                 'maxLmtAmt': '20000000',
                 'maxLmtSz': '9999999999999999',
                 'maxMktAmt': '1000000',
                 'maxMktSz': '1000000',
                 'maxStopSz': '1000000',
                 'maxTriggerSz': '9999999999999999.0000000000000000',
                 'maxTwapSz': '9999999999999999.0000000000000000',
                 'minSz': '1',
                 'optType': '',
                 'quoteCcy': 'BTC',
                 'settleCcy': '',
                 'state': 'live',
                 'stk': '',
                 'tickSz': '0.00000001',
                 'uly': ''}

        """
        if symbol:
            res = self.public.get_instruments(instType=inst_type, instId=symbol)
        else:
            res = self.public.get_instruments(instType=inst_type)
        if res['code'] == '0':
            return res['data']
        else:
            return res['msg']

    # ACCAUNT
    # Получаем баланс
    def get_balance(self, currency: str = None):
        if currency:
            res = self.accaunt.get_account_balance(ccy=currency)
        else:
            res = self.accaunt.get_account_balance()
        # print(res)
        return res['data'][0]['details']

    # TRADE
    def place_order(self, data):
        f = self.trade.place_order(**data)
        # print(f)
        return f['data'][0]['ordId']

    def order_details(self, symbol: str, ord_id: str):
        """

        :param symbol:
        :param ord_id:
        :return: {'accFillSz': '0.019825',
                  'algoClOrdId': '',
                  'algoId': '',
                  'attachAlgoClOrdId': '',
                  'attachAlgoOrds': [],
                  'avgPx': '25.22',
                  'cTime': '1700040545922',
                  'cancelSource': '',
                  'cancelSourceReason': '',
                  'category': 'normal',
                  'ccy': '',
                  'clOrdId': '',
                  'fee': '-0.000019825',
                  'feeCcy': 'KSM',
                  'fillPx': '25.22',
                  'fillSz': '0.019825',
                  'fillTime': '1700040545924',
                  'instId': 'KSM-USDT',
                  'instType': 'SPOT',
                  'lever': '',
                  'ordId': '644952027235651597',
                  'ordType': 'market',
                  'pnl': '0',
                  'posSide': 'net',
                  'px': '',
                  'pxType': '',
                  'pxUsd': '',
                  'pxVol': '',
                  'quickMgnType': '',
                  'rebate': '0',
                  'rebateCcy': 'USDT',
                  'reduceOnly': 'false',
                  'side': 'buy',
                  'slOrdPx': '',
                  'slTriggerPx': '',
                  'slTriggerPxType': '',
                  'source': '',
                  'state': 'filled',
                  'stpId': '',
                  'stpMode': '',
                  'sz': '0.5',
                  'tag': '',
                  'tdMode': 'cash',
                  'tgtCcy': 'quote_ccy',
                  'tpOrdPx': '',
                  'tpTriggerPx': '',
                  'tpTriggerPxType': '',
                  'tradeId': '20809503',
                  'uTime': '1700040545927'}

        """
        return self.trade.get_order(instId=symbol, ordId=ord_id)['data'][0]

class Bot:

    def _time(self):
        return datetime.datetime.now().strftime('%H:%M:%S')

    def debug(self, var: str, inf: str) -> None:
        time = Bot()._time() if var == 'debug' else None
        if conf.debug == 'inform':
            if var == 'inform':
                print(inf)
            elif var == 'debug':
                print('\033[32m {} - {} \033[0;0m'.format(time, inf))
            else:
                print('\033[31m {} \033[0;0m'.format(inf))
        if conf.debug == 'debug':
            if var == 'debug':
                print('\033[32m {} - {} \033[0;0m'.format(time, inf))
            else:
                print('\033[31m {} \033[0;0m'.format(inf))
        if conf.debug == 'error':
            if var == 'error':
                print('\033[31m {} \033[0;0m'.format(inf))

    def chek_files(self):
        Bot().debug('debug', 'Проверяем наличие вспомогательных файлов')
        if not os.path.isfile('trades.json'):
            with open('trades.json', 'w') as f:
                json.dump([], f, indent=2)

    def fill_trades_file(self):
        with open('trades.json', 'r') as f:
            inf = json.loads(f.read())
        if len(inf):
            l = []
            for i in inf:
                l.append(i['symbol'])
            for symbol in conf.symbols:
                if l.count(symbol) == 0:
                    s = OKXex().get_instrument(symbol=symbol)[0]
                    data = {
                        'symbol': s['instId'],
                        'base_cur': s['baseCcy'],
                        'quote_cur': s['quoteCcy'],
                        'min_size': s['minSz'],
                        'lotsize': s['lotSz'],
                        'tick_size': s['tickSz'],
                        'orders': []
                    }
                    inf.append(data)
        else:
            for symbol in conf.symbols:
                s = OKXex().get_instrument(symbol=symbol)[0]
                data = {
                    'symbol': s['instId'],
                    'base_cur': s['baseCcy'],
                    'quote_cur': s['quoteCcy'],
                    'min_size': s['minSz'],
                    'lotsize': s['lotSz'],
                    'tick_size': s['tickSz'],
                    'orders': []
                }
                inf.append(data)
        with open('trades.json', 'w') as f:
            json.dump(inf, f, indent=2)

    def checking_open_positions(self, symbol: str = None):
        with open('trades.json', 'r') as f:
            inf = json.loads(f.read())
        s = False
        if symbol and len(inf) != 0:
            for i in inf:
                if i['symbol'] == symbol:
                    s = True
        elif not symbol:
            if len(inf) == 0:
                Bot().debug('debug', 'Бот ещё не выставлял ордера, открытых позиций нет')
            else:
                Bot().debug('debug', f'Открыто {len(inf)} позиций')
        return s

    def indicator_TSI(self, df: pd.DataFrame) -> pd.DataFrame:
        fast = 25
        slow = 13
        sig = 13
        df[['TSI', 'TSI_s']] = ta.tsi(close=df.Close, fast=fast, slow=slow, signal=sig)
        signal = [0] * len(df)
        for i in range(len(df)):
            if 0 > df.TSI.iloc[i] > df.TSI.iloc[i - 1] < df.TSI.iloc[i - 2]:
                signal[i] = 'buy'
            elif df.TSI.iloc[i] < df.TSI.iloc[i - 1] > df.TSI.iloc[i - 2]:
                signal[i] = 'sell'
        df['SIG'] = signal
        return df

    # Преобразовываем данные о свечах в датафрейм
    def frame(self, symbol):
        data = OKXex().candles(pair=symbol, tf=conf.tf)
        t = []
        o = []
        h = []
        l = []
        c = []
        v = []
        for i in data:
            t.append(int(i[0]) / 1000)
            o.append(float(i[1]))
            h.append(float(i[2]))
            l.append(float(i[3]))
            c.append(float(i[4]))
            v.append(float(i[5]))
        df = pd.DataFrame({'Time': t, 'Open': o, 'High': h, 'Low': l, 'Close': c, 'Volume': v})
        df.Time = pd.to_datetime(df.Time, unit='s')
        df.set_index('Time', inplace=True)
        df.sort_index(ascending=True, inplace=True)
        # df.to_csv('df_data.csv')
        return df

    def leveling(self, size: float, lotsize: str):
        size = Decimal(str(size))
        size = size.quantize(Decimal(lotsize), ROUND_FLOOR)
        return str(size)

    def buy_order(self, inf: dict, price: float) -> dict:
        # Проверяем баланс для покупки
        balance = OKXex().get_balance(inf['quote_cur'])[0]['availBal']
        if float(balance) < conf.sz_quote:
            Bot().debug('error', f'Недостаточно {inf["quote_cur"]} для выставления ордера')
        else:
            size = conf.sz_quote / price
            size = Bot().leveling(size=size, lotsize=inf['lotsize'])
            data = {
                'instId': inf['symbol'],
                'tdMode': 'cash',
                'side': 'buy',
                'ordType': 'market',
                'tgtCcy': 'base_ccy',
                'sz': size,
            }
            order_id = OKXex().place_order(data=data)
            order_inf = OKXex().order_details(symbol=inf['symbol'], ord_id=order_id)
            size = str(float(order_inf['accFillSz']) + float(order_inf['fee']))
            res = {
                'order_id': order_inf['ordId'],
                'price': order_inf['avgPx'],
                'size': size
            }
            Bot().debug('debug', f'Куплено {size} {inf["base_cur"]} по цене {order_inf["avgPx"]} {inf["quote_cur"]}')
            inf['orders'].append(res)
            return inf

    def sell_order(self, inf: dict):
        # Проверяем баланс для продажи
        balance = OKXex().get_balance(inf['base_cur'])[0]['availBal']
        if len(inf['orders']) > 1 and float(balance) > 0:
            size = float(inf['orders'][-1]['size'])
        else:
            size = float(balance)
        size = Bot().leveling(size=size, lotsize=inf['lotsize'])
        data = {
            'instId': inf['symbol'],
            'tdMode': 'cash',
            'side': 'sell',
            'ordType': 'market',
            'tgtCcy': 'base_ccy',
            'sz': size,
        }
        order_id = OKXex().place_order(data=data)
        order_inf = OKXex().order_details(symbol=inf['symbol'], ord_id=order_id)
        if order_inf['state'] == 'filled':
            Bot().debug('error', f'Продано {order_inf["accFillSz"]} {inf["base_cur"]} по цене '
                                 f'{order_inf["avgPx"]} {inf["quote_cur"]}')
            if len(inf['orders']) > 1:
                inf['orders'][-2]['price'] = str(float(inf['orders'][-2]['price']) * conf.less)
            inf['orders'].pop()
        return inf

    def zero_orders(self, inf: dict) -> dict:
        df = Bot().frame(symbol=inf['symbol'])
        df = Bot().indicator_TSI(df)
        # df.to_csv(f'df_data_{inf["symbol"]}.csv')
        if len(inf['orders']) == 0:  # Если ордеров ещё не было
            if df.SIG.iloc[-1] == 'buy':  # Если сигнал на покупку
                Bot().debug('debug', f'{inf["symbol"]}: Выставляем маркет ордер на покупку')
                inf = Bot().buy_order(inf=inf, price=float(df.Close.iloc[-1]))

        else:  # Если ордера по инструменту уже стоят
            # Bot().debug('debug', f'{inf["symbol"]}: Проверяем последний выставленный ордер')
            # Если последняя цена больше цены последнего ордера на указанный процент и сигнал на продажу
            if df.Close.iloc[-1] > float(inf['orders'][-1]['price']) * conf.steps[0] and df.SIG.iloc[-1] == 'sell':
                Bot().debug('degbug', f'{inf["symbol"]}: Выставляем маркет ордер на продажу')
                inf = Bot().sell_order(inf=inf)

            # Если последняя цена муньше цены последнего ордера на указаный процент и сигнал на покупку
            elif df.Close.iloc[-1] < float(inf['orders'][-1]['price']) * conf.steps[1] and \
                    df.SIG.iloc[-1] == 'buy':
                Bot().debug('debug', f'{inf["symbol"]}: Выставляем маркет ордер на покупку')
                inf = Bot().buy_order(inf=inf, price=float(df.Close.iloc[-1]))

        return inf