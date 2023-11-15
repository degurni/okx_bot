import json

import okx.MarketData as Market  # pip install python-okx
from okx import Account, MarketData, PublicData, Trade
import pandas as pd
import pandas_ta as ta
from sklearn import preprocessing
import numpy as np
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
        return res['data'][0]['details']

    # TRADE
    def place_order(self, data):
        f = self.trade.place_order(**data)
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





# # Получить открытые позиции
# def get_positions(symbol: str = None):
#     """
#     Получить открытые позиции
#     :return: {'adl': '1',                          уровень делевереджа
#               'availPos': '',
#               'avgPx': '102.1168888888888889',     цена входа
#               'baseBal': '',
#               'baseBorrowed': '',
#               'baseInterest': '',
#               'bePx': '102.96527791777321',
#               'bizRefId': '',
#               'bizRefType': '',
#               'cTime': '1698925498071',
#               'ccy': 'USDT',
#               'closeOrderAlgo': [],
#               'deltaBS': '',
#               'deltaPA': '',
#               'fee': '-0.05816884',                комиссия
#               'fundingFee': '0.0080302563557077',
#               'gammaBS': '',
#               'gammaPA': '',
#               'idxPx': '101.316',
#               'imr': '3.0357000000000003',
#               'instId': 'TRB-USDT-SWAP',
#               'instType': 'SWAP',
#               'interest': '',
#               'last': '101.228',
#               'lever': '10',                       плечо
#               'liab': '',
#               'liabCcy': '',
#               'liqPenalty': '0',
#               'liqPx': '2.041765621390252',
#               'margin': '',
#               'markPx': '101.19',
#               'mgnMode': 'cross',
#               'mgnRatio': '139.99481419389195',
#               'mmr': '0.1973205',
#               'notionalUsd': '30.361553550000007',
#               'optVal': '',
#               'pendingCloseOrdLiabVal': '',
#               'pnl': '-0.1889333333333333',
#               'pos': '3',                          размер позиции
#               'posCcy': '',
#               'posId': '637080880187998214',       ID
#               'posSide': 'net',
#               'quoteBal': '',
#               'quoteBorrowed': '',
#               'quoteInterest': '',
#               'realizedPnl': '-0.2390719169776256',
#               'sId': 0,
#               'spotInUseAmt': '',
#               'spotInUseCcy': '',
#               'thetaBS': '',
#               'thetaPA': '',
#               'tradeId': '131783287',
#               'uTime': '1698954196183',
#               'upl': '-0.278066666666669',
#               'uplLastPx': '-0.26666666666667',
#               'uplRatio': '-0.0907674429738481',
#               'uplRatioLastPx': '-0.0870462171890174',
#               'usdPx': '',
#               'userId': 44786666,
#               'vegaBS': '',
#               'vegaPA': ''}
#
#     """
#     if symbol:
#         return accaunt.get_positions(instId=symbol)['data']
#     else:
#         # Если не пердовать название торговой пары то получим только открытые позиции
#         return accaunt.get_positions(instType='SWAP')['data']
#
#
# # Изменяем плечо
# def set_lever(symbol: str, lever: str):
#     """
#     Изменяем плечо
#     :param symbol:       DYDX-USDT-SWAP
#     :param lever:        желаемое плечо
#     :return:
#     """
#     s = accaunt.set_leverage(instId=symbol, lever=lever, mgnMode='cross')
#     return s
#
#
#
#
#
# def amend_order(symbol: str):
#     s = trade.amend_order(instId=symbol, newTpTriggerPx='129.065', newTpOrdPx='-1',
#                           newSlTriggerPx='123.929', newSlOrdPx='-1')
#     return s
#
# def plas_order(symbol: str, side: str, size: str):
#     data = {
#         'instId': symbol,
#         'tdMode': 'cross',
#         'side': side,
#         'ordType': 'market',
#         'sz': size
#     }
#     poz_id = trade.place_order(**data)['data']['ordId']
#     # Запрашиваем информацию об открытой позиции
#     f = get_positions(symbol=symbol)
#     open_price = f[0]['avgPx']
#     fee = f[0]['fee']
#     lever = f[0]['lever']
#     size = f[0]['pos']
#     pos_id = f[0]['posId']
#
#
#
#
#
# def plas_order_and_tp_sl(symbol: str, side: str, size: str, tp: str, sl: str):
#     """
#     Выставляем рыночный ордер и тейкпрофит и стоплосс
#     :param symbol:      ATOM-USDT-SWAP
#     :param side:        buy или sell
#     :param size:        кол-во контрактов
#     :param tp:          цена тейкпрофита
#     :param sl:          цена стоплосса
#     :return:
#     """
#     answer = trade.place_order(instId=symbol, tdMode='cross', side=side, ordType='market',
#                                sz=size, tpTriggerPx=tp, tpOrdPx='-1', slTriggerPx=sl, slOrdPx='-1')
#     return answer['data']
#
# def pairs(type: str='SPOT') -> list:
#     """
#
#     :param type:
#     :return: {'alias': '',
#               'baseCcy': 'FTM',
#               'category': '1',
#               'ctMult': '',
#               'ctType': '',
#               'ctVal': '',
#               'ctValCcy': '',
#               'expTime': '',
#               'instFamily': '',
#               'instId': 'FTM-OKB',
#               'instType': 'SPOT',
#               'lever': '',
#               'listTime': '1635155926000',
#               'lotSz': '0.000001',
#               'maxIcebergSz': '999999999999.0000000000000000',
#               'maxLmtSz': '999999999999',
#               'maxMktSz': '1000000',
#               'maxStopSz': '1000000',
#               'maxTriggerSz': '999999999999.0000000000000000',
#               'maxTwapSz': '999999999999.0000000000000000',
#               'minSz': '1',
#               'optType': '',
#               'quoteCcy': 'OKB',
#               'settleCcy': '',
#               'state': 'live',
#               'stk': '',
#               'tickSz': '0.00001',
#               'uly': ''}
#
#     """
#     res = public.get_instruments(instType=type)['data']
#     pairs = []
#     for i in res:
#         pairs.append(i['instId'])
#     return pairs






def detect_accumulation(df):
    means = df.Volume.mean()

    accum = [0] * len(df)
    detect = [0] * len(df)
    sum_detect = [0] * len(df)
    for i in range(len(df)):
        accum[i] = round(means / df.Volume.iloc[i], 2)
        detect[i] = round(df.Volume.diff().iloc[i] / df.Volume.iloc[i], 2)
    df['accum'] = accum
    df['detect'] = detect

    sum_detect[-1] = df.detect.iloc[-1]
    for i in reversed(range(len(df) - 1)):
        sum_detect[i] = sum_detect[i + 1] + df.detect.iloc[i]
    df['sum_detect'] = sum_detect
    print(df.sum_detect.max())
    df.to_csv('df_data.csv')

def _lenght_vektor(df):
    lenght_v = [0] * len(df)
    vector_sig = [0] * len(df)
    for i in range(len(df)):
        lenght_v[i] = math.sqrt(1 + (abs(df.MACD.iloc[i]) - abs(df.MACD.iloc[i-1])) ** 2)
        if lenght_v[i] > 1.000_012:
            vector_sig[i] = 2
        elif lenght_v[i] > 1.000_009:
            vector_sig[i] = 1
    df['lenght_v'] = lenght_v
    df['vector_sig'] = vector_sig
    return df






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

    def _chek_signal(self, df):
        sig = [0] * len(df)
        for i in range(len(df)):
            if df.CCI_sig.iloc[i] == 'sell' and df.MACD_sig.iloc[i] == 'sell':
                sig[i] = 'sell'
                # print(df.index[i], sig[i])
            elif df.CCI_sig.iloc[i] == 'buy' and df.MACD_sig.iloc[i] == 'buy':
                sig[i] = 'buy'
                # print(df.index[i], sig[i])
        df['SIG'] = sig
        # print(df.SIG.value_counts())
        return df

    def _chek_CCI_signal(self, df: pd.DataFrame) -> pd.DataFrame:
        predel = 90
        cci_sig = [0] * len(df)
        for i in range(len(df)):
            if df.CCI.iloc[i] > predel and df.CCI.iloc[i] < df.CCI.iloc[i - 1]:
                cci_sig[i] = 'sell'
            elif df.CCI.iloc[i] < -1 * predel and df.CCI.iloc[i] > df.CCI.iloc[i - 1]:
                cci_sig[i] = 'buy'
        df['CCI_sig'] = cci_sig
        # print(df.CCI_sig.value_counts())
        return df

    def _chek_macd_signal(self, df: pd.DataFrame) -> pd.DataFrame:
        predel = 0.3
        macd_sig = [0] * len(df)
        for i in range(len(df)):
            if df.MACDh.iloc[i] > predel and df.MACDh.iloc[i] < df.MACDh.iloc[i - 1]:
                macd_sig[i] = 'sell'
            elif df.MACDh.iloc[i] < -1 * predel and df.MACDh.iloc[i] > df.MACDh.iloc[i - 1]:
                macd_sig[i] = 'buy'
        df['MACD_sig'] = macd_sig
        # print(df.MACD_sig.value_counts())
        return df

    def add_indicator(self, df: pd.DataFrame) -> pd.DataFrame:
        df[['MACD', 'MACDh', 'MACDs']] = ta.macd(close=df.Close, fast=12, slow=26, signal=9)
        scaler = preprocessing.MinMaxScaler(feature_range=(-1, 1))
        df['MACD'] = scaler.fit_transform(df[['MACD']])
        df['MACDh'] = scaler.fit_transform(df[['MACDh']])
        df['MACDs'] = scaler.fit_transform(df[['MACDs']])

        df['CCI'] = ta.cci(high=df.High, low=df.Low, close=df.Close, length=40)

        df = Bot()._chek_CCI_signal(df=df)
        df = Bot()._chek_macd_signal(df=df)

        df = Bot()._chek_signal(df)
        # df.to_csv('df_data.csv')
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

    def buy_order(self, inf: dict, price: float):
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





    def zero_orders(self, inf: dict):
        if len(inf['orders']) == 0:
            # Bot().debug('debug', f'По торговой паре {inf["symbol"]} ордера не выставлялись')
            df = Bot().frame(symbol=inf['symbol'])
            df = Bot().add_indicator(df)
            df.to_csv(f'df_data_{inf["symbol"]}.csv')
            if df.SIG.iloc[-2] == 'buy':
                Bot().debug('debug', f'{inf["symbol"]}: Выставляем маркет ордер на покупку')
                Bot().buy_order(inf=inf, price=float(df.Close.iloc[-1]))





        else:
            Bot().debug('debug', f'{inf["symbol"]}: Проверяем последний выставленный ордер')

